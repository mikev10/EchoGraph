"""AI-assisted merge using Claude API."""

from dataclasses import dataclass

from rich.console import Console
from rich.status import Status

from echograph_cli.core.merge import (
    ConflictMarkerStyle,
    three_way_merge_sections,
)
from echograph_cli.output import print_unified_diff


@dataclass
class AIMergeResult:
    """Result of an AI-assisted merge operation."""

    merged_content: str
    explanation: str
    had_conflicts: bool
    user_approved: bool
    was_skipped_whitespace: bool = False  # True if skipped due to whitespace-only diff


def _normalize_whitespace(content: str) -> str:
    """Normalize whitespace for comparison.

    Strips trailing whitespace from lines, normalizes line endings,
    collapses multiple blank lines into one, and removes blank lines
    at the start/end of sections.
    """
    lines = content.replace("\r\n", "\n").split("\n")
    # Strip trailing whitespace from each line
    lines = [line.rstrip() for line in lines]
    # Join and collapse multiple blank lines
    text = "\n".join(lines)
    while "\n\n\n" in text:
        text = text.replace("\n\n\n", "\n\n")
    # Remove blank lines after headers (## Header\n\n -> ## Header\n)
    import re
    text = re.sub(r"(^#+\s+.+)\n\n+", r"\1\n", text, flags=re.MULTILINE)
    # Remove blank lines before headers
    text = re.sub(r"\n\n+(#+\s+)", r"\n\n\1", text)
    return text.strip()


def is_whitespace_only_diff(content1: str, content2: str) -> bool:
    """Check if two contents differ only in whitespace.

    Returns True if the only differences are:
    - Trailing whitespace on lines
    - Number of blank lines between sections
    - Line ending differences (CRLF vs LF)
    """
    # First try exact normalized comparison
    if _normalize_whitespace(content1) == _normalize_whitespace(content2):
        return True

    # If that fails, check if diff only contains blank line changes
    import difflib

    lines1 = content1.replace("\r\n", "\n").split("\n")
    lines2 = content2.replace("\r\n", "\n").split("\n")

    diff = list(difflib.unified_diff(lines1, lines2, lineterm=""))

    # Check each changed line - if all changes are blank/whitespace-only, skip
    for line in diff:
        if line.startswith("---") or line.startswith("+++") or line.startswith("@@"):
            continue
        if line.startswith("-") or line.startswith("+"):
            # Get the actual content (skip the +/- prefix)
            content = line[1:]
            # If this changed line has non-whitespace content, it's a real change
            if content.strip():
                return False

    return True


def is_placeholder_only_diff(user_content: str, template_content: str) -> bool:
    """Check if the only differences are placeholder substitutions.

    Detects when user's file is the template with [[PLACEHOLDER]] values replaced.
    In this case, the user's content is "correct" and no merge is needed.
    """
    import re

    # Find all placeholders in template like [[PROJECT_NAME]], [[AUTHOR]], etc.
    placeholders = re.findall(r"\[\[([A-Z_]+)\]\]", template_content)

    if not placeholders:
        return False

    # Create a regex pattern from the template where placeholders become wildcards
    # Escape regex special chars first, then replace placeholders with capture groups
    pattern = re.escape(template_content)
    for placeholder in placeholders:
        # Replace escaped placeholder with a non-greedy wildcard
        escaped_placeholder = re.escape(f"[[{placeholder}]]")
        pattern = pattern.replace(escaped_placeholder, r".+?")

    # Normalize whitespace for comparison
    user_normalized = _normalize_whitespace(user_content)
    pattern_normalized = _normalize_whitespace(pattern)

    # Check if user content matches the pattern
    try:
        if re.fullmatch(pattern_normalized, user_normalized, re.DOTALL):
            return True
    except re.error:
        pass

    return False


def is_high_similarity(
    user_content: str, template_content: str, threshold: float = 0.95
) -> bool:
    """Check if files are very similar (>95% by default).

    When files are nearly identical, the user's version should be kept as-is
    since they haven't made significant customizations and the template
    hasn't changed significantly.
    """
    import difflib

    # Use SequenceMatcher to compute similarity ratio
    user_normalized = _normalize_whitespace(user_content)
    template_normalized = _normalize_whitespace(template_content)

    # Replace placeholders in template with user's likely values for better matching
    import re
    # Find placeholders and their approximate positions
    for match in re.finditer(r"\[\[([A-Z_]+)\]\]", template_normalized):
        # Replace with a generic marker for comparison
        template_normalized = template_normalized.replace(
            match.group(0), "PLACEHOLDER_VALUE"
        )

    ratio = difflib.SequenceMatcher(
        None, user_normalized, template_normalized
    ).ratio()

    return ratio >= threshold


