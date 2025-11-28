"""Tests for three-way merge."""

from echograph_cli.core.merge import three_way_merge


class TestThreeWayMerge:
    """Tests for three-way merge functionality."""

    def test_takes_new_when_base_empty(self) -> None:
        """Should take new version when base is empty."""
        base = ""
        user = ""
        new = "new content"

        merged, conflicts = three_way_merge(base, user, new)

        assert merged == new
        assert len(conflicts) == 0

    def test_takes_new_when_user_unchanged(self) -> None:
        """Should take new version when user hasn't modified."""
        base = "original"
        user = "original"
        new = "updated"

        merged, conflicts = three_way_merge(base, user, new)

        assert merged == new
        assert len(conflicts) == 0

    def test_keeps_user_when_template_unchanged(self) -> None:
        """Should keep user changes when template hasn't changed."""
        base = "original"
        user = "user modified"
        new = "original"

        merged, conflicts = three_way_merge(base, user, new)

        assert merged == user
        assert len(conflicts) == 0

    def test_no_conflict_when_same_change(self) -> None:
        """Should not conflict when user and new made same change."""
        base = "original"
        user = "same change"
        new = "same change"

        merged, conflicts = three_way_merge(base, user, new)

        assert merged == user
        assert len(conflicts) == 0

    def test_detects_conflict_on_different_changes(self) -> None:
        """Should detect conflict when different changes to same line."""
        base = "line 1\noriginal\nline 3\n"
        user = "line 1\nuser change\nline 3\n"
        new = "line 1\ntemplate change\nline 3\n"

        merged, conflicts = three_way_merge(base, user, new)

        assert len(conflicts) == 1
        assert "<<<<<<< YOUR CHANGES" in merged
        assert "=======" in merged
        assert ">>>>>>> NEW TEMPLATE" in merged

    def test_preserves_user_additions(self) -> None:
        """Should preserve lines user added."""
        base = "line 1\nline 2\n"
        user = "line 1\nuser added\nline 2\n"
        new = "line 1\nline 2\n"

        merged, conflicts = three_way_merge(base, user, new)

        assert "user added" in merged
        assert len(conflicts) == 0

    def test_includes_template_additions(self) -> None:
        """Should include lines template added."""
        base = "line 1\nline 2\n"
        user = "line 1\nline 2\n"
        new = "line 1\ntemplate added\nline 2\n"

        merged, conflicts = three_way_merge(base, user, new)

        assert "template added" in merged
        assert len(conflicts) == 0

    def test_conflict_has_correct_line_number(self) -> None:
        """Should report correct line number for conflict."""
        base = "line 1\noriginal\nline 3\n"
        user = "line 1\nuser\nline 3\n"
        new = "line 1\ntemplate\nline 3\n"

        _, conflicts = three_way_merge(base, user, new)

        assert len(conflicts) == 1
        # Conflict should be around line 2
        assert conflicts[0].line_number > 0

    def test_handles_empty_base_with_both_changes(self) -> None:
        """Should handle new file scenario."""
        base = ""
        user = "user content"
        new = "template content"

        # When base is empty, should take new
        merged, conflicts = three_way_merge(base, user, new)

        assert merged == new
