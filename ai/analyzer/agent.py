from typing import Any, Dict

from ai.common import load_prompt, log_event

SUPPORTED_SCENES = {"underwater", "portrait", "landscape", "city", "night"}


def _scene_from_name(name: str) -> str:
    lowered = name.lower()
    if any(token in lowered for token in ["underwater", "ocean", "dive", "diver", "water"]):
        return "underwater"
    if any(token in lowered for token in ["portrait", "person", "skin", "face"]):
        return "portrait"
    if any(token in lowered for token in ["night", "dark", "lowlight"]):
        return "night"
    if any(token in lowered for token in ["city", "street", "building"]):
        return "city"
    if any(token in lowered for token in ["landscape", "mountain", "forest"]):
        return "landscape"
    return "underwater"


def analyze(payload: Dict[str, Any]) -> Dict[str, Any]:
    prompt = load_prompt("analyzer")
    input_file = str(payload.get("input_file") or payload.get("file") or "unknown")
    scene = payload.get("scene") if payload.get("scene") in SUPPORTED_SCENES else _scene_from_name(input_file)
    lowered = input_file.lower()
    water = "blue" if any(token in lowered for token in ["blue", "ocean", "underwater", "dive"]) else "unknown"
    if "green" in lowered or "murky" in lowered:
        water = "green"
    skin = bool(payload.get("skin")) or any(token in lowered for token in ["portrait", "person", "face", "skin", "diver"])
    night = scene == "night" or any(token in lowered for token in ["night", "dark", "lowlight"])

    result = {
        "scene": scene,
        "camera": str(payload.get("camera") or "unknown"),
        "exposure": 0.32 if night else 0.72,
        "white_balance": 6200 if scene == "underwater" else 5600,
        "contrast": "low" if scene in {"underwater", "night"} else "medium",
        "skin": skin,
        "water": water if scene == "underwater" else "unknown",
        "visibility": "medium" if "murky" in lowered else "good",
        "noise": "medium" if night else "low",
        "dynamic_range": "high" if not night else "medium",
    }
    log_event("analyzer", "analyze", {"prompt_chars": len(prompt), "result": result})
    return result
