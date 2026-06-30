# GitHub Repo Index for AI Color Workspace

This index records external GitHub projects that may help the underwater color workbench.

The rule for this project is conservative: external repositories are references first. Runtime integration should happen only through optional adapters that emit JSON metrics, preset suggestions, or versioned parameter snapshots. Preview and export must continue to share the same final grade snapshot.

## Phase 1: Safe References

### colour-science/colour

- URL: https://github.com/colour-science/colour
- Use for: color-space conversion, Lab/XYZ/RGB analysis, Delta E, illuminants, and scoring.
- Workbench fit: Analyzer and Scorer.
- Integration pattern: optional metrics adapter returning JSON.

### wangyanckxx/Single-Underwater-Image-Enhancement-and-Color-Restoration

- URL: https://github.com/wangyanckxx/Single-Underwater-Image-Enhancement-and-Color-Restoration
- Use for: traditional underwater enhancement method references such as white balance, CLAHE, gamma, and channel restoration.
- Workbench fit: preset candidates and planner hints.
- Integration pattern: convert method ideas into versioned preset JSON after license review.

### thatcherfreeman/utility-dctls

- URL: https://github.com/thatcherfreeman/utility-dctls
- Use for: DCTL parameter design references, tone mapping, printer lights, false color, and ColorChecker utilities.
- Workbench fit: DCTL_INDEX design and parameter schema.
- Integration pattern: index and learn structure first; do not copy shader code before license review.

## Phase 2: Optional AI Reference Preview

### xahidbuffon/FUnIE-GAN

- URL: https://github.com/xahidbuffon/FUnIE-GAN
- Use for: AI underwater enhancement reference previews and quality metrics such as UIQM, SSIM, and PSNR.
- Workbench fit: optional comparison render, never the only export path.
- Integration pattern: offline adapter that outputs a reference image plus JSON metrics.

## Phase 3+: Color Management and Rendering

### AcademySoftwareFoundation/OpenColorIO

- URL: https://github.com/AcademySoftwareFoundation/OpenColorIO
- Use for: OCIO configs, ACES-style transforms, LUT pipeline consistency, and display transforms.
- Workbench fit: future preview/export/DaVinci handoff consistency.

### haasn/libplacebo

- URL: https://github.com/haasn/libplacebo
- Use for: GPU rendering primitives, tone mapping, ICC, shaders, scaling, and video processing.
- Workbench fit: future native render backend research.

## API

The local V2 API exposes the registry at:

```text
GET /external-repos
```

Planner results also include:

```json
{
  "external_capabilities": [],
  "external_warnings": [],
  "external_next_step": "..."
}
```

## Additional Model Knowledge Added

### Li-Chongyi/Water-Net_Code

- URL: https://github.com/Li-Chongyi/Water-Net_Code
- Use for: Water-Net benchmark/reference ideas and paired underwater evaluation.
- Integration pattern: benchmark/reference route first because the dependency stack is legacy.

### VITA-Group/All-In-One-Underwater-Image-Enhancement-using-Domain-Adversarial-Learning

- URL: https://github.com/VITA-Group/All-In-One-Underwater-Image-Enhancement-using-Domain-Adversarial-Learning
- Use for: domain-adversarial all-in-one underwater enhancement references across degradation types.
- Integration pattern: model comparison idea for blue/green/murky classifications; license review before code reuse.

### Owen718/FiveAPlus-Network

- URL: https://github.com/Owen718/FiveAPlus-Network
- Use for: lightweight local/offline underwater enhancement preview research.
- Integration pattern: optional fast preview candidate after tests on real Timo clips.

### TingdiRen/URSCT-SESR

- URL: https://github.com/TingdiRen/URSCT-SESR
- Use for: underwater enhancement plus super-resolution research.
- Integration pattern: detail-recovery reference only; do not mix super-resolution into faithful export without review.

### jedypod/open-display-transform

- URL: https://github.com/jedypod/open-display-transform
- Use for: display transforms, tone mapping, SDR/HDR, wide gamut, and LUT handoff research.
- Integration pattern: preview/export display-transform boundary reference.

### xtremestuff/resolve-dctl

- URL: https://github.com/xtremestuff/resolve-dctl
- Use for: additional DaVinci Resolve DCTL organization and shader reference patterns.
- Integration pattern: index concepts and file organization only until license review.
