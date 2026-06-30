from copy import deepcopy
from typing import Any, Dict, List


_REPOSITORIES: List[Dict[str, Any]] = [
    {
        "id": "colour-science-colour",
        "name": "colour-science/colour",
        "url": "https://github.com/colour-science/colour",
        "category": "color_science",
        "priority": 1,
        "license": "BSD-3-Clause",
        "fit": "Use for Lab/XYZ/RGB conversions, Delta E, illuminants, and objective color diagnostics.",
        "integration_phase": "phase_1_analyzer_scorer",
        "adapter_hint": "Wrap as a metrics adapter that returns JSON only; do not change preview pixels directly.",
        "tags": ["analysis", "scoring", "white_balance", "delta_e", "color_space"],
        "risks": ["Adds a third-party dependency if imported directly; keep optional until pinned."],
    },
    {
        "id": "single-underwater-image-enhancement",
        "name": "wangyanckxx/Single-Underwater-Image-Enhancement-and-Color-Restoration",
        "url": "https://github.com/wangyanckxx/Single-Underwater-Image-Enhancement-and-Color-Restoration",
        "category": "underwater_traditional_methods",
        "priority": 2,
        "license": "unknown",
        "fit": "Reference traditional underwater enhancement candidates such as white balance, CLAHE, gamma, and channel restoration.",
        "integration_phase": "phase_1_preset_candidates",
        "adapter_hint": "Extract method names and parameter ideas into versioned preset JSON; avoid vendoring code until license is clarified.",
        "tags": ["underwater", "preset", "white_balance", "clahe", "gamma", "red_channel"],
        "risks": ["License is not explicit; use as reference first, not direct copy."],
    },
    {
        "id": "funie-gan",
        "name": "xahidbuffon/FUnIE-GAN",
        "url": "https://github.com/xahidbuffon/FUnIE-GAN",
        "category": "underwater_ai_enhancement",
        "priority": 3,
        "license": "custom_or_unspecified",
        "fit": "Fast underwater enhancement and UIQM/SSIM/PSNR evaluation ideas for AI reference previews.",
        "integration_phase": "phase_2_ai_reference_preview",
        "adapter_hint": "Run as an offline optional reference renderer; never make it the only export path.",
        "tags": ["underwater", "ai_preview", "uiqm", "ssim", "psnr", "reference_render"],
        "risks": ["Model output may over-style footage; dependency/runtime cost is high."],
    },
    {
        "id": "utility-dctls",
        "name": "thatcherfreeman/utility-dctls",
        "url": "https://github.com/thatcherfreeman/utility-dctls",
        "category": "dctl_reference",
        "priority": 4,
        "license": "check_before_copying",
        "fit": "Reference DCTL parameter structure for tone mapping, printer lights, false color, ColorChecker, and Resolve utilities.",
        "integration_phase": "phase_1_dctl_index",
        "adapter_hint": "Use to design DCTL_INDEX metadata and parameter schema; do not copy shaders without license review.",
        "tags": ["dctl", "davinci", "tone_mapping", "printer_lights", "false_color", "colorchecker"],
        "risks": ["DCTL code must be license-reviewed before vendoring."],
    },
    {
        "id": "opencolorio",
        "name": "AcademySoftwareFoundation/OpenColorIO",
        "url": "https://github.com/AcademySoftwareFoundation/OpenColorIO",
        "category": "color_management",
        "priority": 5,
        "license": "BSD-3-Clause",
        "fit": "Professional color management, OCIO configs, ACES-style transforms, and LUT pipeline consistency.",
        "integration_phase": "phase_3_color_management",
        "adapter_hint": "Keep as a future color-management boundary between preview, export, LUT, and Resolve handoff.",
        "tags": ["ocio", "aces", "lut", "color_management", "display_transform"],
        "risks": ["Powerful but heavy; not needed for the first analyzer-only pass."],
    },
    {
        "id": "libplacebo",
        "name": "haasn/libplacebo",
        "url": "https://github.com/haasn/libplacebo",
        "category": "gpu_rendering",
        "priority": 6,
        "license": "LGPL-2.1-or-later",
        "fit": "GPU video/image rendering primitives, tone mapping, ICC profiles, shaders, and high-quality scaling.",
        "integration_phase": "phase_4_render_backend",
        "adapter_hint": "Research only until the workbench needs a native high-performance renderer.",
        "tags": ["gpu", "render", "tone_mapping", "icc", "shader", "video"],
        "risks": ["Native integration cost is high and would touch playback/export architecture."],
    },

    {
        "id": "water-net-code",
        "name": "Li-Chongyi/Water-Net_Code",
        "url": "https://github.com/Li-Chongyi/Water-Net_Code",
        "category": "underwater_benchmark_model",
        "priority": 7,
        "license": "research_code_check_before_use",
        "fit": "Classic underwater image enhancement benchmark and Water-Net reference for paired evaluation ideas.",
        "integration_phase": "phase_2_benchmark_reference",
        "adapter_hint": "Use as a benchmark/reference route first; TensorFlow 1.x era dependencies make direct runtime integration expensive.",
        "tags": ["underwater", "benchmark", "waternet", "tensorflow", "paired_data", "reference_render"],
        "risks": ["Legacy dependency stack; verify license and runtime before any direct adapter."],
    },
    {
        "id": "all-in-one-underwater-enhancement",
        "name": "VITA-Group/All-In-One-Underwater-Image-Enhancement-using-Domain-Adversarial-Learning",
        "url": "https://github.com/VITA-Group/All-In-One-Underwater-Image-Enhancement-using-Domain-Adversarial-Learning",
        "category": "underwater_ai_enhancement",
        "priority": 8,
        "license": "unknown",
        "fit": "Domain-adversarial all-in-one underwater enhancement reference for different water degradation types.",
        "integration_phase": "phase_2_ai_reference_preview",
        "adapter_hint": "Keep as a model-comparison idea for blue/green/murky water classes; do not vendor code without license review.",
        "tags": ["underwater", "domain_adaptation", "ai_preview", "degradation_type"],
        "risks": ["Older research code and unclear license; use as paper/model reference first."],
    },
    {
        "id": "fiveaplus-network",
        "name": "Owen718/FiveAPlus-Network",
        "url": "https://github.com/Owen718/FiveAPlus-Network",
        "category": "lightweight_underwater_ai",
        "priority": 9,
        "license": "unknown",
        "fit": "Lightweight underwater enhancement network reference; useful for future local/offline low-latency preview research.",
        "integration_phase": "phase_2_lightweight_ai_preview",
        "adapter_hint": "Evaluate as an optional fast preview candidate only after quality tests on Timo underwater clips.",
        "tags": ["underwater", "lightweight", "ai_preview", "low_latency"],
        "risks": ["Small model does not guarantee stable color taste; validate on real footage."],
    },
    {
        "id": "ursct-sesr",
        "name": "TingdiRen/URSCT-SESR",
        "url": "https://github.com/TingdiRen/URSCT-SESR",
        "category": "underwater_enhancement_super_resolution",
        "priority": 10,
        "license": "MIT",
        "fit": "Underwater enhancement plus super-resolution reference for future detail recovery and export-quality research.",
        "integration_phase": "phase_3_detail_recovery_research",
        "adapter_hint": "Keep separate from color grading; if tested, output should be a reference render with JSON metrics, not overwrite grade parameters.",
        "tags": ["underwater", "super_resolution", "detail_recovery", "ai_preview"],
        "risks": ["Super-resolution can invent detail; unsuitable for faithful grading export without review."],
    },
    {
        "id": "open-display-transform",
        "name": "jedypod/open-display-transform",
        "url": "https://github.com/jedypod/open-display-transform",
        "category": "display_transform",
        "priority": 11,
        "license": "check_before_use",
        "fit": "Display transform and tone mapping reference for SDR/HDR, wide gamut, and viewing consistency.",
        "integration_phase": "phase_3_display_transform_research",
        "adapter_hint": "Use as a design reference for preview/export display transform boundaries and LUT handoff notes.",
        "tags": ["display_transform", "tone_mapping", "hdr", "sdr", "wide_gamut", "lut"],
        "risks": ["Should not be mixed into underwater correction before preview/export color pipeline is explicit."],
    },
    {
        "id": "resolve-dctl",
        "name": "xtremestuff/resolve-dctl",
        "url": "https://github.com/xtremestuff/resolve-dctl",
        "category": "dctl_reference",
        "priority": 12,
        "license": "check_before_copying",
        "fit": "Additional DaVinci Resolve DCTL reference collection for learning shader organization and Resolve-specific patterns.",
        "integration_phase": "phase_1_dctl_index",
        "adapter_hint": "Index concepts and file organization only; license-review before copying or generating derivative DCTL code.",
        "tags": ["dctl", "davinci", "resolve", "shader_reference"],
        "risks": ["DCTL code copying has license and taste risks; keep as reference metadata first."],
    },
]


