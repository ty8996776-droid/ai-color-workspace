from typing import Any, Dict, List

from ai.common import load_prompt, log_event
from ai.knowledge.github_registry import recommend_for_analysis


def _nodes_for_scene(scene: str, water: str, skin: bool) -> List[str]:
    if scene == "underwater":
        nodes = ["Balance", "Exposure", "WB", "Contrast", "Water", "Look", "Sharpen"]
        if skin:
            nodes.insert(5, "SkinProtect")
        return nodes
    if scene == "portrait":
        return ["Balance", "Exposure", "WB", "SkinProtect", "Contrast", "Look", "Sharpen"]
    if scene == "night":
        return ["Balance", "Denoise", "Exposure", "WB", "Contrast", "Look", "Sharpen"]
    return ["Balance", "Exposure", "WB", "Contrast", "Look", "Sharpen"]


def plan(analyzer_result: Dict[str, Any]) -> Dict[str, Any]:
    prompt = load_prompt("planner")
    scene = str(analyzer_result.get("scene") or "underwater")
    water = str(analyzer_result.get("water") or "unknown")
    skin = bool(analyzer_result.get("skin"))
    dctl = ["underwater_balance"] if scene == "underwater" else ["base_balance"]
    if water == "blue":
        dctl.append("deep_blue")
    if water == "green":
        dctl.append("green_water_clean")
    if skin:
        dctl.append("skin_protect")
    if analyzer_result.get("noise") in {"medium", "high"}:
        dctl.append("noise_control")

    external = recommend_for_analysis(analyzer_result)
    result = {
        "node_tree": _nodes_for_scene(scene, water, skin),
        "recommended_dctl": dctl,
        "external_capabilities": external["recommendations"],
        "external_warnings": external["warnings"],
        "external_next_step": external["next_step"],
    }
    log_event("planner", "plan", {"prompt_chars": len(prompt), "result": result})
    return result
