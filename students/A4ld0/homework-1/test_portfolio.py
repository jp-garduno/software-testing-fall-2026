"""Tests for the portfolio helper functions."""

from src.portfolio import (
    format_github_profile_url,
    get_navigation_links,
    get_project_count,
)


def test_navigation_links_include_all_main_sections():
    """Navigation should match the sections shown on the page."""
    assert get_navigation_links() == ["About", "Projects", "Skills", "Contact"]


def test_project_count_matches_portfolio_cards():
    """Project count should reflect the displayed project list."""
    projects = [
        "Git Workflow Practice",
        "Software Testing Notes",
        "Course Repository Submission",
    ]

    assert get_project_count(projects) == 3


def test_format_github_profile_url_cleans_username():
    """Profile URL formatting should accept usernames with extra symbols."""
    assert format_github_profile_url(" @A4ld0 ") == "https://github.com/A4ld0"
