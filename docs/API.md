# API Reference

AI Color Workspace exposes a small standard-library JSON API for the MVP foundation. It is designed for local development and workbench integration tests, not public hosting.

Run locally:

```bash
cd /Users/timo/Desktop/视频文件/ai-color-workspace
python3 -m backend.server
```

Default server:

`http://127.0.0.1:8790`

All responses use:

```json
{
  "ok": true,
  "data": {},
  "error": null
}
```

Errors use:

```json
{
  "ok": false,
  "data": null,
  "error": {
    "code": "error_code",
    "message": "message"
  }
}
```

## POST /analyze

Classifies placeholder scene metadata from a JSON request.

Input:

```json
{
  "input_file": "sample-underwater-blue.mp4"
}
```

Output data:

```json
{
  "scene": "underwater",
  "camera": "unknown",
  "exposure": 0.72,
  "white_balance": 6200,
  "contrast": "low",
  "skin": false,
  "water": "blue",
  "visibility": "good",
  "noise": "low",
  "dynamic_range": "high"
}
```

## POST /plan

Builds a suggested grading node order from Analyzer-style metadata.

Input: Analyzer JSON.

Output data:

```json
{
  "node_tree": ["Balance", "Exposure", "WB", "Contrast", "Water", "Look", "Sharpen"],
  "recommended_dctl": ["underwater_balance", "deep_blue"],
  "external_capabilities": [
    {
      "name": "colour-science/colour",
      "category": "color_science",
      "integration_phase": "phase_1_analyzer_scorer"
    }
  ],
  "external_warnings": ["Treat every GitHub project as an external reference until dependency, license, and image-quality tests pass."],
  "external_next_step": "Create optional adapters that emit JSON metrics/preset suggestions before adding runtime dependencies."
}
```

## POST /grade

Builds versioned placeholder parameter JSON from Planner output.

Input: Planner JSON.

Output data:

```json
{
  "Exposure": 0.12,
  "Temperature": -300,
  "Tint": 6,
  "WaterStrength": 0.41,
  "_meta": {
    "schema_version": "1.0",
    "engine": "rule-placeholder",
    "applied_dctl": []
  }
}
```

## POST /export

MVP behavior: scores the current parameters and saves one Memory record. It does not render video yet.

Input:

```json
{
  "input_file": "sample.mp4",
  "dctl_params": {
    "Exposure": 0.12,
    "Temperature": -300,
    "Tint": 6,
    "WaterStrength": 0.41
  }
}
```

## GET /history

Returns recent SQLite Memory records.

## GET /models

Returns the currently available placeholder model registry plus external GitHub knowledge models marked as `external_knowledge` and `reference_only`.

## GET /external-repos

Returns the curated GitHub project registry for underwater enhancement, color-science, DCTL references, color-management, and future render engines. These entries are references first; runtime integration should be done through optional JSON adapters after license and quality checks.

## GET /local-models

Returns the local download and runtime state for external GitHub models under `third_party/github`.

The route distinguishes downloaded projects, runnable local adapters, missing dependencies, missing checkpoints, and local asset indexes such as DCTL collections.

## POST /local-models/run

Runs a safe local adapter.

Input:

```json
{
  "model_id": "colour-science-colour",
  "sample_rgb": [0.16, 0.42, 0.62],
  "target_rgb": [0.42, 0.48, 0.50]
}
```

Output data:

```json
{
  "model": "colour-science-colour",
  "run_mode": "builtin_colour_math",
  "delta_e_76": 29.3,
  "diagnosis": "large_shift"
}
```

Supported first-pass adapters:

- `colour-science-colour`: local color-space diagnostics; uses official `colour-science` when installed, otherwise built-in local math.
- `funie-gan`: CPU PyTorch probe using the downloaded `funie_generator.pth` weight.
- `resolve-dctl`: local DCTL file index.
- `utility-dctls`: local DCTL file index.

## Demo

See [DEMO.md](DEMO.md) for a full local curl sequence.
