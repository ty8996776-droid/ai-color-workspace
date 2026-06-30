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


    def test_github_registry_recommends_underwater_capabilities(self):
        from ai.knowledge.github_registry import list_repositories, recommend_for_analysis

        all_repos = list_repositories()
        self.assertGreaterEqual(len(all_repos), 5)
        result = recommend_for_analysis({"scene": "underwater", "water": "blue", "skin": True, "noise": "low"})
        names = {item["name"] for item in result["recommendations"]}

        self.assertIn("colour-science/colour", names)
        self.assertIn("wangyanckxx/Single-Underwater-Image-Enhancement-and-Color-Restoration", names)
        self.assertIn("thatcherfreeman/utility-dctls", names)
        self.assertIn("xahidbuffon/FUnIE-GAN", names)
        json.dumps(result)

    def test_planner_includes_external_capabilities(self):
        from ai.planner.agent import plan

        result = plan({"scene": "underwater", "water": "blue", "skin": False, "noise": "low"})
        self.assertIn("external_capabilities", result)
        self.assertTrue(any(item["id"] == "colour-science-colour" for item in result["external_capabilities"]))
        self.assertTrue(result["external_warnings"])
        json.dumps(result)


    def test_github_registry_contains_all_discovered_repositories(self):
        from ai.knowledge.github_registry import list_repositories

        ids = {item["id"] for item in list_repositories()}
        expected = {
            "colour-science-colour",
            "single-underwater-image-enhancement",
            "funie-gan",
            "utility-dctls",
            "opencolorio",
            "libplacebo",
            "water-net-code",
            "all-in-one-underwater-enhancement",
            "fiveaplus-network",
            "ursct-sesr",
            "open-display-transform",
            "resolve-dctl",
        }

        self.assertTrue(expected.issubset(ids), sorted(expected - ids))

    def test_models_endpoint_exposes_external_knowledge_models(self):
        from backend.server import create_app

        response = create_app(memory_db_path=":memory:").handle("GET", "/models", {})
        self.assertTrue(response["ok"])
        external_models = [item for item in response["data"]["models"] if item.get("type") == "external_knowledge"]
        external_names = {item["name"] for item in external_models}

        self.assertGreaterEqual(len(external_models), 12)
        self.assertIn("github:colour-science/colour", external_names)
        self.assertIn("github:Li-Chongyi/Water-Net_Code", external_names)
        self.assertIn("github:jedypod/open-display-transform", external_names)
        json.dumps(response)

    def test_api_routes_are_callable_with_json(self):
        from backend.server import create_app

        app = create_app(memory_db_path=":memory:")
        analyze_response = app.handle("POST", "/analyze", {"input_file": "sample-underwater-blue.mp4"})
        plan_response = app.handle("POST", "/plan", analyze_response["data"])
        grade_response = app.handle("POST", "/grade", plan_response["data"])
        score_response = app.handle("POST", "/export", {"dctl_params": grade_response["data"]})
        history_response = app.handle("GET", "/history", {})
        models_response = app.handle("GET", "/models", {})
        external_repos_response = app.handle("GET", "/external-repos", {})

        self.assertTrue(external_repos_response["ok"])
        self.assertGreaterEqual(len(external_repos_response["data"]["repositories"]), 5)
        for response in [analyze_response, plan_response, grade_response, score_response, history_response, models_response, external_repos_response]:
            self.assertTrue(response["ok"])
            json.dumps(response)

    def test_local_model_status_and_colour_run_are_callable(self):
        from ai.runtime.local_models import list_local_models, run_local_model

        status = list_local_models()
        self.assertIn("models", status)
        self.assertTrue(any(item["id"] == "colour-science-colour" for item in status["models"]))

        result = run_local_model({"model_id": "colour-science-colour"})
        self.assertEqual(result["model"], "colour-science-colour")
        self.assertIn("delta_e_76", result)
        self.assertGreaterEqual(result["delta_e_76"], 0)
        json.dumps(result)

    def test_local_model_api_routes_are_callable(self):
        from backend.server import create_app

        app = create_app(memory_db_path=":memory:")
        status_response = app.handle("GET", "/local-models", {})
        run_response = app.handle("POST", "/local-models/run", {"model_id": "colour-science-colour"})

        self.assertTrue(status_response["ok"])
        self.assertTrue(run_response["ok"])
        self.assertIn("models", status_response["data"])
        self.assertIn("delta_e_76", run_response["data"])


if __name__ == "__main__":
    unittest.main()
