---
title: "Coding Conventions"
category: coding
---
# Coding Conventions

Auto-generated from project analysis. Update manually as patterns evolve.

## Formatting
- Indentation: 4 spaces
- Line length: no strict limit, lines often exceed 120 chars
- Semicolons: no (Python)

## Naming
- Variables/functions: snake_case (e.g., `get_config`, `baseurl`, `pil2tensor`)
- Classes/types: PascalCase (e.g., `Comfly_Mj`, `ComflyBaseNode`, `OpenAISoraAPIPlus`)
- Constants: UPPER_SNAKE_CASE (e.g., `NODE_CLASS_MAPPINGS`, `NODE_DISPLAY_NAME_MAPPINGS`)
- Files: snake_case (e.g., `utils.py`, `nano_banana_zyx.py`)

## Imports
- Style: mixed (import module + from module import name)
- Order: stdlib → third-party → local (.utils, .Comfly)
- No path aliases

## Patterns
- Single-file monolithic structure: ~80+ node classes defined in `Comfly.py`
- Nodes inherit from `ComflyBaseNode` which provides shared HTTP polling logic
- Node registry: NODE_CLASS_MAPPINGS dict + NODE_DISPLAY_NAME_MAPPINGS dict
- API key via config file (`Comflyapi.json`) with get_config()/save_config() helpers
- Error handling: try/except with optional skip_error flag for graceful degradation
- Polling pattern: POST to API → poll task status → download result

## Entries
