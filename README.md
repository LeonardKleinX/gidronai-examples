# GidronAI Examples

Example scripts and configuration templates for the [GidronAI](https://gidronai.me) Synthetic Reality Engine.

## Examples

| Script | Description |
|--------|-------------|
| [`basic_scene.py`](examples/basic_scene.py) | Generate a simple urban scene with default settings |
| [`custom_agents.py`](examples/custom_agents.py) | Spawn agents with custom behaviors and export trajectories |
| [`batch_generation.py`](examples/batch_generation.py) | Generate multiple scenes in batch using the cloud API |

## Config Templates

| Config | Description |
|--------|-------------|
| [`urban_intersection.yaml`](configs/urban_intersection.yaml) | 4-way intersection with pedestrians and vehicles |
| [`highway_segment.yaml`](configs/highway_segment.yaml) | Multi-lane highway with merging traffic |
| [`indoor_warehouse.yaml`](configs/indoor_warehouse.yaml) | Indoor warehouse with forklift agents |

## Usage

### Local Engine

```bash
pip install gidronai
python examples/basic_scene.py
```

### Cloud API

```bash
pip install gidronai-sdk
export GIDRON_API_KEY="your-api-key"
python examples/batch_generation.py
```

## Requirements

- Python 3.10+
- `gidronai` (local engine) or `gidronai-sdk` (cloud API)

## License

MIT -- see the respective package licenses.

---

[GidronAI](https://gidronai.me) -- Toronto, Canada.
