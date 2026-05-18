---
title: "Learnings"
category: learning
---
# Learnings

Bugs, gotchas, and lessons learned during development.
Add entries with: `/spec-add learning <description>`

## Entries

<spec-entry category="learning" keywords="comfyui, node, register, import, mappings" date="2026-05-18" source="milestone-complete">

### ComfyUI 节点注册三步模式

要让一个外部 `.py` 文件的节点类接入 ComfyUI，需要在主模块 `Comfly.py` 中完成三步：
1. `from .module_name import ClassName` — 导入节点类
2. `NODE_CLASS_MAPPINGS` 字典追加 `"ClassName": ClassName`
3. `NODE_DISPLAY_NAME_MAPPINGS` 字典追加 `"ClassName": "Display Name"`

Milestone: phase-1-节点注册

</spec-entry>