# New prompt strategy: Instead of asking AI to merge (which fails),
# we ask it to ONLY identify new sections to append.
# This is much safer - user content is never touched.

EXTRACT_NEW_SECTIONS_SYSTEM = """\
You analyze template files to find NEW sections that don't exist in a user's file.

Your ONLY job is to identify genuinely NEW content from the template that should
be APPENDED to the user's file. You must NEVER modify, summarize, or replace
any existing user content.

Rules:
1. Compare section headers between user's file and template
2. A section is "new" ONLY if no similar header exists in the user's file
3. Ignore sections that exist in user's file even if content differs
4. Ignore cosmetic differences (formatting, wording, examples)
5. Output ONLY the new sections to append, or "NONE" if nothing new

Response format:
```sections
[new sections to append, preserving their exact template formatting]
```
```summary
- [what new sections were found, or "No new sections"]
```

If there are no genuinely new sections, output:
```sections
NONE
```
```summary
- No new sections found in template
```"""

EXTRACT_NEW_SECTIONS_USER = """Find NEW sections in the template that don't exist
in the user's file.

## User's Current File (DO NOT MODIFY - only check what sections exist):
```
{user_content}
```

## Template (find NEW sections from this):
```
{template_content}
```

## File: {filename}

List the section headers in each file, then output any genuinely NEW sections
from the template that should be appended to the user's file."""

# Keep old prompt for backwards compatibility but mark as deprecated
MERGE_SYSTEM_PROMPT = EXTRACT_NEW_SECTIONS_SYSTEM


MERGE_USER_PROMPT = """Please merge these two versions of a file.

## User's Current Version (preserve their customizations):
```
{user_content}
```

## New Template Version (add new features from this):
```
{template_content}
```

## File Context:
- Filename: {filename}

Analyze what the user has customized vs what is boilerplate, then output the merged
content and brief summary in the specified format."""


def get_anthropic_client(interactive: bool = True):
    """Get Anthropic client, prompting for key if needed.

    Args:
        interactive: If True, prompt user for API key if not set.

    Returns:
        Configured Anthropic client.

    Raises:
        ImportError: If anthropic package not installed.
        ValueError: If API key not available.
    """
    try:
        import anthropic
    except ImportError:
        raise ImportError(
            "anthropic package required for AI merge.\n"
            "Install with: uv tool install echograph[ai]"
        )

    from echograph_cli.core.config import get_api_key, prompt_for_api_key

    if interactive:
        api_key = prompt_for_api_key(
            key_name="anthropic_api_key",
            service_name="Anthropic",
            console_url="https://console.anthropic.com/",
        )
    else:
        api_key = get_api_key("anthropic_api_key")

    if not api_key:
        raise ValueError(
            "Anthropic API key required for AI merge.\n"
            "Set with: export ANTHROPIC_API_KEY=your-key\n"
            "Or run interactively to be prompted."
        )

    return anthropic.Anthropic(api_key=api_key)


def detect_file_type(filename: str) -> str:
    """Detect file type for context in AI prompt."""
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

    type_map = {
        "md": "Markdown documentation",
        "yaml": "YAML configuration",
        "yml": "YAML configuration",
        "json": "JSON configuration",
        "toml": "TOML configuration",
        "py": "Python source code",
        "js": "JavaScript source code",
        "ts": "TypeScript source code",
        "txt": "Plain text",
    }

    return type_map.get(ext, f"Configuration file ({ext})")


