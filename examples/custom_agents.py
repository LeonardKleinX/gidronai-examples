"""Custom agent behaviors and trajectory export.

Demonstrates how to:
1. Use different navigation models (social force vs ORCA)
2. Configure agent populations with varying parameters
3. Export agent trajectories as numpy arrays
"""

import numpy as np
from pathlib import Path

from gidronai import SceneEngine, AgentPool
from gidronai.config import SceneConfig, AgentConfig, SimulationConfig


def run_with_behavior(behavior: str, num_agents: int, steps: int) -> np.ndarray:
    """Run a simulation with the given behavior model and return trajectories."""
    cfg = SceneConfig(
        scene_type="urban_intersection",
        size=(100.0, 100.0, 20.0),
        agents=AgentConfig(
            count=num_agents,
            behavior=behavior,
            max_speed=2.0,
            neighbor_radius=8.0,
            seed=42,
        ),
        simulation=SimulationConfig(total_steps=steps),
    )

    engine = SceneEngine(cfg)
    scene = engine.synthesize()

    pool = AgentPool(scene, config=cfg.agents)
    pool.assign_goals_from_config(cfg)

    # Record trajectories: shape (steps, num_agents, 3)
    trajectories = np.zeros((steps, num_agents, 3))

    dt = 1 / 60
    for step in range(steps):
        pool.update(time=step * dt, dt=dt)
        trajectories[step] = pool.positions_array()

    return trajectories


def main() -> None:
    output_dir = Path("./output/trajectories")
    output_dir.mkdir(parents=True, exist_ok=True)

    for behavior in ("social_force", "orca"):
        print(f"\nRunning {behavior} model with 30 agents for 600 steps...")
        trajectories = run_with_behavior(behavior, num_agents=30, steps=600)

        # Save raw trajectories
        out_path = output_dir / f"trajectories_{behavior}.npy"
        np.save(out_path, trajectories)
        print(f"  Saved: {out_path} (shape: {trajectories.shape})")

        # Compute statistics
        displacements = np.linalg.norm(
            trajectories[-1] - trajectories[0], axis=1
        )
        speeds = np.linalg.norm(np.diff(trajectories, axis=0), axis=2)

        print(f"  Mean displacement: {displacements.mean():.2f} m")
        print(f"  Mean speed: {speeds.mean() * 60:.2f} m/s")
        print(f"  Max speed: {speeds.max() * 60:.2f} m/s")

    print("\nDone. Trajectories saved to", output_dir)


if __name__ == "__main__":
    main()
