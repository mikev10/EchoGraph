"""Data models for EchoGraph CLI."""

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class SetupMode(Enum):
    """Init setup mode."""

    MINIMAL = "minimal"
    FULL = "full"
    INTERACTIVE = "interactive"


@dataclass
class ProjectConfig:
    """Project configuration for template rendering."""

    project_name: str
    tech_stack: list[str] = field(default_factory=list)
    has_tests: bool = True
    test_framework: str = "pytest"
    formatter: str = "ruff"
    linter: str = "ruff"


@dataclass
class ValidationResult:
    """Result of a validation check."""

    file_path: Path
    line_number: int | None
    rule: str
    message: str
    severity: str  # "error", "warning", "info"


@dataclass
class DoctorCheck:
    """Result of a doctor check."""

    name: str
    passed: bool
    message: str
    fix_hint: str | None = None


@dataclass
class MergeConflict:
    """A conflict detected during three-way merge."""

    line_number: int
    base_content: str
    user_content: str
    new_content: str


@dataclass
class MergeResult:
    """Result of template merge operation."""

    merged_content: str
    conflicts: list[MergeConflict]
    has_conflicts: bool = field(init=False)

    def __post_init__(self) -> None:
        """Set has_conflicts based on conflicts list."""
        self.has_conflicts = len(self.conflicts) > 0


class ConflictResolution(Enum):
    """How to resolve file conflicts during init."""

    SKIP = "skip"
    OVERWRITE = "overwrite"
    RENAME = "rename"


@dataclass
class FileConflict:
    """A file that already exists in the target directory."""

    template_path: str  # Relative path from templates
    target_path: Path  # Absolute path in target directory
    resolution: ConflictResolution | None = None
