---
title: "Architecture Constraints"
category: arch
---
# Architecture Constraints

Auto-generated from project structure. Update manually as architecture evolves.

## Module Structure
- Type: single-package ComfyUI custom node
- Package entry: `__init__.py` exports NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS, WEB_DIRECTORY
- Start: `__init__.py` auto-starts AiHelper background thread on import

## Key Modules
- `Comfly.py` — Main module (~1MB, ~23,200 lines). All 80+ node classes + base class + config helpers
- `utils.py` — Image conversion utilities (PIL ↔ tensor)
- `AiHelper.py` — aiohttp Web service for proxy/cache (runs in background thread)
- `nano_banana_zyx.py` — Custom user extension (not yet registered in NODE_CLASS_MAPPINGS)
- `web/` — Custom node UI (JavaScript)
- `docs/` — MJ style JSON references
- `workflow/` — ComfyUI workflow templates

## Layer Boundaries
- No formal layers — monolithic design
- `ComflyBaseNode` (base class) → individual node classes → API calls to `ai.t8star.org`
- Node classes are independent of each other; shared logic in `ComflyBaseNode`

## Dependency Rules
- `__init__.py` → `Comfly.py`
- `Comfly.py` → `utils.py`, `comfy.*`, `comfy_api.*`
- `nano_banana_zyx.py` → standalone (imports `Comfly.py` utilities)
- `AiHelper.py` → aiohttp web server, independent of node logic
- All external API calls route through `https://ai.t8star.org`

## Technology Constraints
- Runtime: Python >= 3.10
- Framework: ComfyUI custom nodes specification
- Module system: Python packages (with `__init__.py`)
- Key dependency: torch, openai, aiohttp (see pyproject.toml)

## Entries
