# Local Demo

This demo uses only placeholder metadata and local JSON routes. It does not upload media, read `.env` files, or process private video material.

## 1. Run Tests

```bash
python3 -m unittest discover -s tests -v
```

Expected result: all MVP foundation tests pass.

## 2. Start The API

```bash
python3 -m backend.server
```

Default server:

```text
http://127.0.0.1:8790
```

## 3. Analyze A Sample Underwater Filename

```bash
curl -sS -X POST http://127.0.0.1:8790/analyze \
  -H 'Content-Type: application/json' \
  -d '{"input_file":"sample-underwater-blue.mp4"}'
```

Example response:

```json
{
  "ok": true,
  "data": {
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
  },
  "error": null
}
```

## 4. Create A Node Plan

```bash
curl -sS -X POST http://127.0.0.1:8790/plan \
  -H 'Content-Type: application/json' \
  -d '{"scene":"underwater","water":"blue","skin":false,"noise":"low"}'
```

Example response:

```json
{
  "ok": true,
  "data": {
    "node_tree": ["Balance", "Exposure", "WB", "Contrast", "Water", "Look", "Sharpen"],
    "recommended_dctl": ["underwater_balance", "deep_blue"]
  },
  "error": null
}
```

## 5. Generate Placeholder Grade Parameters

```bash
curl -sS -X POST http://127.0.0.1:8790/grade \
  -H 'Content-Type: application/json' \
  -d '{"node_tree":["Balance","Exposure","WB","Contrast","Water","Look","Sharpen"],"recommended_dctl":["underwater_balance","deep_blue"]}'
```

Example response:

```json
{
  "ok": true,
  "data": {
    "Exposure": 0.12,
    "Temperature": -300,
    "Tint": 6,
    "WaterStrength": 0.41,
    "_meta": {
      "schema_version": "1.0",
      "engine": "rule-placeholder",
      "applied_dctl": []
    }
  },
  "error": null
}
```

## 6. Save A Scored Export Record

```bash
curl -sS -X POST http://127.0.0.1:8790/export \
  -H 'Content-Type: application/json' \
  -d '{"input_file":"sample-underwater-blue.mp4","dctl_params":{"Exposure":0.12,"Temperature":-300,"Tint":6,"WaterStrength":0.41}}'
```

MVP behavior: this saves a SQLite Memory record and returns a score. It does not render a video file yet.

## 7. Inspect History

```bash
curl -sS http://127.0.0.1:8790/history
```

Use this to verify that `/export` wrote a local Memory record.
