import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

WORKSPACE_ROOT = Path(__file__).resolve().parents[1]
PROMPT_ROOT = WORKSPACE_ROOT / "ai" / "prompt"
LOG_ROOT = WORKSPACE_ROOT / "output" / "logs"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_prompt(name: str) -> str:
    path = PROMPT_ROOT / f"{name}.md"
    if not path.exists():
        raise FileNotFoundError(f"Prompt file not found: {path}")
    return path.read_text(encoding="utf-8")


def log_event(component: str, event: str, payload: Dict[str, Any]) -> None:
    LOG_ROOT.mkdir(parents=True, exist_ok=True)
    record = {
        "created_at": utc_now(),
        "component": component,
        "event": event,
        "payload": payload,
    }
    with (LOG_ROOT / "workspace-v2.jsonl").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def ok(data: Dict[str, Any]) -> Dict[str, Any]:
    return {"ok": True, "data": data, "error": None}


def fail(message: str, code: str = "bad_request") -> Dict[str, Any]:
    return {"ok": False, "data": None, "error": {"code": code, "message": message}}
