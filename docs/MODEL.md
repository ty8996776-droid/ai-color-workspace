# Model Plan

Current MVP models:

| Name | Type | Status |
|---|---|---|
| rule-analyzer | deterministic rules | active |
| rule-planner | deterministic rules | active |
| rule-dctl-engine | deterministic parameter merge | active |
| rule-scorer | deterministic rules | active |

## Future Model Targets

- MediaPipe: lightweight person/background protection.
- SAM 2 or equivalent segmentation: subject masks and video object tracking.
- OpenAI vision or similar: higher-level frame diagnosis and failure explanation.
- Local underwater classifier: water type, haze, skin, coral/fish, sand, highlight risk.

## Constraint

No external model dependency is required for the MVP. This keeps the base system runnable before heavier AI work starts.
