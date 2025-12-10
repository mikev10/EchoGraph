"""Interactive merge workflow with session persistence."""

import json
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path

from rich.console import Console
from rich.prompt import Confirm, Prompt

from echograph_cli.core.merge import (
    ConflictMarkerStyle,
    three_way_merge,
    three_way_merge_sections,
)
from echograph_cli.core.models import MergeSession, SectionConflict
from echograph_cli.output import print_three_panel_merge, print_unified_diff

MERGE_SESSION_FILE = ".claude/.merge-in-progress.json"


class InteractiveMerger:
    """Main class for interactive merge workflow.

    Handles:
    - Interactive conflict resolution with visual diff and three-panel view
    - Session persistence for resuming interrupted merges
    - Section-level merge for markdown files
    """

    def __init__(self, console: Console, target_dir: Path):
        """Initialize the interactive merger.

        Args:
            console: Rich console for output
            target_dir: Target directory for the project
        """
        self.console = console
        self.target_dir = target_dir
        self.session: MergeSession | None = None

    def check_for_existing_session(self) -> bool:
        """Check if there's an interrupted merge session to resume.

        Returns:
            True if a session file exists, False otherwise
        """
        session_file = self.target_dir / MERGE_SESSION_FILE
        if session_file.exists():
            try:
                with open(session_file, encoding="utf-8") as f:
                    data = json.load(f)
                self.session = MergeSession(**data)
                return True
            except (json.JSONDecodeError, TypeError, KeyError):
                # Invalid session file - ignore it
                return False
        return False

    def save_session(self) -> None:
        """Save current session state for resume."""
        if self.session:
            session_file = self.target_dir / MERGE_SESSION_FILE
            session_file.parent.mkdir(parents=True, exist_ok=True)
            with open(session_file, "w", encoding="utf-8") as f:
                json.dump(asdict(self.session), f, indent=2)

    def clear_session(self) -> None:
        """Remove session file after successful completion."""
        session_file = self.target_dir / MERGE_SESSION_FILE
        if session_file.exists():
            session_file.unlink()

    def start_session(self, files: list[str]) -> None:
        """Initialize a new merge session.

        Args:
            files: List of file paths to process
        """
        self.session = MergeSession(
            files=files,
            current_file_index=0,
            conflicts_resolved={},
            started_at=datetime.now(UTC).isoformat(),
        )
        self.save_session()

    def prompt_resume(self) -> bool:
        """Prompt user to resume or discard existing session.

        Returns:
            True if user wants to resume, False to start fresh
        """
        if not self.session:
            return False

        self.console.print("\n[yellow]Found interrupted merge session[/yellow]")
        self.console.print(f"  Started: {self.session.started_at}")
        progress = self.session.current_file_index
        total = len(self.session.files)
        self.console.print(f"  Progress: {progress}/{total} files")
        self.console.print(
            f"  Resolved: {len(self.session.conflicts_resolved)} conflict(s)"
        )

        return Confirm.ask("Resume from where you left off?", default=True)

    def resolve_conflict_interactive(
        self,
        conflict: SectionConflict,
    ) -> str:
        """Interactive conflict resolution with three-panel view.

        Args:
            conflict: The section conflict to resolve

        Returns:
            The resolved content string
        """
        print_three_panel_merge(
            conflict.user_content,
            conflict.base_content if conflict.base_content else None,
            conflict.new_content,
            f"Section: {conflict.section_title}",
        )

        self.console.print("\n[bold]Choose resolution:[/bold]")
        self.console.print("  \\[y] Keep yours")
        self.console.print("  \\[t] Take theirs (new template)")
        self.console.print("  \\[b] Keep both (yours then theirs)")
        self.console.print("  \\[e] Edit manually (add markers)")

        choice = Prompt.ask("Choice", choices=["y", "t", "b", "e"], default="y")

        if choice == "t":
            return conflict.new_content
        elif choice == "b":
            return conflict.user_content.rstrip() + "\n\n" + conflict.new_content
        elif choice == "e":
            return self._create_manual_edit_content(conflict)
        return conflict.user_content

    def _create_manual_edit_content(self, conflict: SectionConflict) -> str:
        """Create content with markers for manual editing.

        Args:
            conflict: The section conflict

        Returns:
            Content with edit markers
        """
        return (
            f"<!-- YOUR VERSION -->\n{conflict.user_content.rstrip()}\n\n"
            f"<!-- NEW TEMPLATE -->\n{conflict.new_content.rstrip()}\n\n"
            f"<!-- EDIT ABOVE AND REMOVE THESE MARKERS -->\n"
        )

    def merge_file_interactive(
        self,
        file_path: Path,
        base_content: str,
        user_content: str,
        new_content: str,
    ) -> tuple[str, int]:
        """Interactively merge a single file.

        Args:
            file_path: Path to the file being merged
            base_content: Original template content
            user_content: User's current content
            new_content: New template content

        Returns:
            Tuple of (merged_content, conflict_count)
        """
        filename = file_path.name
        is_markdown = file_path.suffix == ".md"

        # Show diff first
        self.console.print(f"\n[bold cyan]Merging: {filename}[/bold cyan]")
        print_unified_diff(user_content, new_content, filename)

        if is_markdown:
            # Use section-level merge for markdown
            merged, conflicts = three_way_merge_sections(
                base_content,
                user_content,
                new_content,
                ConflictMarkerStyle.HTML_COMMENT,
            )

            if conflicts:
                self.console.print(
                    f"\n[yellow]Found {len(conflicts)} section conflict(s)[/yellow]"
                )

                resolved_sections: list[str] = []
                for conflict in conflicts:
                    resolved = self.resolve_conflict_interactive(conflict)
                    resolved_sections.append(resolved)

                # Rebuild merged content with resolved conflicts
                # (For now, just use the auto-merged content with markers)
                return merged, len(conflicts)

            return merged, 0
        else:
            # Use line-level merge for other files
            merged, conflicts = three_way_merge(
                base_content,
                user_content,
                new_content,
                ConflictMarkerStyle.GIT,
            )
            return merged, len(conflicts)

    def run_interactive_update(
        self,
        files_to_merge: list[tuple[Path, str, str, str]],
    ) -> dict[str, str]:
        """Run the full interactive update workflow.

        Args:
            files_to_merge: List of (path, base, user, new) tuples

        Returns:
            Dict mapping file paths to their merged content
        """
        results: dict[str, str] = {}

        # Check for existing session
        if self.check_for_existing_session():
            if self.prompt_resume():
                # Resume from saved state
                start_index = self.session.current_file_index if self.session else 0
                results = self.session.conflicts_resolved.copy() if self.session else {}
            else:
                self.clear_session()
                start_index = 0
        else:
            start_index = 0

        # Start new session if needed
        if not self.session:
            self.start_session([str(f[0]) for f in files_to_merge])

        try:
            remaining = files_to_merge[start_index:]
            for i, (path, base, user, new) in enumerate(remaining, start_index):
                total_files = len(files_to_merge)
                self.console.print(f"\n[dim]File {i + 1}/{total_files}[/dim]")

                merged, conflict_count = self.merge_file_interactive(
                    path, base, user, new
                )

                results[str(path)] = merged

                # Update session
                if self.session:
                    self.session.current_file_index = i + 1
                    self.session.conflicts_resolved[str(path)] = "merged"
                    self.save_session()

                if conflict_count > 0:
                    msg = f"{conflict_count} conflict(s) marked for review"
                    self.console.print(f"[yellow]{msg}[/yellow]")

            # Clear session on successful completion
            self.clear_session()

        except KeyboardInterrupt:
            self.console.print("\n[yellow]Merge interrupted. Progress saved.[/yellow]")
            self.console.print("Run the command again to resume.")
            raise

        return results
