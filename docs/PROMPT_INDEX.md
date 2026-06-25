# Prompt Index

Prompts are stored under `ai/prompt/`. Agent code must load prompts from these files rather than hardcoding prompt text.

| Agent | File | Purpose |
|---|---|---|
| Analyzer | `../ai/prompt/analyzer.md` | scene and image metadata analysis |
| Planner | `../ai/prompt/planner.md` | node tree and DCTL/LUT planning |
| DCTL Engine | `../ai/prompt/dctl.md` | parameter generation guidance |
| Scorer | `../ai/prompt/scorer.md` | score and suggestion guidance |

## Rule

Any future LLM prompt change must be made in this folder and reflected in this index.
