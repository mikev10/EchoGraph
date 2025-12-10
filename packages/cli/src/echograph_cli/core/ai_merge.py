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


MERGE_SYSTEM_PROMPT = """\
You are an expert at merging configuration and documentation files.

Your task is to intelligently merge a user's customized file with a new template version.

CRITICAL RULE: The user's version is ALWAYS more important than the template.
- If the user has MORE content than the template, KEEP all the user's content
- If the user has DIFFERENT content than the template, KEEP the user's version
- The template only provides NEW sections or features the user doesn't have yet
- NEVER remove or shorten user content to match a simpler template

Key principles:
1. PRESERVE all user content - their version represents intentional customizations
2. ADD new sections from template that don't exist in user's version
3. KEEP user's specific values, examples, project names, expanded explanations
4. Only UPDATE generic boilerplate IF the template has genuinely NEW functionality
5. MAINTAIN the user's structure and formatting preferences

What to KEEP from user's version:
- All custom project names, paths, URLs, examples
- All expanded or reworded explanations (even if template is shorter)
- All custom sections not in template
- User's task lists, code examples, specific instructions
- ANY content that is more detailed than the template

What to ADD from template:
- Genuinely NEW sections that don't exist in user's version
- NEW features or capabilities not present in user's file
- Critical fixes or corrections (rare)

What to NEVER do:
- Remove user content because template doesn't have it
- Replace detailed user examples with generic template placeholders
- Shorten user's expanded explanations
- Treat template examples as "correct" when user has real content

Response format - output EXACTLY this structure:
```merged
[the complete merged file content]
```
```summary
- [1-2 concise bullet points: what was preserved, what was added]
```

Do not include any other text outside these code blocks."""


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

Analyze what the user has customized vs what is boilerplate, then output the merged content and brief summary in the specified format."""


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


def _parse_merge_response(response_text: str) -> tuple[str, str]:
    """Parse the merged content and summary from AI response.

    Expected format:
    ```merged
    [content]
    ```
    ```summary
    [summary]
    ```
    """
    import re

    # Extract merged content
    merged_match = re.search(r"```merged\n(.*?)```", response_text, re.DOTALL)
    if merged_match:
        merged_content = merged_match.group(1).strip()
    else:
        # Fallback: try to find any code block or use full response
        code_match = re.search(r"```(?:\w+)?\n(.*?)```", response_text, re.DOTALL)
        if code_match:
            merged_content = code_match.group(1).strip()
        else:
            merged_content = response_text.strip()

    # Extract summary
    summary_match = re.search(r"```summary\n(.*?)```", response_text, re.DOTALL)
    if summary_match:
        explanation = summary_match.group(1).strip()
    else:
        explanation = "Merged user customizations with template updates"

    return merged_content, explanation


def ai_merge_content(
    user_content: str,
    template_content: str,
    filename: str,
) -> tuple[str, str]:
    """Use Claude to intelligently merge user content with template.

    Args:
        user_content: User's current file content
        template_content: New template content
        filename: Name of the file being merged

    Returns:
        Tuple of (merged_content, explanation)
    """
    client = get_anthropic_client()

    user_prompt = MERGE_USER_PROMPT.format(
        user_content=user_content,
        template_content=template_content,
        filename=filename,
    )

    # Single API call - Haiku is faster for simple merge tasks
    response = client.messages.create(
        model="claude-3-5-haiku-20241022",
        max_tokens=8192,
        system=MERGE_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    )

    return _parse_merge_response(response.content[0].text)


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
    """
    # Skip if only whitespace differences
    if is_whitespace_only_diff(user_content, template_content):
        console.print(f"[dim]Skipping {filename} - only whitespace differences[/dim]")
        return AIMergeResult(
            merged_content=user_content,
            explanation="Skipped - only whitespace differences",
            had_conflicts=False,
            user_approved=True,
            was_skipped_whitespace=True,
        )

    # Skip if user's file is just the template with placeholders filled in
    if is_placeholder_only_diff(user_content, template_content):
        console.print(f"[dim]Skipping {filename} - only placeholder substitutions[/dim]")
        return AIMergeResult(
            merged_content=user_content,
            explanation="Skipped - user file matches template with placeholders filled",
            had_conflicts=False,
            user_approved=True,
            was_skipped_whitespace=True,
        )

    is_markdown = filename.endswith(".md")

    # For markdown, try section-level merge first
    if is_markdown:
        merged, conflicts = three_way_merge_sections(
            "",  # No base version
            user_content,
            template_content,
            ConflictMarkerStyle.HTML_COMMENT,
        )

        if not conflicts:
            # Clean merge - no AI needed
            return AIMergeResult(
                merged_content=merged,
                explanation="Section-level merge: No conflicts detected",
                had_conflicts=False,
                user_approved=True,
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
            import typer
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
            f"[dim]Skipping {filename} - AI merge found only whitespace differences[/dim]"
        )
        return AIMergeResult(
            merged_content=user_content,
            explanation="Skipped - only whitespace differences after AI analysis",
            had_conflicts=False,
            user_approved=True,
            was_skipped_whitespace=True,
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

    import typer

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