def _parse_sections_response(response_text: str) -> tuple[str | None, str]:
    """Parse the new sections and summary from AI response.

    Expected format:
    ```sections
    [new sections or NONE]
    ```
    ```summary
    [summary]
    ```

    Returns:
        Tuple of (new_sections or None if NONE, explanation)
    """
    import re

    # Extract sections content
    sections_match = re.search(r"```sections\n(.*?)```", response_text, re.DOTALL)
    if sections_match:
        sections_content = sections_match.group(1).strip()
        # Check if AI said there are no new sections
        if sections_content.upper() == "NONE" or not sections_content:
            sections_content = None
    else:
        # Fallback: try to find any code block
        code_match = re.search(r"```(?:\w+)?\n(.*?)```", response_text, re.DOTALL)
        if code_match:
            content = code_match.group(1).strip()
            sections_content = None if content.upper() == "NONE" else content
        else:
            sections_content = None

    # Extract summary
    summary_match = re.search(r"```summary\n(.*?)```", response_text, re.DOTALL)
    if summary_match:
        explanation = summary_match.group(1).strip()
    else:
        if sections_content:
            explanation = "Found new sections to append"
        else:
            explanation = "No new sections found in template"

    return sections_content, explanation


# Keep old parser for backwards compatibility
def _parse_merge_response(response_text: str) -> tuple[str, str]:
    """Parse merged content - now delegates to sections parser."""
    sections, explanation = _parse_sections_response(response_text)
    return sections or "", explanation


def ai_extract_new_sections(
    user_content: str,
    template_content: str,
    filename: str,
) -> tuple[str | None, str]:
    """Use Claude to identify NEW sections in template not in user's file.

    This is safer than asking AI to merge - it only extracts new content
    to append, never modifying user's existing content.

    Args:
        user_content: User's current file content
        template_content: New template content
        filename: Name of the file being merged

    Returns:
        Tuple of (new_sections_to_append or None, explanation)
    """
    client = get_anthropic_client()

    user_prompt = EXTRACT_NEW_SECTIONS_USER.format(
        user_content=user_content,
        template_content=template_content,
        filename=filename,
    )

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=8192,
        system=EXTRACT_NEW_SECTIONS_SYSTEM,
        messages=[{"role": "user", "content": user_prompt}],
    )

    return _parse_sections_response(response.content[0].text)


def ai_merge_content(
    user_content: str,
    template_content: str,
    filename: str,
) -> tuple[str, str]:
    """Extract new sections and append to user content.

    Uses the safer 'extract new sections' approach instead of full merge.
    User content is NEVER modified - only new sections are appended.

    Args:
        user_content: User's current file content
        template_content: New template content
        filename: Name of the file being merged

    Returns:
        Tuple of (merged_content, explanation)
    """
    new_sections, explanation = ai_extract_new_sections(
        user_content, template_content, filename
    )

    if new_sections is None:
        # No new sections - return user content unchanged
        return user_content, explanation

    # Append new sections to user content
    # Ensure proper spacing between existing content and new sections
    user_stripped = user_content.rstrip()
    merged = f"{user_stripped}\n\n{new_sections}\n"

    return merged, explanation


