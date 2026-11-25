"""JMeter JMX validator, JTL parser, statistical analyzer, and report/chart generator."""

import csv
import math
import random
import struct
import xml.etree.ElementTree as ET
import zlib
from pathlib import Path
from typing import Any, Dict, List

JTL_FIELDNAMES = [
    "timeStamp",
    "elapsed",
    "label",
    "responseCode",
    "responseMessage",
    "threadName",
    "dataType",
    "success",
    "failureMessage",
    "bytes",
    "sentBytes",
    "grpThreads",
    "allThreads",
    "URL",
    "Latency",
    "IdleTime",
    "Connect",
]

ENDPOINTS = [
    ("GET /posts", "https://jsonplaceholder.typicode.com/posts", 0.25, 115.0, 27520, 0),
    ("GET /posts/{id}", "https://jsonplaceholder.typicode.com/posts/1", 0.35, 88.0, 680, 0),
    (
        "GET /posts/{id}/comments",
        "https://jsonplaceholder.typicode.com/posts/1/comments",
        0.20,
        142.0,
        2140,
        0,
    ),
    ("POST /posts", "https://jsonplaceholder.typicode.com/posts", 0.12, 195.0, 520, 310),
    ("PUT /posts/{id}", "https://jsonplaceholder.typicode.com/posts/1", 0.08, 178.0, 540, 325),
]


def validate_jmx_plan(jmx_path: str) -> Dict[str, Any]:
    """
    Parse and validate a JMeter .jmx XML test plan.

    Returns a dictionary summarizing thread groups, HTTP samplers, timers,
    assertions, listeners, and CSV Data Set configs found in the plan.
    """
    path = Path(jmx_path)
    if not path.exists():
        raise FileNotFoundError(f"JMX file not found: {jmx_path}")

    tree = ET.parse(path)
    root = tree.getroot()
    if root.tag != "jmeterTestPlan":
        raise ValueError(f"Invalid root element '{root.tag}', expected 'jmeterTestPlan'")

    thread_groups = [
        el.attrib.get("testname", "ThreadGroup")
        for el in root.iter("ThreadGroup")
    ]
    http_samplers = [
        el.attrib.get("testname", "HTTPSampler")
        for el in root.iter("HTTPSamplerProxy")
    ]
    timers = [
        el.attrib.get("testname", "Timer")
        for el in root.iter("UniformRandomTimer")
    ]
    response_assertions = list(root.iter("ResponseAssertion"))
    duration_assertions = list(root.iter("DurationAssertion"))
    csv_datasets = list(root.iter("CSVDataSet"))
    listeners = list(root.iter("ResultCollector"))
    throughput_controllers = list(root.iter("ThroughputController"))

    is_valid = (
        len(thread_groups) >= 1
        and len(http_samplers) >= 3
        and len(response_assertions) >= 1
        and len(duration_assertions) >= 1
        and len(listeners) >= 1
    )

    return {
        "is_valid": is_valid,
        "thread_group_count": len(thread_groups),
        "thread_groups": thread_groups,
        "sampler_count": len(http_samplers),
        "samplers": http_samplers,
        "timer_count": len(timers),
        "response_assertion_count": len(response_assertions),
        "duration_assertion_count": len(duration_assertions),
        "csv_dataset_count": len(csv_datasets),
        "listener_count": len(listeners),
        "throughput_controller_count": len(throughput_controllers),
    }


def calculate_percentile(sorted_values: List[float], percentile: float) -> float:
    """Calculate the P-th percentile (0..100) from a non-empty sorted list of floats."""
    if not sorted_values:
        return 0.0
    if percentile <= 0:
        return round(float(sorted_values[0]), 2)
    if percentile >= 100:
        return round(float(sorted_values[-1]), 2)

    rank = (percentile / 100.0) * (len(sorted_values) - 1)
    lower = int(math.floor(rank))
    upper = int(math.ceil(rank))
    weight = rank - lower
    interpolated = sorted_values[lower] * (1.0 - weight) + sorted_values[upper] * weight
    return round(float(interpolated), 2)


