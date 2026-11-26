"""Tiny pytest plugin: dump setup/call/teardown durations to $BENCH_OUT."""
import json
import os
from collections import defaultdict

PHASES = defaultdict(float)
TESTS = set()


def pytest_runtest_logreport(report):
    PHASES[report.when] += report.duration
    TESTS.add(report.nodeid)


def pytest_sessionfinish(session):
    with open(os.environ["BENCH_OUT"], "w") as out:
        json.dump({"tests": len(TESTS), **{k: PHASES[k] for k in ("setup", "call", "teardown")}}, out)
