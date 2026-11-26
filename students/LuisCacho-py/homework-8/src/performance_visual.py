"""Bonus features: Visual Regression PNG renderer/comparator (Option A) and Performance Metrics (Option C)."""

from pathlib import Path
from typing import Any, Dict, List
import struct
import zlib


def _make_png_chunk(chunk_type: bytes, data: bytes) -> bytes:
    crc = zlib.crc32(chunk_type + data) & 0xFFFFFFFF
    return struct.pack(">I", len(data)) + chunk_type + data + struct.pack(">I", crc)


def render_todomvc_png(
    filepath: str,
    todos: List[Dict[str, Any]],
    current_filter: str = "all",
    active_count: int = 0,
) -> Path:
    """
    Render a valid 320x200 RGB PNG image representing the current TodoMVC UI state.

    Visual layout encodes:
    - Top header banner (TodoMVC red accent)
    - Each visible todo row (green status bar for completed, amber for active)
    - Footer bar encoding active filter tab and active item counter
    """
    width, height = 320, 200
    rows_raw = bytearray()

    for y in range(height):
        rows_raw.append(0)  # PNG filter type 0 (None)
        for x in range(width):
            # Default background: light warm gray (#F5F5F5)
            r, g, b = 245, 245, 245

            # Header bar
            if 10 <= y < 35 and 20 <= x < 300:
                r, g, b = 175, 47, 47

            # Todo card container
            elif 40 <= y < 165 and 20 <= x < 300:
                r, g, b = 255, 255, 255
                row_index = (y - 45) // 22
                row_offset = (y - 45) % 22
                if 0 <= row_index < len(todos) and 2 <= row_offset <= 18:
                    item = todos[row_index]
                    # Left status indicator box (28..44)
                    if 28 <= x < 44:
                        if item.get("completed"):
                            r, g, b = 46, 160, 67
                        else:
                            r, g, b = 210, 153, 34
                    # Simulated text bar proportional to title length
                    text_end = min(285, 52 + len(item.get("title", "")) * 7)
                    if 52 <= x < text_end and 7 <= row_offset <= 13:
                        if item.get("completed"):
                            r, g, b = 180, 180, 180
                        else:
                            r, g, b = 60, 60, 60

            # Footer filter indicator
            elif 170 <= y < 190 and 20 <= x < 300:
                if current_filter == "all" and 25 <= x < 95:
                    r, g, b = 175, 47, 47
                elif current_filter == "active" and 110 <= x < 190:
                    r, g, b = 37, 99, 235
                elif current_filter == "completed" and 205 <= x < 295:
                    r, g, b = 46, 160, 67
                elif 280 <= x < 280 + min(15, active_count * 3):
                    r, g, b = 80, 80, 80
                else:
                    r, g, b = 230, 230, 230

            rows_raw.extend((r, g, b))

    signature = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    compressed = zlib.compress(bytes(rows_raw), level=6)
    png_bytes = (
        signature
        + _make_png_chunk(b"IHDR", ihdr)
        + _make_png_chunk(b"IDAT", compressed)
        + _make_png_chunk(b"IEND", b"")
    )

    out_path = Path(filepath)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(png_bytes)
    return out_path


def compare_screenshots(baseline_path: str, candidate_path: str) -> Dict[str, Any]:
    """
    Compare two PNG screenshots and report visual regression metrics (Bonus Option A).
    """
    base_bytes = Path(baseline_path).read_bytes()
    cand_bytes = Path(candidate_path).read_bytes()

    if base_bytes == cand_bytes:
        return {
            "identical": True,
            "diff_bytes": 0,
            "diff_ratio": 0.0,
        }

    max_len = max(len(base_bytes), len(cand_bytes))
    min_len = min(len(base_bytes), len(cand_bytes))
    diff_count = abs(len(base_bytes) - len(cand_bytes))
    for idx in range(min_len):
        if base_bytes[idx] != cand_bytes[idx]:
            diff_count += 1

    return {
        "identical": False,
        "diff_bytes": diff_count,
        "diff_ratio": round(diff_count / max_len, 4) if max_len else 0.0,
    }


def summarize_performance_metrics(metrics: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Aggregate operation timings into a performance report summary (Bonus Option C).
    """
    if not metrics:
        return {
            "total_operations": 0,
            "total_duration_ms": 0.0,
            "average_duration_ms": 0.0,
            "max_duration_ms": 0.0,
            "by_action": {},
        }

    durations = [float(m["duration_ms"]) for m in metrics]
    by_action: Dict[str, List[float]] = {}
    for entry in metrics:
        by_action.setdefault(entry["action"], []).append(float(entry["duration_ms"]))

    action_summary = {
        action: {
            "count": len(vals),
            "avg_ms": round(sum(vals) / len(vals), 4),
            "max_ms": round(max(vals), 4),
        }
        for action, vals in by_action.items()
    }

    total_ms = round(sum(durations), 4)
    return {
        "total_operations": len(durations),
        "total_duration_ms": total_ms,
        "average_duration_ms": round(total_ms / len(durations), 4),
        "max_duration_ms": round(max(durations), 4),
        "by_action": action_summary,
    }
