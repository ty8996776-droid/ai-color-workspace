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
- Check downloaded external model/runtime status through `/local-models`.

See [docs/DEMO.md](docs/DEMO.md) for a copy-paste local demo.

## Current Features

- External GitHub Knowledge Registry for underwater enhancement, lightweight AI preview, color-science, DCTL, color-management, display-transform, and render-engine references.
- Local external model runtime status and safe first-pass adapters for downloaded GitHub projects.
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
- `GET /external-repos`
- `GET /local-models`
- `POST /local-models/run`

See [docs/API.md](docs/API.md).

## Public Demo Assets

No public screenshots, GIFs, sample videos, or release downloads are published yet. The public asset plan is tracked in [docs/PUBLIC_DEMO_ASSETS.md](docs/PUBLIC_DEMO_ASSETS.md), and the first release checklist is tracked in [docs/RELEASE_CHECKLIST.md](docs/RELEASE_CHECKLIST.md).

Prepared next public assets:

- A terminal demo script for `/analyze -> /plan -> /grade -> /export -> /history`.
- Issue templates for bug reports, feature requests, and demo feedback.
- Draft release notes for `v0.1.0`.
- A local source archive script for the first GitHub Release.

## Important Notes

- This MVP does not include real video rendering yet.
- This MVP does not include real DaVinci `.dctl` shader output yet.
- This MVP does not include SAM 2, MediaPipe, OpenAI vision, or other production visual models yet.
- User media, API keys, `.env` files, and private material are intentionally excluded.

## Roadmap

See [docs/ROADMAP.md](docs/ROADMAP.md).

## External GitHub Knowledge Registry

The workspace keeps a conservative registry of useful GitHub projects in `ai/knowledge/github_registry.py` and documents the integration strategy in `docs/GITHUB_REPO_INDEX.md`. The registry is used by Planner output as `external_capabilities` and is available through `GET /external-repos`.

## Local External Models

Downloaded third-party projects live under `third_party/github/` and are ignored by Git. The workbench exposes their local state through `GET /local-models`.

The first safe local runtime route is:

```bash
curl -sS -X POST http://127.0.0.1:8790/local-models/run \
  -H 'Content-Type: application/json' \
  -d '{"model_id":"colour-science-colour"}'
```

FUnIE-GAN has local weights in the downloaded repository and can run a CPU PyTorch probe through `/local-models/run`. Research models that require old TensorFlow/PyTorch stacks stay marked as dependency or checkpoint gated until verified.
