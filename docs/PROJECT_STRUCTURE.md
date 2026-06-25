# Project Structure

The active workspace is not a conventional repository. The existing platform is mainly a local single-file workbench:

`/Users/timo/Desktop/视频文件/Timo水下调色工作台.html`

AI Color Workspace V2 is added as a new isolated folder:

```text
ai-color-workspace/
├── backend/
├── frontend/
├── ai/
│   ├── analyzer/
│   ├── planner/
│   ├── dctl_engine/
│   ├── scorer/
│   ├── memory/
│   └── prompt/
├── dctl/
│   └── params/
├── lut/
├── dataset/
├── output/
├── docs/
└── tests/
```

This keeps the existing workbench stable and makes V2 easy to remove or migrate.

## Git Status

`/Users/timo/Desktop/视频文件` is not currently a Git repository. Branch creation and commit were therefore not possible in this folder.

To avoid committing video素材 and `.env.local`, `ai-color-workspace/` is initialized as its own Git repository on:

`feature/ai-color-workspace-v2`
