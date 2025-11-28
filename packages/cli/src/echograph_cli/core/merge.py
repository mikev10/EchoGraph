"""Three-way merge for template updates."""

import difflib

from echograph_cli.core.models import MergeConflict


def three_way_merge(
    base: str,
    user: str,
    new: str,
) -> tuple[str, list[MergeConflict]]:
    """Perform three-way merge preserving user customizations.

    Args:
        base: Original template content (from previous version)
        user: User's modified version
        new: New template version

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
                merged_lines.append("<<<<<<< YOUR CHANGES\n")
                merged_lines.extend(user_lines[u_j1:u_j2])
                merged_lines.append("=======\n")
                merged_lines.extend(new_lines[n_j1:n_j2])
                merged_lines.append(">>>>>>> NEW TEMPLATE\n")

            i = max(u_i2, n_i2)

    return "".join(merged_lines), conflicts
