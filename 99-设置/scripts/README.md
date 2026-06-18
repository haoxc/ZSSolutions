# Vault Scripts

此目录存放 Vault 相关的自动化脚本。

## 运行方式

所有 Python 脚本通过 `uv` 运行，不依赖系统 pip/conda：

```bash
# 单文件直接跑（自动装依赖）
uv run --with httpx script.py

# 或先声明依赖再跑
uv add requests
uv run script.py
```

## 环境

| 环境 | Python | 用途 |
|------|--------|------|
| Hermes venv | 3.11.15 | Hermes Agent 自身 |
| Anaconda3 | 3.13.9 | LiteLLM Gateway |
| uv（推荐） | 3.11 / 3.13 | 日常脚本，按需创建 venv |

**原则**：新脚本一律用 uv，不污染 Hermes 和 Anaconda 环境。

## 目录规范

```
scripts/
  README.md           ← 本文件
  shared/             ← 跨平台通用工具脚本
  windows/            ← Windows 专用（路径/进程/注册表相关）
  macos/              ← macOS 专用（launchd/plist/Homebrew 相关）
```

脚本顶部加注释说明依赖：
```python
# deps: httpx, rich
# run:  uv run script.py
```
