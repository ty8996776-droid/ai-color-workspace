# Public Demo Assets

This file tracks the public-facing assets that make the repository easier to evaluate without private footage or credentials.

## Current Public State

- README quick start: ready.
- Curl demo walkthrough: ready in `docs/DEMO.md`.
- Public screenshots: not published yet.
- Public terminal GIF/video: not published yet.
- GitHub Release package: checklist prepared, not published yet.
- Private media: intentionally excluded.

## Terminal Demo Script

Use this sequence for a terminal GIF, short screen recording, or release demo transcript.

```bash
python3 -m unittest discover -s tests -v
python3 -m backend.server
curl -sS -X POST http://127.0.0.1:8790/analyze \
  -H 'Content-Type: application/json' \
  -d '{"input_file":"sample-underwater-blue.mp4"}'
curl -sS -X POST http://127.0.0.1:8790/plan \
  -H 'Content-Type: application/json' \
  -d '{"scene":"underwater","water":"blue","skin":false,"noise":"low"}'
curl -sS -X POST http://127.0.0.1:8790/grade \
  -H 'Content-Type: application/json' \
  -d '{"node_tree":["Balance","Exposure","WB","Contrast","Water","Look","Sharpen"],"recommended_dctl":["underwater_balance","deep_blue"]}'
curl -sS -X POST http://127.0.0.1:8790/export \
  -H 'Content-Type: application/json' \
  -d '{"input_file":"sample-underwater-blue.mp4","dctl_params":{"Exposure":0.12,"Temperature":-300,"Tint":6,"WaterStrength":0.41}}'
curl -sS http://127.0.0.1:8790/history
```

Recommended recording framing:

- Keep the terminal at 100-120 columns.
- Use a clean clone or clean working tree.
- Hide shell paths that reveal private local folders.
- Do not show `.env`, API keys, private video names, or user media folders.
- End on the `/history` response so viewers see the full MVP loop.

## Screenshot Candidates

- API terminal with `/analyze -> /plan -> /grade -> /export`.
- Future workbench integration panel showing node tree, DCTL parameters, score, and warnings.
- Release page with the source package and quick-start note.

## Suggested GitHub Topics

These topics are intended for repository settings, not code behavior:

- `underwater-video`
- `color-grading`
- `davinci-resolve`
- `dctl`
- `lut`
- `ai-video`
- `video-tools`
- `python`

## Public Safety Rules

- Use synthetic filenames such as `sample-underwater-blue.mp4`.
- Do not publish private clips, customer footage, `.env` files, tokens, keys, or local path screenshots.
- Treat third-party GitHub projects as references until dependency, license, and visual-quality checks pass.
