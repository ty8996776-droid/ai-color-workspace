import json
import math
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List

from ai.common import WORKSPACE_ROOT, log_event
from ai.knowledge.github_registry import list_repositories

LOCAL_REPO_ROOT = WORKSPACE_ROOT / "third_party" / "github"
EXTERNAL_VENV_PYTHON = WORKSPACE_ROOT / ".venv-external" / "bin" / "python"


def _repo_path(repo_id: str) -> Path:
    return LOCAL_REPO_ROOT / repo_id


def _python_has(module_name: str, python_path: Path = Path(sys.executable)) -> Dict[str, Any]:
    if not python_path.exists():
        return {"available": False, "python": str(python_path), "reason": "python_not_found"}
    script = (
        "import importlib, json\n"
        f"m=importlib.import_module({module_name!r})\n"
        "print(json.dumps({'version': getattr(m, '__version__', 'unknown')}))\n"
    )
    result = subprocess.run(
        [str(python_path), "-c", script],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=12,
    )
    if result.returncode != 0:
        reason = result.stderr.strip().splitlines()[-1] if result.stderr.strip() else "import_failed"
        return {"available": False, "python": str(python_path), "reason": reason}
    data = json.loads(result.stdout)
    return {"available": True, "python": str(python_path), "version": data["version"]}


def _repo_runtime_status(repo: Dict[str, Any]) -> Dict[str, Any]:
    repo_id = repo["id"]
    path = _repo_path(repo_id)
    status: Dict[str, Any] = {
        "id": repo_id,
        "name": repo["name"],
        "category": repo["category"],
        "download": {"exists": path.exists(), "path": str(path)},
        "runtime": "downloaded" if path.exists() else "not_downloaded",
        "can_run_now": False,
        "run_mode": "status_only",
        "notes": [],
    }

    if repo_id == "colour-science-colour":
        colour_state = _python_has("colour", EXTERNAL_VENV_PYTHON)
        status["dependency"] = {"colour": colour_state}
        status["can_run_now"] = True
        if colour_state["available"]:
            status["runtime"] = "ready"
            status["run_mode"] = "colour_science_python"
        else:
            status["runtime"] = "ready_with_builtin_fallback"
            status["run_mode"] = "builtin_colour_math"
            status["notes"].append(
                "Official colour-science import is not available yet; using built-in local color math for diagnostics."
            )

    elif repo_id == "funie-gan":
        weights = sorted(path.glob("**/*.pth")) + sorted(path.glob("**/*.h5"))
        torch_state = _python_has("torch", EXTERNAL_VENV_PYTHON)
        if not torch_state["available"]:
            torch_state = _python_has("torch", Path(sys.executable))
        status["weights"] = [{"path": str(item), "size_bytes": item.stat().st_size} for item in weights]
        status["dependency"] = {"torch": torch_state}
        if weights and torch_state["available"]:
            status["runtime"] = "ready"
            status["can_run_now"] = True
            status["run_mode"] = "funie_gan_pytorch"
        elif weights:
            status["runtime"] = "weights_ready_dependency_missing"
            status["notes"].append("FUnIE-GAN weights are downloaded locally, but PyTorch is not installed.")
        else:
            status["runtime"] = "missing_weights"
            status["notes"].append("FUnIE-GAN code is downloaded, but no local weight file was found.")

    elif repo_id in {"resolve-dctl", "utility-dctls"}:
        dctls = sorted(path.glob("**/*.dctl"))
        status["assets"] = {"dctl_files": len(dctls)}
        status["runtime"] = "index_ready"
        status["can_run_now"] = bool(dctls)
        status["run_mode"] = "dctl_index"

    elif repo_id in {"water-net-code", "all-in-one-underwater-enhancement", "fiveaplus-network", "ursct-sesr"}:
        weights = sorted(path.glob("**/*.pth")) + sorted(path.glob("**/*.ckpt")) + sorted(path.glob("**/*.h5"))
        status["weights"] = [{"path": str(item), "size_bytes": item.stat().st_size} for item in weights]
        status["runtime"] = "needs_weight_or_legacy_environment"
        status["notes"].append("Research code is downloaded, but a verified checkpoint/runtime path is still required.")

    else:
        status["notes"].append("Downloaded locally for inspection; no safe runtime adapter is enabled yet.")

    return status


def list_local_models() -> Dict[str, Any]:
    models = [_repo_runtime_status(repo) for repo in list_repositories()]
    return {
        "local_repo_root": str(LOCAL_REPO_ROOT),
        "models": models,
        "ready_count": sum(1 for item in models if item["can_run_now"]),
        "downloaded_count": sum(1 for item in models if item["download"]["exists"]),
    }


def _srgb_to_xyz(rgb: List[float]) -> List[float]:
    def linearize(value: float) -> float:
        value = max(0.0, min(1.0, value))
        return value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4

    r, g, b = [linearize(v) for v in rgb]
    return [
        r * 0.4124564 + g * 0.3575761 + b * 0.1804375,
        r * 0.2126729 + g * 0.7151522 + b * 0.0721750,
        r * 0.0193339 + g * 0.1191920 + b * 0.9503041,
    ]


def _xyz_to_lab(xyz: List[float]) -> List[float]:
    white = [0.95047, 1.0, 1.08883]

    def f(value: float) -> float:
        delta = 6 / 29
        return value ** (1 / 3) if value > delta ** 3 else value / (3 * delta ** 2) + 4 / 29

    fx, fy, fz = [f(component / white[index]) for index, component in enumerate(xyz)]
    return [116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)]


def _delta_e_76(lab_a: List[float], lab_b: List[float]) -> float:
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(lab_a, lab_b)))


