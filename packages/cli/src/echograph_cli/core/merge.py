"""Three-way merge for template updates."""

import difflib
import re
from enum import Enum

from echograph_cli.core.models import MergeConflict, SectionConflict


class ConflictMarkerStyle(Enum):
    """Style for conflict markers in merged output."""

    GIT = "git"  # <<<<<<< / ======= / >>>>>>>
    HTML_COMMENT = "html"  # <!-- CONFLICT: ... -->


def get_conflict_markers(style: ConflictMarkerStyle) -> tuple[str, str, str]:
    """Return (start, separator, end) markers for given style.

    Args:
        style: The conflict marker style to use

    Returns:
        Tuple of (start_marker, separator, end_marker)
    """
    if style == ConflictMarkerStyle.HTML_COMMENT:
        return (
            "<!-- CONFLICT: YOUR VERSION -->\n",
            "<!-- CONFLICT: NEW TEMPLATE -->\n",
            "<!-- CONFLICT END -->\n",
        )
    # Default to GIT style
    return (
        "<<<<<<< YOUR CHANGES\n",
        "=======\n",
        ">>>>>>> NEW TEMPLATE\n",
    )


def three_way_merge(
    base: str,
    user: str,
    new: str,
    marker_style: ConflictMarkerStyle = ConflictMarkerStyle.GIT,
) -> tuple[str, list[MergeConflict]]:
    """Perform three-way merge preserving user customizations.

    Args:
        base: Original template content (from previous version)
        user: User's modified version
        new: New template version
        marker_style: Style for conflict markers (default: GIT)

    Returns:
        Tuple of (merged_content, list_of_conflicts)
    """
    # If base is empty, this is a new file - take new version
    if not base:
        return new, []

    # If user hasn't changed from base, take new version
    if user == base:
        return new, []

    # If new hasn't changed from base, keep user version
    if new == base:
        return user, []

    # If user and new are the same, no conflict
    if user == new:
        return user, []

    # Perform line-by-line merge
    base_lines = base.splitlines(keepends=True)
    user_lines = user.splitlines(keepends=True)
    new_lines = new.splitlines(keepends=True)

    conflicts: list[MergeConflict] = []
    merged_lines: list[str] = []

    # Use SequenceMatcher to find differences
    user_matcher = difflib.SequenceMatcher(None, base_lines, user_lines)
    new_matcher = difflib.SequenceMatcher(None, base_lines, new_lines)

    # Build change maps
    user_changes: dict[int, tuple[str, int, int, int, int]] = {}
    for op in user_matcher.get_opcodes():
        if op[0] != "equal":
            user_changes[op[1]] = op

    new_changes: dict[int, tuple[str, int, int, int, int]] = {}
    for op in new_matcher.get_opcodes():
        if op[0] != "equal":
            new_changes[op[1]] = op

    i = 0
    while i < len(base_lines):
        user_op = user_changes.get(i)
        new_op = new_changes.get(i)

        if user_op is None and new_op is None:
            # No changes at this position
            merged_lines.append(base_lines[i])
            i += 1
        elif user_op is None and new_op is not None:
            # Only new template changed
            _, i1, i2, j1, j2 = new_op
            merged_lines.extend(new_lines[j1:j2])
            i = i2
        elif user_op is not None and new_op is None:
            # Only user changed - preserve their changes
            _, i1, i2, j1, j2 = user_op
            merged_lines.extend(user_lines[j1:j2])
            i = i2
        else:
            # Both changed - check if same change or conflict
            assert user_op is not None and new_op is not None
            _, u_i1, u_i2, u_j1, u_j2 = user_op
            _, n_i1, n_i2, n_j1, n_j2 = new_op

            user_content = "".join(user_lines[u_j1:u_j2])
            new_content = "".join(new_lines[n_j1:n_j2])

            if user_content == new_content:
                # Same change - use either
                merged_lines.extend(user_lines[u_j1:u_j2])
            else:
                # Conflict - add markers
                conflict = MergeConflict(
                    line_number=len(merged_lines) + 1,
                    base_content="".join(base_lines[u_i1:u_i2]),
                    user_content=user_content,
                    new_content=new_content,
                )
                conflicts.append(conflict)

                # Add conflict markers
                start, sep, end = get_conflict_markers(marker_style)
                merged_lines.append(start)
                merged_lines.extend(user_lines[u_j1:u_j2])
                merged_lines.append(sep)
                merged_lines.extend(new_lines[n_j1:n_j2])
                merged_lines.append(end)

            i = max(u_i2, n_i2)

    return "".join(merged_lines), conflicts


