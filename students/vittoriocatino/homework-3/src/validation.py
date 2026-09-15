"""Input validation helpers for the task tracker."""


class TaskValidationError(ValueError):
    """Raised when an input cannot be used to create or update a task."""


def validate_title(title: str) -> str:
    """Strip and validate a non-empty task title of at most 80 characters."""

    cleaned_title = title.strip()
    if not cleaned_title:
        raise TaskValidationError("A task title is required")
    if len(cleaned_title) > 80:
        raise TaskValidationError("A task title must contain at most 80 characters")
    return cleaned_title


def validate_priority(priority: int) -> int:
    """Validate the integer priority scale from one (low) to five (high)."""

    if isinstance(priority, bool) or not isinstance(priority, int):
        raise TaskValidationError("Priority must be an integer")
    if priority < 1 or priority > 5:
        raise TaskValidationError("Priority must be between 1 and 5")
    return priority


def normalise_tags(tags: list[str] | None) -> list[str]:
    """Return unique lowercase tags while preserving their original order."""

    if tags is None:
        return []
    normalised = []
    for tag in tags:
        if not isinstance(tag, str):
            raise TaskValidationError("Every tag must be text")
        cleaned_tag = tag.strip().lower()
        if cleaned_tag and cleaned_tag not in normalised:
            normalised.append(cleaned_tag)
    return normalised
