import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any, Dict, Optional

from ai.analyzer.agent import analyze
from ai.common import WORKSPACE_ROOT, fail, log_event, ok
from ai.dctl_engine.engine import build_params
from ai.memory.store import MemoryStore
from ai.knowledge.github_registry import external_knowledge_models, list_repositories
from ai.planner.agent import plan
from ai.runtime.local_models import list_local_models, run_local_model
from ai.scorer.agent import score


class ColorWorkspaceApp:
    def __init__(self, memory_db_path: Optional[str] = None):
        db_path = Path(memory_db_path) if memory_db_path else None
        self.memory = MemoryStore(db_path)
        self.memory.init_db()
        self._last_analyzer: Dict[str, Any] = {}
        self._last_planner: Dict[str, Any] = {}
        self._last_params: Dict[str, Any] = {}

    def handle(self, method: str, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        try:
            log_event("api", "request", {"method": method, "path": path})
            if method == "POST" and path == "/analyze":
                self._last_analyzer = analyze(payload)
                return ok(self._last_analyzer)
            if method == "POST" and path == "/plan":
                self._last_planner = plan(payload)
                return ok(self._last_planner)
            if method == "POST" and path == "/grade":
                self._last_params = build_params(payload)
                return ok(self._last_params)
            if method == "POST" and path == "/export":
                params = payload.get("dctl_params") or self._last_params or payload
                score_result = score(params)
                record_id = self.memory.save_record(
                    input_file=str(payload.get("input_file") or "unknown"),
                    analyzer_result=payload.get("analyzer_result") or self._last_analyzer,
                    planner_result=payload.get("planner_result") or self._last_planner,
                    dctl_params=params,
                    score_result=score_result,
                    user_feedback=str(payload.get("user_feedback") or ""),
                )
                return ok({"record_id": record_id, "score_result": score_result})
            if method == "GET" and path == "/history":
                return ok({"history": self.memory.list_history(limit=int(payload.get("limit", 20)))})
            if method == "GET" and path == "/external-repos":
                return ok({"repositories": list_repositories()})
            if method == "GET" and path == "/local-models":
                return ok(list_local_models())
            if method == "POST" and path == "/local-models/run":
                return ok(run_local_model(payload))
            if method == "GET" and path == "/models":
                return ok(
                    {
                        "models": [
                            {"name": "rule-analyzer", "type": "placeholder", "status": "active"},
                            {"name": "rule-planner", "type": "placeholder", "status": "active"},
                            {"name": "rule-dctl-engine", "type": "placeholder", "status": "active"},
                            {"name": "rule-scorer", "type": "placeholder", "status": "active"},
                        ]
                        + external_knowledge_models()
                    }
                )
            return fail(f"Route not found: {method} {path}", "not_found")
        except Exception as exc:
            log_event("api", "error", {"method": method, "path": path, "error": str(exc)})
            return fail(str(exc), "internal_error")


def create_app(memory_db_path: Optional[str] = None) -> ColorWorkspaceApp:
    return ColorWorkspaceApp(memory_db_path=memory_db_path)


class _Handler(BaseHTTPRequestHandler):
    app = create_app()

    def _read_json(self) -> Dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0") or "0")
        if length == 0:
            return {}
        raw = self.rfile.read(length).decode("utf-8")
        return json.loads(raw) if raw else {}

    def _send(self, response: Dict[str, Any]) -> None:
        body = json.dumps(response, ensure_ascii=False).encode("utf-8")
        self.send_response(200 if response.get("ok") else 400)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        self._send(self.app.handle("GET", self.path.split("?")[0], {}))

    def do_POST(self) -> None:
        self._send(self.app.handle("POST", self.path.split("?")[0], self._read_json()))


def run(host: str = "127.0.0.1", port: int = 8790) -> None:
    server = HTTPServer((host, port), _Handler)
    log_event("api", "server_start", {"host": host, "port": port, "root": str(WORKSPACE_ROOT)})
    server.serve_forever()


if __name__ == "__main__":
    run()
