# DCTL Index

Current scan result: no real `.dctl` files were found in the active workspace.

The MVP therefore creates versioned DCTL parameter presets. Real DaVinci Resolve `.dctl` shader files should be added later and indexed here.

## Categories

### 基础调色

No real DCTL file yet.

### 海水/潜水

| Name | Version | File | Purpose | Scenario |
|---|---:|---|---|---|
| underwater_balance | 1.0 | `../dctl/params/underwater_balance.v1.json` | underwater baseline balance | blue/green water repair |
| deep_blue | 1.0 | `../dctl/params/deep_blue.v1.json` | deep blue water shaping | blue water / deep scenes |

### 人像肤色

| Name | Version | File | Purpose | Scenario |
|---|---:|---|---|---|
| skin_protect | 1.0 | `../dctl/params/skin_protect.v1.json` | protect warm subject tones | divers, portraits, exposed skin |

### 电影感

No real DCTL file yet.

### 测试/实验版本

No real DCTL file yet.

## Versioning

- Real DCTL files must include name and version in filename.
- Parameter presets must include `name`, `version`, `category`, and `parameters`.
- Deprecated DCTL files should not be deleted immediately; move them to an archive folder with a note.
