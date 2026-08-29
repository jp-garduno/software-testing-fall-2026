"""Small helper functions that describe the portfolio project."""

NAVIGATION_LINKS = ("About", "Projects", "Skills", "Contact")


def get_navigation_links():
    """Return the visible navigation labels used by the portfolio."""
    return list(NAVIGATION_LINKS)


def get_project_count(projects):
    """Return the number of projects displayed in the portfolio."""
    return len(projects)


def format_github_profile_url(username):
    """Build a GitHub profile URL from a username."""
    clean_username = username.strip().lstrip("@")
    return f"https://github.com/{clean_username}"
