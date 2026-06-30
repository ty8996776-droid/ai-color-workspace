# Release Checklist

Use this checklist for the first public GitHub release.

## v0.1.0 MVP Gate

- [ ] Fresh clone succeeds.
- [ ] `python3 -m unittest discover -s tests -v` passes.
- [ ] `python3 -m backend.server` starts on `http://127.0.0.1:8790`.
- [ ] `docs/DEMO.md` curl flow works from `/analyze` through `/history`.
- [ ] README states the MVP limits clearly.
- [ ] No private footage, `.env`, API keys, private keys, SQLite databases, or logs are included.
- [ ] Third-party downloaded projects under `third_party/` are not included in the source package.
- [ ] Release notes link to the demo and API docs.

## Package Command

Build a local source archive without runtime output or private material:

```bash
bash scripts/build_release_package.sh v0.1.0
```

The script writes to `output/releases/`, which is ignored by Git.

## GitHub Release Draft

Title:

```text
v0.1.0 - Runnable MVP architecture
```

Short description:

```text
First public MVP of the AI Color Workspace foundation: local JSON API, analyzer/planner/DCTL/scorer/memory loop, demo docs, and conservative external GitHub knowledge registry.
```

Attach:

- `ai-color-workspace-v0.1.0-source.zip`

Do not attach private footage, local model downloads, `.env` files, or generated logs.
