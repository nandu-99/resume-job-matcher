"""Measure synthetic end-to-end CPU requests: python -m m5.benchmark."""

import argparse
import importlib.metadata
import json
import platform
from pathlib import Path
import statistics
import threading
import time

import psutil
import torch

from m5.app import EXAMPLE_JOB, EXAMPLE_RESUME
from m5.inference import clear_matcher_cache, load_matcher
from m5.service import analyse_match


def percentile(values, fraction):
    values = sorted(values)
    position = (len(values) - 1) * fraction
    lower = int(position)
    return values[lower] + (values[min(lower + 1, len(values) - 1)] - values[lower]) * (position - lower)


def run_benchmark(repeats=20):
    if repeats < 5:
        raise ValueError("Use at least five timed requests.")
    process = psutil.Process()
    baseline = process.memory_info().rss
    peak = [baseline]
    stop = threading.Event()

    def sample_memory():
        while not stop.wait(0.01):
            peak[0] = max(peak[0], process.memory_info().rss)

    clear_matcher_cache()
    sampler = threading.Thread(target=sample_memory, daemon=True)
    sampler.start()
    try:
        started = time.perf_counter()
        matcher = load_matcher(device="cpu")
        load_seconds = time.perf_counter() - started
        started = time.perf_counter()
        analyse_match(EXAMPLE_RESUME, EXAMPLE_JOB)
        first_request_ms = (time.perf_counter() - started) * 1000
        timings = []
        for _ in range(repeats):
            started = time.perf_counter()
            analyse_match(EXAMPLE_RESUME, EXAMPLE_JOB)
            timings.append((time.perf_counter() - started) * 1000)
        peak[0] = max(peak[0], process.memory_info().rss)
    finally:
        stop.set()
        sampler.join()
    return {
        "schema_version": 1,
        "scope": "CPU guarded service, synthetic example, sequential requests; excludes browser/network/rendering",
        "python": platform.python_version(), "platform": platform.platform(),
        "cpu_count": os_cpu_count(), "torch_threads": torch.get_num_threads(),
        "versions": {name: importlib.metadata.version(name) for name in (
            "torch", "transformers", "tokenizers", "streamlit", "huggingface-hub", "psutil")},
        "weights_sha256": matcher.weights_sha256,
        "model_load_seconds": round(load_seconds, 4),
        "model_load_scope": "includes provision/download if absent, hash verification and CPU loading; imports excluded",
        "first_request_ms_after_load": round(first_request_ms, 3),
        "warm_requests": repeats,
        "warm_median_ms": round(statistics.median(timings), 3),
        "warm_p95_ms": round(percentile(timings, 0.95), 3),
        "warm_mean_ms": round(statistics.mean(timings), 3),
        "rss_baseline_mib": round(baseline / 2**20, 2),
        "sampled_peak_rss_mib": round(peak[0] / 2**20, 2),
        "memory_scope": "whole process RSS sampled every 10 ms; imports included; not a guaranteed peak",
    }


def os_cpu_count():
    import os
    return os.cpu_count()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repeats", type=int, default=20)
    parser.add_argument("--output", type=Path, default=Path("m5/performance/local_cpu.json"))
    args = parser.parse_args()
    report = run_benchmark(args.repeats)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
