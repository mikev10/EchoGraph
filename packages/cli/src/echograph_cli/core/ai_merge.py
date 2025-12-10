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
    and collapses multiple blank lines into one.
    """
    lines = content.replace("\r\n", "\n").split("\n")
    # Strip trailing whitespace from each line
    lines = [line.rstrip() for line in lines]
    # Join and collapse multiple blank lines
    text = "\n".join(lines)
    while "\n\n\n" in text:
        text = text.replace("\n\n\n", "\n\n")
    return text.strip()


def is_whitespace_only_diff(content1: str, content2: str) -> bool:
    """Check if two contents differ only in whitespace.

    Returns True if the only differences are:
    - Trailing whitespace on lines
    - Number of blank lines between sections
    - Line ending differences (CRLF vs LF)
    """
    return _normalize_whitespace(content1) == _normalize_whitespace(content2)


MERGE_SYSTEM_PROMPT = """\
You are an expert at merging configuration and documentation files.

Your task is to intelligently merge a user's customized file with a new \
template version.

Key principles:
1. PRESERVE user customizations - these represent intentional changes
2. ADD new features from the template that don't exist in the user's version
3. KEEP user's specific values (project names, paths, custom sections)
4. UPDATE boilerplate/generic text with improved template versions
5. MAINTAIN the overall structure and formatting

When identifying what to keep vs update:
- Custom project names, paths, URLs = KEEP user's version
- Custom sections not in template = KEEP entirely
- Generic instructions that were improved = USE template version
- User's reworded/expanded explanations = KEEP user's version
- New sections in template = ADD to result
- Deprecated sections removed from template = KEEP if user has content"""


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
- File type: {file_type}

## Instructions:
1. Analyze what the user has customized vs what is boilerplate
2. Merge intelligently, preserving user intent while adding new template features
3. Output ONLY the merged file content, nothing else
4. Do not add any explanatory comments or markers
5. Maintain proper formatting and structure"""


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
    file_type = detect_file_type(filename)

    user_prompt = MERGE_USER_PROMPT.format(
        user_content=user_content,
        template_content=template_content,
        filename=filename,
        file_type=file_type,
    )

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=8192,
        system=MERGE_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    )

    merged_content = response.content[0].text

    # Generate brief explanation
    explain_prompt = """In 2-3 bullet points, summarize what was merged:
- What user customizations were preserved?
- What new template features were added?
- Any sections that were updated?

Be very brief, max 3 lines total."""

    explain_response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=256,
        messages=[
            {"role": "user", "content": user_prompt},
            {"role": "assistant", "content": merged_content},
            {"role": "user", "content": explain_prompt},
        ],
    )

    explanation = explain_response.content[0].text

    return merged_content, explanation


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
            raise
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
    except KeyboardInterrupt:
        console.print("\n[yellow]Aborted by user[/yellow]")
        raise

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
