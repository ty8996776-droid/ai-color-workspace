# Investor Brief

## Project

AI Color Workspace is an open-source foundation for a modular AI color grading platform focused first on underwater video and photo workflows.

Repository:

https://github.com/ty8996776-droid/ai-color-workspace

## One-Line Positioning

An AI-assisted color grading workspace that helps underwater creators analyze footage, plan grading nodes, generate versioned parameters, score results, and later connect real segmentation, DCTL/LUT generation, and DaVinci-style workflows.

## Current Stage

This repository is an MVP platform foundation. It is intentionally not presented as a finished automatic grading product.

Current working foundation:

- Analyzer Agent
- Planner Agent
- DCTL parameter engine
- Scorer Agent
- SQLite Memory Agent
- Prompt file management
- JSON API service
- DCTL parameter index
- Unit tests
- Public README, MIT license, and NOTICE

## Why This Can Matter

Underwater footage is hard to grade because water absorbs red light, shifts color balance, reduces contrast, adds haze, and makes skin protection difficult. Many divers, instructors, dive shops, and content creators need faster first-pass correction before manual editing or DaVinci Resolve finishing.

The project focuses on a specific, painful niche instead of trying to become a general video editor.

## Target Users

- Recreational divers who want better-looking clips quickly.
- Dive instructors and dive shops handling client media.
- Underwater photographers and videographers.
- Creators who need social-ready water color correction.
- DaVinci Resolve users who want AI-assisted node planning and parameter suggestions.

## Product Direction

Short term:

- Keep the current open-source V2 architecture stable.
- Connect the V2 API back into the existing local underwater color workbench.
- Add real frame extraction and lightweight mask diagnostics.
- Build an evaluation dataset from real underwater samples.

Mid term:

- Add water/person/highlight/sand/coral-fish segmentation.
- Add MediaPipe or similar person protection.
- Prototype SAM 2 or equivalent object mask workflows.
- Add DaVinci handoff reports and real DCTL/LUT export paths.

Long term:

- Keep a useful open-source foundation.
- Offer paid cloud or local Pro services for advanced analysis, segmentation, batch processing, and commercial delivery workflows.

## Possible Business Models

- Open-source foundation plus paid AI service.
- Pro version for batch processing, higher-quality analysis, advanced masks, and export.
- Paid LUT/DCTL packs and DaVinci workflow templates.
- Custom workflow development for dive shops, creators, and media teams.
- Training material for underwater color grading workflows.

## Current Moat

- Domain focus: underwater video, not generic color grading.
- Workflow focus: analysis, planning, scoring, memory, and DaVinci handoff.
- Real creator context: built around actual underwater shooting and grading problems.
- Architecture prepared for learning loop and future segmentation.

## Current Gaps

- No real visual model is bundled yet.
- No production DCTL shader generation yet.
- No real video rendering pipeline in V2 yet.
- No usage analytics or download traction yet.
- No monetization layer yet.

## Metrics To Track

- GitHub stars
- Forks
- Watchers
- Issues opened by real users
- Pull requests
- Partnership or investment issue submissions
- Release asset downloads after releases exist
- Demo video views and inbound messages
- Number of real underwater samples evaluated

## Partnership / Investment Contact Path

For public collaboration or investment interest, open an issue using the `Investment / Partnership Interest` issue template.

Do not post private financial data, passwords, API keys, or confidential documents in public GitHub issues.

## Suggested Next Milestones Before Serious Fundraising

1. Publish a short demo video showing the existing workbench and V2 architecture.
2. Connect V2 API into the current workbench UI.
3. Add at least 30 real underwater sample evaluations.
4. Publish a first Release with a runnable MVP package.
5. Add screenshots, demo GIF, and roadmap checkboxes to README.
6. Collect 5-10 real user feedback items from divers or creators.

