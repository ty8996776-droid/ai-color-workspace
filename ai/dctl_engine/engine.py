from typing import Any, Dict, List

from ai.common import load_prompt, log_event

DCTL_PARAM_PRESETS: Dict[str, Dict[str, float]] = {
    "base_balance": {"Exposure": 0.04, "Temperature": 0, "Tint": 0, "WaterStrength": 0.0},
    "underwater_balance": {"Exposure": 0.08, "Temperature": -160, "Tint": 4, "WaterStrength": 0.28},
    "deep_blue": {"Exposure": 0.04, "Temperature": -140, "Tint": 2, "WaterStrength": 0.13},
    "green_water_clean": {"Exposure": 0.03, "Temperature": -80, "Tint": 7, "WaterStrength": 0.18},
    "skin_protect": {"Exposure": 0.0, "Temperature": 80, "Tint": -1, "WaterStrength": -0.04},
    "noise_control": {"Exposure": -0.02, "Temperature": 0, "Tint": 0, "WaterStrength": -0.02},
}


def build_params(planner_result: Dict[str, Any]) -> Dict[str, Any]:
    prompt = load_prompt("dctl")
    recommended: List[str] = list(planner_result.get("recommended_dctl") or [])
    params = {"Exposure": 0.0, "Temperature": 0.0, "Tint": 0.0, "WaterStrength": 0.0}
    applied = []
    for name in recommended:
        preset = DCTL_PARAM_PRESETS.get(name)
        if not preset:
            continue
        applied.append({"name": name, "version": "1.0"})
        for key, value in preset.items():
            params[key] += value

    result: Dict[str, Any] = {
        "Exposure": round(max(-1.0, min(1.0, params["Exposure"])), 3),
        "Temperature": int(round(max(-2000, min(2000, params["Temperature"])))),
        "Tint": int(round(max(-50, min(50, params["Tint"])))),
        "WaterStrength": round(max(0.0, min(1.0, params["WaterStrength"])), 3),
        "_meta": {
            "schema_version": "1.0",
            "engine": "rule-placeholder",
            "applied_dctl": applied,
        },
    }
    log_event("dctl_engine", "build_params", {"prompt_chars": len(prompt), "result": result})
    return result
