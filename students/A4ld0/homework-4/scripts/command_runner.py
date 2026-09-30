"""Shared UTF-8 subprocess capture for the verification and comparison scripts."""

import subprocess


def capture_command(command, directory, environment):
    """Return a completed command with both streams, leaving exit handling to callers."""
    return subprocess.run(
        command,
        cwd=directory,
        env=environment,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
