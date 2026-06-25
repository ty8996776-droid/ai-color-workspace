# Roadmap

## Phase 1: V2 Foundation

- Isolated project structure.
- Five basic Agents.
- Prompt files.
- JSON API.
- SQLite Memory.
- DCTL parameter index.
- Unit tests.

## Phase 2: Current Workbench Integration

- Add a V2 API bridge to `Timo水下调色工作台.html`.
- Send current frame metadata to `/analyze`.
- Show Planner and Scorer output in the UI.
- Keep the old workbench path usable.

## Phase 3: Real Visual Analysis

- Extract current frame images.
- Add lightweight water/skin/highlight masks.
- Add MediaPipe person protection.

## Phase 4: AI Mask Prototype

- Add segmentation server.
- Test SAM 2 or a local alternative.
- Cache masks for video keyframes.

## Phase 5: DCTL/LUT Delivery

- Generate real DCTL files.
- Validate parameters in DaVinci Resolve.
- Export DaVinci node reports.

## Phase 6: Learning Loop

- Use Memory feedback to compare parameter choices.
- Add manual rating from user.
- Improve Planner and Scorer with real project history.
