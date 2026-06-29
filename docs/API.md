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
  "recommended_dctl": ["underwater_balance", "deep_blue"]
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

Returns the currently available placeholder model registry.

## Demo

See [DEMO.md](DEMO.md) for a full local curl sequence.
