# AI Color Workspace

AI Color Workspace is the modular V2 foundation for Timo's underwater AI color grading workbench.

This repository currently contains a runnable MVP architecture, not a finished automatic color grading product. The first goal is a stable and testable platform skeleton that can later connect real visual analysis, segmentation, DCTL generation, and the existing local workbench UI.

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

## Run Tests

```bash
python3 -m unittest discover -s tests -v
```

## Run API

```bash
python3 -m backend.server
```

Default local server:

```text
http://127.0.0.1:8790
```

## API Routes

- `POST /analyze`
- `POST /plan`
- `POST /grade`
- `POST /export`
- `GET /history`
- `GET /models`

See [docs/API.md](docs/API.md).

## Important Notes

- This MVP does not include real video rendering yet.
- This MVP does not include real DaVinci `.dctl` shader output yet.
- This MVP does not include SAM 2, MediaPipe, OpenAI vision, or other production visual models yet.
- User media, API keys, `.env` files, and private素材 are intentionally excluded.

## Roadmap

See [docs/ROADMAP.md](docs/ROADMAP.md).

## Partnership / Investment Interest

This project is open to early collaboration around underwater AI color workflows, creator tools, DaVinci handoff, and future commercial pilots.

For public-safe partnership or investment interest, open an issue with the `Investment / Partnership Interest` template.

See:

- [docs/INVESTOR_BRIEF.md](docs/INVESTOR_BRIEF.md)
- [docs/PARTNERSHIP_INTAKE.md](docs/PARTNERSHIP_INTAKE.md)
