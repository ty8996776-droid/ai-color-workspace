# AI Color Workspace V2 Architecture

AI Color Workspace V2 is added as an isolated platform skeleton under `ai-color-workspace/`. It does not replace the current single-file workbench `Timo水下调色工作台.html`.

## Runtime Flow

```text
Input file/frame
  -> Analyzer Agent
  -> Planner Agent
  -> DCTL Engine
  -> Scorer Agent
  -> Memory Agent
  -> API JSON response and logs
```

## Modules

- `backend/`: standard-library JSON API server.
- `ai/analyzer/`: rule-based scene and image metadata analysis.
- `ai/planner/`: color node planning and DCTL/LUT recommendation.
- `ai/dctl_engine/`: deterministic parameter builder with version metadata.
- `ai/scorer/`: rule-based quality score and suggestions.
- `ai/memory/`: SQLite persistence for analysis, planning, params, score, feedback.
- `ai/prompt/`: prompt files loaded from disk. Prompts are not hardcoded in Agent code.
- `dctl/`: versioned DCTL parameter presets and DCTL index.
- `tests/`: unittest-based smoke tests for the MVP.

## Current Integration Choice

The current workbench remains untouched. V2 is implemented as a parallel foundation so it can later be connected through API calls without destabilizing the existing local tool.

## Logging

All Agent and API actions write JSON lines to:

`output/logs/workspace-v2.jsonl`

## Placeholder Logic

The first implementation uses deterministic rules. It does not run real computer vision, SAM 2, MediaPipe, OpenAI vision, LUT baking, or pixel processing yet.
