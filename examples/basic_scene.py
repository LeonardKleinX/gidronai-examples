"""Basic scene generation using the GidronAI local engine.

Generates an urban intersection scene with 12 pedestrian agents,
runs the physics simulation for 500 steps, and exports training
data in COCO format.
"""

from pathlib import Path

from gidronai import SceneEngine, PhysicsWorld, AgentPool, DataExporter
from gidronai.config import load_config


def main() -> None:
    # Load configuration (or use defaults)
    config_path = Path(__file__).parent.parent / "configs" / "urban_intersection.yaml"

    if config_path.exists():
        cfg = load_config(config_path)
    else:
        # Fall back to programmatic config
        from gidronai.config import SceneConfig, PhysicsConfig, AgentConfig, ExportConfig, SimulationConfig
        cfg = SceneConfig(
            scene_type="urban_intersection",
            size=(200.0, 200.0, 50.0),
            weather="overcast",
            time_of_day="14:30",
            physics=PhysicsConfig(gravity=-9.81, dt=1/240),
            agents=AgentConfig(count=12, behavior="social_force"),
            export=ExportConfig(format="coco", resolution=(1920, 1080)),
            simulation=SimulationConfig(total_steps=500),
        )

    # Build the scene
    engine = SceneEngine(cfg)
    scene = engine.synthesize()
    print(f"Scene synthesized: {len(scene)} nodes")

    # Attach physics
    world = PhysicsWorld(scene, gravity=cfg.physics.gravity, dt=cfg.physics.dt)
    print(f"Physics world: {len(world.bodies)} bodies")

    # Spawn agents
    pool = AgentPool(scene, num_agents=cfg.agents.count, behavior=cfg.agents.behavior)
    pool.assign_goals_from_config(cfg)
    print(f"Agents spawned: {pool.active_count} active")

    # Set up exporter
    exporter = DataExporter(scene, config=cfg.export)

    # Run simulation
    for step in range(cfg.simulation.total_steps):
        world.step()
        pool.update(world.time, dt=cfg.physics.dt)

        # Capture every Nth frame
        if step % cfg.export.frame_skip == 0:
            exporter.capture_frame(
                frame_id=step,
                timestamp=world.time,
                agent_positions=pool.positions_array(),
            )

        if step % 100 == 0:
            print(f"  Step {step}/{cfg.simulation.total_steps} | "
                  f"Active agents: {pool.active_count} | "
                  f"KE: {world.kinetic_energy:.2f}")

    # Export
    output_dir = Path("./output/basic_scene")
    exporter.write(output_dir)
    print(f"\nExport complete: {exporter.frame_count} frames -> {output_dir}")


if __name__ == "__main__":
    main()
