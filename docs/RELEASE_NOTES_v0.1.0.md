# v0.1.0 Release Notes

AI Color Workspace v0.1.0 is a runnable MVP architecture for an underwater AI color grading workbench.

## Included

- Local standard-library JSON API.
- Analyzer Agent for scene metadata.
- Planner Agent for color node planning.
- DCTL Engine for versioned parameter JSON.
- Scorer Agent for rule-based grade scoring.
- SQLite Memory for export/history records.
- Prompt files loaded from disk.
- DCTL parameter index.
- External GitHub Knowledge Registry for conservative integration planning.
- Local model status endpoints and safe first-pass adapters.
- Unit tests for the MVP foundation.
- Public demo walkthrough and release checklist.

## Not Included Yet

- Real video rendering.
- Real DaVinci Resolve `.dctl` shader output.
- Real LUT export.
- Production segmentation or mask generation.
- SAM 2, MediaPipe, OpenAI vision, or other production visual models.
- Private footage, `.env` files, API keys, or local third-party model downloads.

## Try It

```bash
python3 -m unittest discover -s tests -v
python3 -m backend.server
```

Then follow `docs/DEMO.md`.

## Safety Note

This release is a platform skeleton. It is useful for validating the API shape and workflow loop, not for final automatic color grading exports.