def smart_merge_file(
    user_content: str,
    template_content: str,
    filename: str,
    console: Console,
    auto_approve: bool = False,
) -> AIMergeResult:
    """Perform smart merge with preview and approval flow.

    For markdown files, uses section-level merge first.
    For other files or when sections conflict, uses AI merge.

    Args:
        user_content: User's current file content
        template_content: New template content
        filename: Name of the file being merged
        console: Rich console for output
        auto_approve: If True, skip confirmation prompt

    Returns:
        AIMergeResult with merged content and metadata

    Raises:
        typer.Exit: If user presses Ctrl+C to abort
    """
    import typer

    # Check for interrupt before any processing
    try:
        # Skip if only whitespace differences
        if is_whitespace_only_diff(user_content, template_content):
            console.print(
                f"[dim]Skipping {filename} - whitespace differences only[/dim]"
            )
            return AIMergeResult(
                merged_content=user_content,
                explanation="Skipped - only whitespace differences",
                had_conflicts=False,
                user_approved=True,
                was_skipped_whitespace=True,
            )

        # Skip if user's file is just the template with placeholders filled in
        if is_placeholder_only_diff(user_content, template_content):
            console.print(
                f"[dim]Skipping {filename} - placeholder substitutions only[/dim]"
            )
            return AIMergeResult(
                merged_content=user_content,
                explanation="Skipped - template with placeholders filled",
                had_conflicts=False,
                user_approved=True,
                was_skipped_whitespace=True,
            )

        # Skip if files are >95% similar
        if is_high_similarity(user_content, template_content):
            console.print(
                f"[dim]Skipping {filename} - files nearly identical[/dim]"
            )
            return AIMergeResult(
                merged_content=user_content,
                explanation="Skipped - files are >95% similar, keeping user version",
                had_conflicts=False,
                user_approved=True,
                was_skipped_whitespace=True,
            )
    except KeyboardInterrupt:
        console.print("\n[yellow]Aborted by user[/yellow]")
        raise typer.Exit(1)

    is_markdown = filename.endswith(".md")

    # For markdown, try section-level merge first
    if is_markdown:
        try:
            merged, conflicts = three_way_merge_sections(
                "",  # No base version
                user_content,
                template_content,
                ConflictMarkerStyle.HTML_COMMENT,
            )
        except KeyboardInterrupt:
            console.print("\n[yellow]Aborted by user[/yellow]")
            raise typer.Exit(1)

        if not conflicts:
            # Clean merge - no AI needed
            # But still check if merged content is different from user's content
            if is_whitespace_only_diff(user_content, merged):
                console.print(f"[dim]Skipping {filename} - no changes needed[/dim]")
                return AIMergeResult(
                    merged_content=user_content,
                    explanation="No changes needed",
                    had_conflicts=False,
                    user_approved=True,
                    was_skipped_whitespace=True,
                )

            # Show diff and ask for approval
            console.print(f"\n[bold cyan]Section Merge Preview: {filename}[/bold cyan]")
            print_unified_diff(user_content, merged, filename)
            console.print("\n[dim]Section-level merge: No conflicts detected[/dim]")

            if auto_approve:
                return AIMergeResult(
                    merged_content=merged,
                    explanation="Section-level merge: No conflicts detected",
                    had_conflicts=False,
                    user_approved=True,
                )

            # Ask for approval
            console.print("\n[bold]Accept this merge?[/bold]")
            console.print("  \\[y] Yes, apply merge")
            console.print("  \\[n] No, keep original")

            try:
                choice = typer.prompt("Choose", default="y").lower()
            except (KeyboardInterrupt, EOFError):
                console.print("\n[yellow]Aborted by user[/yellow]")
                raise typer.Exit(1)

            if choice == "y":
                return AIMergeResult(
                    merged_content=merged,
                    explanation="Section-level merge: No conflicts detected",
                    had_conflicts=False,
                    user_approved=True,
                )
            else:
                return AIMergeResult(
                    merged_content=user_content,
                    explanation="User declined - kept original",
                    had_conflicts=False,
                    user_approved=False,
                )

        # Has conflicts - use AI to resolve
        console.print(
            f"[yellow]Found {len(conflicts)} section conflict(s) - "
            f"using AI to resolve[/yellow]"
        )

    # Use AI merge with spinner
    merged_content = ""
    explanation = ""

    with Status(
        f"[cyan]Analyzing {filename}... (you'll review before any changes)[/cyan]",
        console=console,
        spinner="dots",
    ) as status:
        try:
            merged_content, explanation = ai_merge_content(
                user_content,
                template_content,
                filename,
            )
        except KeyboardInterrupt:
            status.stop()
            console.print("\n[yellow]Aborted by user[/yellow]")
            raise typer.Exit(1)
        except ImportError as e:
            status.stop()
            console.print(f"[red]{e}[/red]")
            return AIMergeResult(
                merged_content=user_content,
                explanation="AI merge unavailable - kept original",
                had_conflicts=True,
                user_approved=False,
            )
        except ValueError as e:
            status.stop()
            console.print(f"[red]{e}[/red]")
            return AIMergeResult(
                merged_content=user_content,
                explanation="AI merge unavailable - kept original",
                had_conflicts=True,
                user_approved=False,
            )
        except Exception as e:
            status.stop()
            console.print(f"[red]AI merge failed: {e}[/red]")
            return AIMergeResult(
                merged_content=user_content,
                explanation=f"AI merge failed: {e}",
                had_conflicts=True,
                user_approved=False,
            )

    # Check if AI merge result only differs in whitespace
    if is_whitespace_only_diff(user_content, merged_content):
        console.print(
            f"[dim]Skipping {filename} - AI found whitespace only[/dim]"
        )
        return AIMergeResult(
            merged_content=user_content,
            explanation="Skipped - only whitespace differences after AI analysis",
            had_conflicts=False,
            user_approved=True,
            was_skipped_whitespace=True,
        )

    # Validate AI didn't remove significant content (common failure mode)
    user_lines = len(user_content.splitlines())
    merged_lines = len(merged_content.splitlines())
    reduction_ratio = merged_lines / user_lines if user_lines > 0 else 1.0

    if reduction_ratio < 0.8:  # More than 20% reduction
        console.print(
            f"\n[bold red]Warning: AI merge validation failed for {filename}[/bold red]"
        )
        reduction_pct = (1 - reduction_ratio) * 100
        console.print(
            f"[red]AI removed significant content: "
            f"{user_lines} -> {merged_lines} lines "
            f"({reduction_pct:.0f}% reduction)[/red]"
        )
        console.print(
            "[yellow]This usually means the AI ignored "
            "the preservation instructions.[/yellow]"
        )
        console.print("[dim]Keeping your original file unchanged.[/dim]")
        return AIMergeResult(
            merged_content=user_content,
            explanation=f"Rejected - AI removed {reduction_pct:.0f}% of content",
            had_conflicts=True,
            user_approved=False,
        )

    # Show diff preview
    console.print(f"\n[bold cyan]AI Merge Preview: {filename}[/bold cyan]")
    print_unified_diff(user_content, merged_content, filename)

    console.print(f"\n[dim]{explanation}[/dim]")

    if auto_approve:
        return AIMergeResult(
            merged_content=merged_content,
            explanation=explanation,
            had_conflicts=False,
            user_approved=True,
        )

    # Ask for approval
    console.print("\n[bold]Accept this merge?[/bold]")
    console.print("  \\[y] Yes, apply merge")
    console.print("  \\[n] No, keep original")
    console.print("  \\[e] Edit (save with conflict markers)")

    try:
        choice = typer.prompt("Choose", default="y").lower()
    except (KeyboardInterrupt, EOFError):
        console.print("\n[yellow]Aborted by user[/yellow]")
        raise typer.Exit(1)

    if choice == "y":
        return AIMergeResult(
            merged_content=merged_content,
            explanation=explanation,
            had_conflicts=False,
            user_approved=True,
        )
    elif choice == "e":
        # Add conflict markers for manual editing
        marked_content = _add_conflict_markers(user_content, merged_content, filename)
        return AIMergeResult(
            merged_content=marked_content,
            explanation="Saved with conflict markers for manual editing",
            had_conflicts=True,
            user_approved=True,
        )
    else:
        return AIMergeResult(
            merged_content=user_content,
            explanation="User declined - kept original",
            had_conflicts=False,
            user_approved=False,
        )


