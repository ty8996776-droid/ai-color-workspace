from typing import Any, Dict, List

from ai.common import load_prompt, log_event


def _score_from_penalty(base: int, penalty: int) -> int:
    return max(0, min(100, base - penalty))


def score(payload: Dict[str, Any]) -> Dict[str, Any]:
    prompt = load_prompt("scorer")
    exposure = abs(float(payload.get("Exposure", 0)))
    tint = abs(float(payload.get("Tint", 0)))
    water_strength = float(payload.get("WaterStrength", 0))
    temperature = abs(float(payload.get("Temperature", 0)))
    suggestions: List[str] = []
    if exposure > 0.3:
        suggestions.append("减少曝光调整幅度")
    if water_strength > 0.55:
        suggestions.append("降低蓝色饱和度")
    if temperature > 800:
        suggestions.append("降低白平衡偏移")
    if tint > 12:
        suggestions.append("检查洋红/绿色偏移")

    items = {
        "Exposure": _score_from_penalty(92, int(exposure * 60)),
        "Contrast": 88,
        "Skin": 82 if "skin" in str(payload).lower() else 80,
        "Highlight": _score_from_penalty(88, int(exposure * 35)),
        "Shadow": 84,
        "Water": _score_from_penalty(94, int(max(0, water_strength - 0.45) * 55)),
        "Noise": 87,
        "LookConsistency": _score_from_penalty(91, int((temperature / 2000) * 10)),
    }
    result = {
        "score": int(round(sum(items.values()) / len(items))),
        "items": items,
        "suggestion": suggestions or ["保持当前参数，优先检查人物肤色和高光"],
    }
    log_event("scorer", "score", {"prompt_chars": len(prompt), "result": result})
    return result