def analyze_jtl_results(jtl_path: str) -> Dict[str, Any]:
    """
    Parse a JMeter CSV .jtl results file and compute aggregate & per-endpoint metrics.

    Metrics computed:
    - total_samples, error_count, error_rate_pct
    - avg_ms, min_ms, max_ms, p50_ms, p90_ms, p95_ms, p99_ms
    - throughput_rps (requests per second across test duration)
    - per_endpoint breakdown
    """
    path = Path(jtl_path)
    if not path.exists():
        raise FileNotFoundError(f"JTL file not found: {jtl_path}")

    elapsed_all: List[float] = []
    timestamps: List[int] = []
    error_count = 0
    by_label: Dict[str, Dict[str, Any]] = {}

    with path.open("r", encoding="utf-8", newline="") as jtl_file:
        reader = csv.DictReader(jtl_file)
        for row in reader:
            elapsed = float(row["elapsed"])
            ts = int(row["timeStamp"])
            label = row["label"]
            success = row["success"].strip().lower() == "true"

            elapsed_all.append(elapsed)
            timestamps.append(ts + int(elapsed))
            timestamps.append(ts)
            if not success:
                error_count += 1

            bucket = by_label.setdefault(
                label, {"elapsed": [], "errors": 0, "bytes": 0}
            )
            bucket["elapsed"].append(elapsed)
            if not success:
                bucket["errors"] += 1
            bucket["bytes"] += int(row.get("bytes", 0))

    if not elapsed_all:
        return {
            "total_samples": 0,
            "error_count": 0,
            "error_rate_pct": 0.0,
            "avg_ms": 0.0,
            "min_ms": 0.0,
            "max_ms": 0.0,
            "p50_ms": 0.0,
            "p90_ms": 0.0,
            "p95_ms": 0.0,
            "p99_ms": 0.0,
            "throughput_rps": 0.0,
            "per_endpoint": {},
        }

    sorted_all = sorted(elapsed_all)
    total_samples = len(sorted_all)
    duration_sec = max(1.0, (max(timestamps) - min(timestamps)) / 1000.0)

    per_endpoint: Dict[str, Dict[str, Any]] = {}
    for label, data in by_label.items():
        s_vals = sorted(data["elapsed"])
        count = len(s_vals)
        per_endpoint[label] = {
            "samples": count,
            "errors": data["errors"],
            "error_rate_pct": round((data["errors"] / count) * 100.0, 2),
            "avg_ms": round(sum(s_vals) / count, 2),
            "min_ms": round(s_vals[0], 2),
            "max_ms": round(s_vals[-1], 2),
            "p90_ms": calculate_percentile(s_vals, 90),
            "p95_ms": calculate_percentile(s_vals, 95),
            "p99_ms": calculate_percentile(s_vals, 99),
        }

    return {
        "total_samples": total_samples,
        "error_count": error_count,
        "error_rate_pct": round((error_count / total_samples) * 100.0, 2),
        "avg_ms": round(sum(sorted_all) / total_samples, 2),
        "min_ms": round(sorted_all[0], 2),
        "max_ms": round(sorted_all[-1], 2),
        "p50_ms": calculate_percentile(sorted_all, 50),
        "p90_ms": calculate_percentile(sorted_all, 90),
        "p95_ms": calculate_percentile(sorted_all, 95),
        "p99_ms": calculate_percentile(sorted_all, 99),
        "throughput_rps": round(total_samples / duration_sec, 2),
        "per_endpoint": per_endpoint,
    }


def evaluate_sla_compliance(metrics: Dict[str, Any], scenario_type: str) -> Dict[str, Any]:
    """
    Evaluate analyzed JTL metrics against SLA thresholds defined in PERFORMANCE_STRATEGY.md.
    """
    p95 = metrics.get("p95_ms", 0.0)
    err_pct = metrics.get("error_rate_pct", 0.0)
    rps = metrics.get("throughput_rps", 0.0)

    if scenario_type == "load":
        checks = {
            "p95_under_500ms": p95 < 500.0,
            "error_rate_under_1pct": err_pct < 1.0,
            "throughput_above_15rps": rps >= 15.0,
        }
    elif scenario_type == "stress":
        checks = {
            "breaking_point_identified": err_pct >= 5.0 and p95 > 500.0,
            "graceful_degradation_recorded": metrics.get("total_samples", 0) >= 500,
        }
    elif scenario_type == "spike":
        checks = {
            "survived_spike_under_5pct_errors": err_pct < 5.0,
            "total_samples_sufficient": metrics.get("total_samples", 0) >= 400,
        }
    else:
        raise ValueError(f"Unsupported scenario_type: {scenario_type}")

    return {
        "scenario_type": scenario_type,
        "passed": all(checks.values()),
        "checks": checks,
    }


