import json
import os
import tempfile
import unittest
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parents[1]

import sys

sys.path.insert(0, str(WORKSPACE_ROOT))


class V2FoundationTests(unittest.TestCase):
    def test_analyzer_returns_required_json_shape(self):
        from ai.analyzer.agent import analyze

        result = analyze({"input_file": "sample-underwater-blue.mp4"})
        self.assertEqual(result["scene"], "underwater")
        self.assertIn(result["water"], {"blue", "green", "neutral", "unknown"})
        self.assertIsInstance(result["exposure"], float)
        self.assertIn("white_balance", result)
        json.dumps(result)

    def test_planner_returns_node_tree_and_dctl_list(self):
        from ai.planner.agent import plan

        result = plan({"scene": "underwater", "water": "blue", "skin": True, "noise": "low"})
        self.assertIn("Balance", result["node_tree"])
        self.assertIn("Water", result["node_tree"])
        self.assertIn("underwater_balance", result["recommended_dctl"])
        json.dumps(result)

    def test_dctl_engine_returns_versioned_parameters(self):
        from ai.dctl_engine.engine import build_params

        result = build_params({"recommended_dctl": ["underwater_balance", "deep_blue", "skin_protect"]})
        self.assertIn("Exposure", result)
        self.assertIn("WaterStrength", result)
        self.assertIn("_meta", result)
        self.assertEqual(result["_meta"]["schema_version"], "1.0")
        json.dumps(result)

    def test_scorer_returns_score_items_and_suggestions(self):
        from ai.scorer.agent import score

        result = score({"Exposure": 0.12, "Temperature": -300, "Tint": 6, "WaterStrength": 0.41})
        self.assertGreaterEqual(result["score"], 0)
        self.assertLessEqual(result["score"], 100)
        self.assertIn("Water", result["items"])
        self.assertIsInstance(result["suggestion"], list)
        json.dumps(result)

    def test_memory_store_writes_and_reads_history(self):
        from ai.memory.store import MemoryStore

        with tempfile.TemporaryDirectory() as tmpdir:
            store = MemoryStore(Path(tmpdir) / "memory.sqlite3")
            store.init_db()
            store.save_record(
                input_file="sample.mp4",
                analyzer_result={"scene": "underwater"},
                planner_result={"node_tree": ["Balance"]},
                dctl_params={"Exposure": 0.1},
                score_result={"score": 90},
                user_feedback="good",
            )
            history = store.list_history(limit=10)

        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["input_file"], "sample.mp4")
        self.assertEqual(history[0]["score_result"]["score"], 90)

    def test_prompt_files_are_indexed_and_not_missing(self):
        required = ["analyzer.md", "planner.md", "dctl.md", "scorer.md"]
        for name in required:
            path = WORKSPACE_ROOT / "ai" / "prompt" / name
            self.assertTrue(path.exists(), f"missing prompt file: {name}")
            self.assertGreater(path.stat().st_size, 20)

    def test_api_routes_are_callable_with_json(self):
        from backend.server import create_app

        app = create_app(memory_db_path=":memory:")
        analyze_response = app.handle("POST", "/analyze", {"input_file": "sample-underwater-blue.mp4"})
        plan_response = app.handle("POST", "/plan", analyze_response["data"])
        grade_response = app.handle("POST", "/grade", plan_response["data"])
        score_response = app.handle("POST", "/export", {"dctl_params": grade_response["data"]})
        history_response = app.handle("GET", "/history", {})
        models_response = app.handle("GET", "/models", {})

        for response in [analyze_response, plan_response, grade_response, score_response, history_response, models_response]:
            self.assertTrue(response["ok"])
            json.dumps(response)


if __name__ == "__main__":
    unittest.main()
