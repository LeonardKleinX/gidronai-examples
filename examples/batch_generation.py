"""Batch scene generation using the GidronAI cloud API.

Generates multiple scenes with varied parameters and downloads
the results. Requires a GidronAI API key.
"""

import os
import sys
from pathlib import Path

from gidronai_sdk import GidronClient, GidronError, RateLimitError


# Scene variations to generate
SCENE_CONFIGS = [
    {
        "scene_type": "urban_intersection",
        "num_agents": 20,
        "weather": "clear",
        "time_of_day": "10:00",
        "num_frames": 300,
    },
    {
        "scene_type": "urban_intersection",
        "num_agents": 50,
        "weather": "rain",
        "time_of_day": "16:30",
        "num_frames": 300,
    },
    {
        "scene_type": "highway_segment",
        "num_agents": 15,
        "weather": "overcast",
        "time_of_day": "08:00",
        "num_frames": 500,
        "agent_behavior": "waypoint",
    },
    {
        "scene_type": "parking_lot",
        "num_agents": 8,
        "weather": "fog",
        "time_of_day": "06:30",
        "num_frames": 200,
    },
]


def main() -> None:
    api_key = os.environ.get("GIDRON_API_KEY")
    if not api_key:
        print("Error: Set GIDRON_API_KEY environment variable")
        sys.exit(1)

    output_base = Path("./output/batch")
    output_base.mkdir(parents=True, exist_ok=True)

    client = GidronClient(api_key=api_key)
    jobs = []

    # Submit all jobs
    print(f"Submitting {len(SCENE_CONFIGS)} scene generation jobs...\n")
    for i, config in enumerate(SCENE_CONFIGS):
        try:
            job = client.generate_scene(**config)
            jobs.append((i, config, job))
            print(f"  [{i+1}] Submitted: {config['scene_type']} "
                  f"({config['num_agents']} agents, {config['weather']}) "
                  f"-> job {job.job_id}")
        except RateLimitError as e:
            print(f"  [{i+1}] Rate limited. Retry after {e.retry_after}s")
        except GidronError as e:
            print(f"  [{i+1}] Error: {e.message}")

    # Wait for results and download
    print(f"\nWaiting for {len(jobs)} jobs to complete...\n")
    for i, config, job in jobs:
        try:
            result = client.wait_for_job(job.job_id, timeout=600)
            dest = output_base / f"scene_{i:03d}_{config['scene_type']}"
            client.download(result.output_url, dest=dest)
            print(f"  [{i+1}] Complete: {result.frame_count} frames "
                  f"({result.duration_seconds:.1f}s) -> {dest}")
        except TimeoutError:
            print(f"  [{i+1}] Timeout waiting for job {job.job_id}")
        except GidronError as e:
            print(f"  [{i+1}] Failed: {e.message}")

    # Print usage
    usage = client.get_usage()
    print(f"\nUsage this period: {usage.jobs_submitted} jobs, "
          f"{usage.frames_generated} frames, "
          f"{usage.storage_gb:.2f} GB stored")

    client.close()


if __name__ == "__main__":
    main()
