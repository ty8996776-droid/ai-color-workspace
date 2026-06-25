# DCTL Index

This directory tracks DCTL-related parameter presets for AI Color Workspace V2.

No real `.dctl` shader file was found in the current workspace scan. The current MVP therefore stores versioned parameter presets under `dctl/params/` and keeps actual DCTL shader generation for a later phase.

| Name | Version | Category | Scenario | File |
|---|---:|---|---|---|
| underwater_balance | 1.0 | 海水/潜水 | underwater blue/green balance baseline | `params/underwater_balance.v1.json` |
| deep_blue | 1.0 | 海水/潜水 | deep blue water cleanup | `params/deep_blue.v1.json` |
| skin_protect | 1.0 | 人像肤色 | protect diver skin/subject warm tones | `params/skin_protect.v1.json` |

## Version Rule

- New parameter versions use `<name>.v<major>.json`.
- Real DCTL shader files should use `<name>_v<major>_<minor>.dctl`.
- Experimental files must include `experimental` in metadata or filename.