def list_repositories() -> List[Dict[str, Any]]:
    return deepcopy(sorted(_REPOSITORIES, key=lambda item: item["priority"]))


def recommend_for_analysis(analyzer_result: Dict[str, Any]) -> Dict[str, Any]:
    scene = str(analyzer_result.get("scene") or "").lower()
    water = str(analyzer_result.get("water") or "").lower()
    skin = bool(analyzer_result.get("skin"))
    noise = str(analyzer_result.get("noise") or "").lower()

    selected_ids = {"colour-science-colour", "single-underwater-image-enhancement", "utility-dctls"}
    warnings = [
        "Treat every GitHub project as an external reference until dependency, license, and image-quality tests pass.",
        "Keep preview/export consistency by converting external output into JSON grade snapshots before touching pixels.",
    ]

    if scene == "underwater" and water in {"blue", "green", "murky", "unknown"}:
        selected_ids.add("funie-gan")
    if skin:
        selected_ids.add("opencolorio")
    if noise in {"medium", "high"}:
        selected_ids.add("funie-gan")

    recommendations = [repo for repo in list_repositories() if repo["id"] in selected_ids]
    return {
        "recommendations": recommendations,
        "warnings": warnings,
        "next_step": "Create optional adapters that emit JSON metrics/preset suggestions before adding runtime dependencies.",
    }


def external_knowledge_models() -> List[Dict[str, Any]]:
    models = []
    for repo in list_repositories():
        models.append(
            {
                "name": f"github:{repo['name']}",
                "type": "external_knowledge",
                "status": "reference_only",
                "source_id": repo["id"],
                "category": repo["category"],
                "integration_phase": repo["integration_phase"],
                "url": repo["url"],
                "fit": repo["fit"],
                "adapter_hint": repo["adapter_hint"],
                "risks": repo["risks"],
            }
        )
    return models
