class TaskValidationError(ValueError):
    pass


def validate_title(title: str) -> str:
    cleaned_title = title.strip()
    if not cleaned_title:
        raise TaskValidationError("A task title is required")
    if len(cleaned_title) > 80:
        raise TaskValidationError("A task title must contain at most 80 characters")
    return cleaned_title


def validate_priority(priority: int) -> int:
    if isinstance(priority, bool) or not isinstance(priority, int):
        raise TaskValidationError("Priority must be an integer")
    if priority < 1 or priority > 5:
        raise TaskValidationError("Priority must be between 1 and 5")
    return priority


def normalise_tags(tags: list[str] | None) -> list[str]:
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