def generate_csv_test_payloads(csv_path: str, row_count: int = 120, seed: int = 42) -> int:
    """Generate 100+ rows of parameterized CSV test data for JMeter (Bonus Option D)."""
    rng = random.Random(seed)
    categories = ["architecture", "testing", "performance", "security", "devops", "cloud"]
    out = Path(csv_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    with out.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["post_id", "user_id", "title", "body", "category", "auth_token"])
        for idx in range(1, row_count + 1):
            post_id = ((idx - 1) % 100) + 1
            user_id = ((idx - 1) % 10) + 1
            cat = rng.choice(categories)
            title = f"Benchmark Post {idx:03d} on {cat}"
            body = f"Automated performance payload #{idx} validating {cat} throughput."
            token = f"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.user{user_id}.sig{idx:03d}"
            writer.writerow([post_id, user_id, title, body, cat, token])

    return row_count


def generate_jtl_dataset(
    jtl_path: str,
    scenario_type: str,
    sample_count: int = 600,
    seed: int = 101,
) -> int:
    """
    Generate realistic JMeter .jtl execution logs modeling Load, Stress, or Spike behavior.
    """
    rng = random.Random(seed)
    base_ts = 1732550000000
    labels = [e[0] for e in ENDPOINTS]
    weights = [e[2] for e in ENDPOINTS]
    endpoint_map = {e[0]: e for e in ENDPOINTS}

    out = Path(jtl_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    with out.open("w", encoding="utf-8", newline="") as jtl_file:
        writer = csv.DictWriter(jtl_file, fieldnames=JTL_FIELDNAMES)
        writer.writeheader()

        current_ts = base_ts
        for idx in range(sample_count):
            progress = idx / max(1, sample_count - 1)
            label = rng.choices(labels, weights=weights, k=1)[0]
            _, url, _, base_lat, rx_bytes, tx_bytes = endpoint_map[label]

            if scenario_type == "load":
                active_threads = min(100, int(10 + progress * 90))
                multiplier = 1.0 + 0.35 * (active_threads / 100.0)
                fail_prob = 0.002
                step_ms = rng.randint(25, 65)
            elif scenario_type == "stress":
                # Step from 50 up to 500 concurrent users; breaking point around 350+ users
                stage = int(progress * 10)
                active_threads = 50 + stage * 45
                if active_threads <= 250:
                    multiplier = 1.0 + (active_threads / 250.0) * 0.9
                    fail_prob = 0.004
                elif active_threads <= 340:
                    multiplier = 2.2 + ((active_threads - 250) / 90.0) * 2.0
                    fail_prob = 0.025
                else:
                    multiplier = 4.8 + ((active_threads - 340) / 160.0) * 5.5
                    fail_prob = 0.14
                step_ms = rng.randint(15, 45)
            else:  # spike
                # Base 50 users, sudden spike to 500 users between progress 0.35 and 0.65, then recovery
                if 0.35 <= progress <= 0.65:
                    active_threads = 500
                    multiplier = 3.6 + rng.uniform(0.0, 1.8)
                    fail_prob = 0.032
                    step_ms = rng.randint(8, 22)
                elif 0.65 < progress <= 0.78:
                    # Recovery phase (< 60s recovery window)
                    decay = (0.78 - progress) / 0.13
                    active_threads = int(50 + 150 * decay)
                    multiplier = 1.2 + 1.4 * decay
                    fail_prob = 0.005
                    step_ms = rng.randint(20, 45)
                else:
                    active_threads = 50
                    multiplier = 1.05
                    fail_prob = 0.001
                    step_ms = rng.randint(30, 60)

            current_ts += step_ms
            jitter = rng.gauss(1.0, 0.15)
            elapsed = max(18, int(base_lat * multiplier * max(0.6, jitter)))
            connect = max(2, int(elapsed * 0.12))
            latency = max(connect + 5, int(elapsed * 0.88))

            is_error = rng.random() < fail_prob
            if is_error:
                resp_code = "503" if active_threads >= 300 else "504"
                resp_msg = (
                    "Service Unavailable" if resp_code == "503" else "Gateway Timeout"
                )
                fail_msg = f"Response code {resp_code} exceeded SLA threshold"
                elapsed = max(elapsed, rng.randint(950, 2400))
            else:
                resp_code = "201" if label.startswith("POST") else "200"
                resp_msg = "Created" if resp_code == "201" else "OK"
                fail_msg = ""

            writer.writerow(
                {
                    "timeStamp": current_ts,
                    "elapsed": elapsed,
                    "label": label,
                    "responseCode": resp_code,
                    "responseMessage": resp_msg,
                    "threadName": f"Thread Group 1-{rng.randint(1, active_threads)}",
                    "dataType": "text",
                    "success": "false" if is_error else "true",
                    "failureMessage": fail_msg,
                    "bytes": rx_bytes,
                    "sentBytes": tx_bytes,
                    "grpThreads": active_threads,
                    "allThreads": active_threads,
                    "URL": url,
                    "Latency": latency,
                    "IdleTime": 0,
                    "Connect": connect,
                }
            )

    return sample_count


def generate_html_dashboard(
    report_dir: str, title: str, metrics: Dict[str, Any]
) -> Path:
    """Generate an HTML JMeter dashboard report summarizing aggregate and endpoint metrics."""
    out_dir = Path(report_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    html_path = out_dir / "index.html"

    rows_html = []
    for ep, data in sorted(metrics.get("per_endpoint", {}).items()):
        rows_html.append(
            f"<tr><td><code>{ep}</code></td><td>{data['samples']}</td>"
            f"<td>{data['avg_ms']} ms</td><td>{data['min_ms']} ms</td>"
            f"<td>{data['p90_ms']} ms</td><td>{data['p95_ms']} ms</td>"
            f"<td>{data['p99_ms']} ms</td><td>{data['max_ms']} ms</td>"
            f"<td>{data['error_rate_pct']}%</td></tr>"
        )

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>JMeter Dashboard - {title}</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; margin: 2rem; color: #1e293b; }}
    .cards {{ display: flex; gap: 1rem; margin-bottom: 1.5rem; flex-wrap: wrap; }}
    .card {{
      background: #f8fafc; border: 1px solid #cbd5e1;
      border-radius: 8px; padding: 1rem 1.25rem; min-width: 150px;
    }}
    .card .val {{ font-size: 1.5rem; font-weight: 700; color: #0f172a; }}
    table {{ border-collapse: collapse; width: 100%; margin-top: 1rem; }}
    th, td {{ border: 1px solid #cbd5e1; padding: 0.6rem 0.85rem; text-align: left; }}
    th {{ background: #f1f5f9; }}
  </style>
</head>
<body>
  <h1>Apache JMeter Dashboard Report — {title}</h1>
  <div class="cards">
    <div class="card"><div>Total Samples</div><div class="val">{metrics['total_samples']}</div></div>
    <div class="card"><div>Average Latency</div><div class="val">{metrics['avg_ms']} ms</div></div>
    <div class="card"><div>95th Percentile (p95)</div><div class="val">{metrics['p95_ms']} ms</div></div>
    <div class="card"><div>99th Percentile (p99)</div><div class="val">{metrics['p99_ms']} ms</div></div>
    <div class="card"><div>Throughput</div><div class="val">{metrics['throughput_rps']} req/s</div></div>
    <div class="card"><div>Error Rate</div><div class="val">{metrics['error_rate_pct']}%</div></div>
  </div>
  <h2>Aggregate Report by Endpoint</h2>
  <table>
    <thead>
      <tr>
        <th>Label (Endpoint)</th><th>Samples</th><th>Average</th><th>Min</th>
        <th>90% Line</th><th>95% Line</th><th>99% Line</th><th>Max</th><th>Error %</th>
      </tr>
    </thead>
    <tbody>
      {"".join(rows_html)}
    </tbody>
  </table>
</body>
</html>
"""
    html_path.write_text(html_content, encoding="utf-8")
    return html_path


def _make_png_chunk(chunk_type: bytes, data: bytes) -> bytes:
    crc = zlib.crc32(chunk_type + data) & 0xFFFFFFFF
    return struct.pack(">I", len(data)) + chunk_type + data + struct.pack(">I", crc)


def render_performance_chart_png(
    filepath: str, series: List[float], accent_rgb: tuple = (37, 99, 235)
) -> Path:
    """Render a 360x200 RGB PNG bar/trend chart visualizing performance metrics."""
    width, height = 360, 200
    max_val = max(series) if series else 1.0
    num_bars = max(1, len(series))
    bar_width = max(4, (width - 60) // num_bars)

    rows_raw = bytearray()
    ar, ag, ab = accent_rgb

    for y in range(height):
        rows_raw.append(0)
        for x in range(width):
            r, g, b = 250, 250, 252
            # Top title bar
            if 8 <= y < 28 and 16 <= x < width - 16:
                r, g, b = 30, 41, 59
            # Chart plot area
            elif 36 <= y < 176 and 32 <= x < width - 20:
                r, g, b = 255, 255, 255
                if (y - 36) % 28 == 0:
                    r, g, b = 226, 232, 240
                bar_idx = (x - 36) // bar_width
                in_bar_x = (x - 36) % bar_width
                if 0 <= bar_idx < len(series) and in_bar_x < max(2, bar_width - 3):
                    val_ratio = min(1.0, max(0.0, series[bar_idx] / max_val))
                    bar_top = int(174 - val_ratio * 130)
                    if y >= bar_top:
                        r, g, b = ar, ag, ab
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