def _run_builtin_colour_math(payload: Dict[str, Any]) -> Dict[str, Any]:
    sample_rgb = payload.get("sample_rgb") or [0.16, 0.42, 0.62]
    target_rgb = payload.get("target_rgb") or [0.42, 0.48, 0.50]
    sample_lab = _xyz_to_lab(_srgb_to_xyz([float(v) for v in sample_rgb]))
    target_lab = _xyz_to_lab(_srgb_to_xyz([float(v) for v in target_rgb]))
    delta_e = _delta_e_76(sample_lab, target_lab)
    return {
        "model": "colour-science-colour",
        "run_mode": "builtin_colour_math",
        "sample_rgb": sample_rgb,
        "target_rgb": target_rgb,
        "sample_lab": [round(v, 4) for v in sample_lab],
        "target_lab": [round(v, 4) for v in target_lab],
        "delta_e_76": round(delta_e, 4),
        "diagnosis": "large_shift" if delta_e >= 18 else "moderate_shift" if delta_e >= 8 else "small_shift",
    }


def _run_colour_science(payload: Dict[str, Any]) -> Dict[str, Any]:
    if not _python_has("colour", EXTERNAL_VENV_PYTHON)["available"]:
        return _run_builtin_colour_math(payload)

    script = r"""
import json
import sys
import colour

payload = json.loads(sys.stdin.read() or "{}")
sample_rgb = payload.get("sample_rgb") or [0.16, 0.42, 0.62]
target_rgb = payload.get("target_rgb") or [0.42, 0.48, 0.50]
sample_xyz = colour.sRGB_to_XYZ(sample_rgb)
target_xyz = colour.sRGB_to_XYZ(target_rgb)
sample_lab = colour.XYZ_to_Lab(sample_xyz)
target_lab = colour.XYZ_to_Lab(target_xyz)
delta_e = float(colour.delta_E(sample_lab, target_lab, method="CIE 1976"))
print(json.dumps({
    "model": "colour-science-colour",
    "run_mode": "colour_science_python",
    "colour_version": colour.__version__,
    "sample_rgb": sample_rgb,
    "target_rgb": target_rgb,
    "sample_lab": [round(float(v), 4) for v in sample_lab],
    "target_lab": [round(float(v), 4) for v in target_lab],
    "delta_e_76": round(delta_e, 4),
    "diagnosis": "large_shift" if delta_e >= 18 else "moderate_shift" if delta_e >= 8 else "small_shift",
}))
"""
    result = subprocess.run(
        [str(EXTERNAL_VENV_PYTHON), "-c", script],
        input=json.dumps(payload),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=20,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "colour science run failed")
    return json.loads(result.stdout)


def _run_dctl_index(repo_id: str) -> Dict[str, Any]:
    path = _repo_path(repo_id)
    files = sorted(path.glob("**/*.dctl"))
    return {
        "model": repo_id,
        "run_mode": "dctl_index",
        "dctl_file_count": len(files),
        "sample_files": [str(item.relative_to(path)) for item in files[:12]],
    }


def _run_funie_gan_probe() -> Dict[str, Any]:
    status = _repo_runtime_status({"id": "funie-gan", "name": "xahidbuffon/FUnIE-GAN", "category": "underwater_ai_enhancement"})
    if not status["can_run_now"]:
        return {
            "model": "funie-gan",
            "run_mode": status["run_mode"],
            "can_run_now": False,
            "runtime": status["runtime"],
            "notes": status["notes"],
        }

    python_path = Path(status["dependency"]["torch"]["python"])
    pytorch_root = _repo_path("funie-gan") / "PyTorch"
    model_path = pytorch_root / "models" / "funie_generator.pth"
    script = r"""
import json
import torch
from nets import funiegan

model = funiegan.GeneratorFunieGAN()
model.load_state_dict(torch.load("models/funie_generator.pth", map_location="cpu"))
model.eval()
with torch.no_grad():
    sample = torch.zeros(1, 3, 256, 256)
    sample[:, 1, :, :] = 0.35
    sample[:, 2, :, :] = 0.65
    output = model(sample)
print(json.dumps({
    "model": "funie-gan",
    "run_mode": "funie_gan_pytorch_probe",
    "model_path": "PyTorch/models/funie_generator.pth",
    "input_shape": list(sample.shape),
    "output_shape": list(output.shape),
    "output_min": round(float(output.min()), 6),
    "output_max": round(float(output.max()), 6),
    "output_mean": round(float(output.mean()), 6),
}))
"""
    result = subprocess.run(
        [str(python_path), "-c", script],
        cwd=str(pytorch_root),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=60,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "FUnIE-GAN probe failed")
    return json.loads(result.stdout)


def run_local_model(payload: Dict[str, Any]) -> Dict[str, Any]:
    model_id = str(payload.get("model_id") or "colour-science-colour")
    status = next((item for item in list_local_models()["models"] if item["id"] == model_id), None)
    if not status:
        raise ValueError(f"Unknown local model: {model_id}")
    if model_id == "colour-science-colour":
        result = _run_colour_science(payload)
    elif model_id == "funie-gan":
        result = _run_funie_gan_probe()
    elif model_id in {"resolve-dctl", "utility-dctls"}:
        result = _run_dctl_index(model_id)
    else:
        result = {
            "model": model_id,
            "run_mode": status["run_mode"],
            "can_run_now": status["can_run_now"],
            "runtime": status["runtime"],
            "notes": status["notes"],
        }
    log_event("runtime", "local_model_run", {"model_id": model_id, "run_mode": result["run_mode"]})
    return result