def parse_markdown_sections(content: str) -> dict[str, str]:
    """Parse markdown into sections by ## headers.

    Args:
        content: Markdown content

    Returns:
        Dict mapping section titles to their content (including header)
    """
    sections: dict[str, str] = {}

    # Split by ## headers, keeping the delimiter
    pattern = r"(^## .+$)"
    parts = re.split(pattern, content, flags=re.MULTILINE)

    # First part before any ## header
    if parts[0].strip():
        sections["_preamble"] = parts[0]

    # Process header/content pairs
    for i in range(1, len(parts), 2):
        if i + 1 < len(parts):
            header = parts[i].strip()
            section_content = parts[i + 1]
            # Extract section title without ##
            title = header.replace("## ", "").strip()
            sections[title] = header + "\n" + section_content
        elif parts[i].strip():
            # Header without content
            header = parts[i].strip()
            title = header.replace("## ", "").strip()
            sections[title] = header + "\n"

    return sections


def three_way_merge_sections(
    base: str,
    user: str,
    new: str,
    marker_style: ConflictMarkerStyle = ConflictMarkerStyle.HTML_COMMENT,
) -> tuple[str, list[SectionConflict]]:
    """Three-way merge at section level for markdown files.

    Parses markdown by ## headers and merges sections intelligently:
    - Sections only in user are preserved
    - Sections only in new template are added
    - Identical sections are kept as-is
    - Modified sections are merged or marked as conflicts

    Args:
        base: Original template content (from previous version)
        user: User's current version
        new: New template version
        marker_style: Style for conflict markers (default: HTML_COMMENT)

    Returns:
        Tuple of (merged_content, list_of_section_conflicts)
    """
    base_sections = parse_markdown_sections(base) if base else {}
    user_sections = parse_markdown_sections(user)
    new_sections = parse_markdown_sections(new)

    conflicts: list[SectionConflict] = []
    result_parts: list[str] = []

    # Track which sections we've processed
    processed_sections: set[str] = set()

    # Helper to normalize section titles for comparison
    def normalize_title(title: str) -> str:
        return re.sub(r"[^\w\s]", "", title).lower().strip()

    # Build a map of normalized titles to actual titles
    new_title_map = {normalize_title(t): t for t in new_sections}
    base_title_map = {normalize_title(t): t for t in base_sections}

    # Process user's sections first (preserve their order)
    for user_title, user_content in user_sections.items():
        if user_title == "_preamble":
            result_parts.append(user_content)
            processed_sections.add("_preamble")
            continue

        normalized = normalize_title(user_title)
        processed_sections.add(normalized)

        # Check if section exists in new template
        if normalized in new_title_map:
            new_title = new_title_map[normalized]
            new_content = new_sections[new_title]

            # Check base for three-way comparison
            base_content = ""
            if normalized in base_title_map:
                base_title = base_title_map[normalized]
                base_content = base_sections[base_title]

            # Determine how to handle this section
            if user_content == new_content:
                # Same content - keep either
                result_parts.append(user_content)
            elif user_content == base_content:
                # User didn't change from base - take new version
                result_parts.append(new_content)
            elif new_content == base_content:
                # New template didn't change from base - keep user version
                result_parts.append(user_content)
            else:
                # Both changed differently - this is a conflict
                conflict = SectionConflict(
                    section_title=user_title,
                    base_content=base_content,
                    user_content=user_content,
                    new_content=new_content,
                )
                conflicts.append(conflict)

                # Add with conflict markers
                start, sep, end = get_conflict_markers(marker_style)
                result_parts.append(
                    f"{start}{user_content.rstrip()}\n{sep}{new_content.rstrip()}\n{end}"
                )
        else:
            # Section only in user - keep it
            result_parts.append(user_content)

    # Add new sections that don't exist in user's file
    for new_title, new_content in new_sections.items():
        if new_title == "_preamble":
            continue

        normalized = normalize_title(new_title)
        if normalized not in processed_sections:
            # New section - add it
            result_parts.append(new_content)

    # Join with proper spacing
    merged = ""
    for i, part in enumerate(result_parts):
        if i == 0:
            merged = part.rstrip()
        else:
            merged += "\n\n" + part.rstrip()

    return merged + "\n", conflicts


def merge_claude_md_sections(
    existing: str,
    template: str,
) -> tuple[str, list[str]]:
    """Merge template sections into existing CLAUDE.md.

    Only adds sections that don't exist in the user's file.
    Never overwrites existing sections.

    Args:
        existing: User's existing CLAUDE.md content
        template: Template CLAUDE.md content

    Returns:
        Tuple of (merged_content, list_of_added_section_names)
    """
    existing_sections = parse_markdown_sections(existing)
    template_sections = parse_markdown_sections(template)

    added_sections: list[str] = []
    result_parts: list[str] = []

    # Start with existing content
    result_parts.append(existing.rstrip())

    # Find sections in template that don't exist in user's file
    for title, content in template_sections.items():
        if title == "_preamble":
            continue

        # Check if section exists (case-insensitive, ignore emojis)
        title_normalized = re.sub(r"[^\w\s]", "", title).lower().strip()
        exists = False

        for existing_title in existing_sections:
            existing_normalized = re.sub(r"[^\w\s]", "", existing_title).lower().strip()
            if title_normalized == existing_normalized:
                exists = True
                break

        if not exists:
            added_sections.append(title)
            result_parts.append("\n\n" + content.rstrip())

    return "\n".join(result_parts) + "\n", added_sections
