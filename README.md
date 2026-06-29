# AI Color Workspace

AI Color Workspace is a modular V2 foundation for an underwater AI color grading workbench.

It is built for underwater video workflows where footage often needs blue/green water correction, exposure recovery, skin protection, node planning, DCTL/LUT delivery, and repeatable grading history.

> Current status: runnable MVP architecture. This is not a finished automatic color grading product yet.

The first goal is a stable and testable platform skeleton that can later connect real visual analysis, segmentation, DCTL generation, and the existing local workbench UI.

## What You Can Try Today

- Run the JSON API locally.
- Send a sample underwater filename to `/analyze`.
- Convert analyzer output into a grading node plan.
- Generate placeholder DCTL-style parameter JSON.
- Save an export/scoring record into SQLite Memory.
- Run the unit test suite to verify the MVP foundation.

See [docs/DEMO.md](docs/DEMO.md) for a copy-paste local demo.

## Current Features

- Analyzer Agent for scene and frame metadata analysis.
- Planner Agent for color node planning.
- DCTL Engine for versioned parameter generation.
- Scorer Agent for rule-based grading scores and suggestions.
- Memory Agent backed by SQLite.
- Prompt files loaded from disk instead of hardcoded in code.
- Standard-library JSON API.
- DCTL parameter index.
- Unit tests for the MVP foundation.

## Demo Flow

```text
sample underwater clip name
  -> Analyzer Agent
  -> Planner Agent
  -> DCTL Engine
  -> Scorer + SQLite Memory
```

Example output from `/grade`:

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

## Project Structure

```text
backend/
frontend/
ai/
  analyzer/
  planner/
  dctl_engine/
  scorer/
  memory/
  prompt/
dctl/
lut/
dataset/
output/
docs/
tests/
```

## Quick Start

Clone and enter the repository:

```bash
git clone https://github.com/ty8996776-droid/ai-color-workspace.git
cd ai-color-workspace
```

Run tests:

```bash
python3 -m unittest discover -s tests -v
```

Run the API:

```bash
python3 -m backend.server
```

Default local server:

```text
http://127.0.0.1:8790
```

Send a sample request:

```bash
curl -sS -X POST http://127.0.0.1:8790/analyze \
  -H 'Content-Type: application/json' \
  -d '{"input_file":"sample-underwater-blue.mp4"}'
```

## API Routes

- `POST /analyze`
- `POST /plan`
- `POST /grade`
- `POST /export`
- `GET /history`
- `GET /models`

See [docs/API.md](docs/API.md).

## Public Demo Assets

No public screenshots, GIFs, sample videos, or release downloads are published yet.

Recommended next public asset:

- A short terminal GIF showing `/analyze -> /plan -> /grade -> /export`.
- One screenshot of the future workbench integration.
- A first GitHub Release with a source archive and a verified quick-start note.

## Important Notes

- This MVP does not include real video rendering yet.
- This MVP does not include real DaVinci `.dctl` shader output yet.
- This MVP does not include SAM 2, MediaPipe, OpenAI vision, or other production visual models yet.
- User media, API keys, `.env` files, and private material are intentionally excluded.

## Roadmap

See [docs/ROADMAP.md](docs/ROADMAP.md).