def _add_conflict_markers(
    original: str,
    ai_merged: str,
    filename: str,
) -> str:
    """Add conflict markers for manual resolution."""
    is_markdown = filename.endswith(".md")

    if is_markdown:
        return (
            f"<!-- YOUR ORIGINAL VERSION -->\n"
            f"<!--\n{original}\n-->\n\n"
            f"<!-- AI MERGED VERSION (review and edit below) -->\n"
            f"{ai_merged}\n"
        )
    else:
        return (
            f"<<<<<<< YOUR VERSION\n"
            f"{original}\n"
            f"=======\n"
            f"{ai_merged}\n"
            f">>>>>>> AI MERGED\n"
        )


def batch_smart_merge(
    files: list[tuple[str, str, str]],  # (filename, user_content, template_content)
    console: Console,
    auto_approve: bool = False,
) -> dict[str, AIMergeResult]:
    """Batch process multiple files with smart merge.

    Args:
        files: List of (filename, user_content, template_content) tuples
        console: Rich console for output
        auto_approve: If True, skip all confirmation prompts

    Returns:
        Dict mapping filename to AIMergeResult
    """
    results: dict[str, AIMergeResult] = {}

    for i, (filename, user_content, template_content) in enumerate(files, 1):
        console.print(f"\n[dim]Processing {i}/{len(files)}: {filename}[/dim]")

        result = smart_merge_file(
            user_content=user_content,
            template_content=template_content,
            filename=filename,
            console=console,
            auto_approve=auto_approve,
        )

        results[filename] = result

        if result.user_approved:
            console.print(f"[green]Merged: {filename}[/green]")
        else:
            console.print(f"[yellow]Skipped: {filename}[/yellow]")

    return results
