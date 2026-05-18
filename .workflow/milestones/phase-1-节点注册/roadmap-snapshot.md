# Roadmap: Comfyui-zhenzhen

## Overview

将 `nano_banana_zyx.py` 的 `Comfly_nano_banana2_edit_ZYX` 节点接入 ComfyUI 节点系统，使其在 ComfyUI 中可见可用。

## Phases

**Minimum-phase principle:** Default 1 phase. Only add phases for hard dependencies.

- [x] **Phase 1: 节点注册** - 在 Comfly.py 中 import 并注册节点

## Phase Details

### Phase 1: 节点注册
**Goal**: `Comfly_nano_banana2_edit_ZYX` 节点在 ComfyUI 中可见，可正常创建、配置、执行
**Depends on**: Nothing (first phase)
**Requirements**: Active REQ-1: 将 `nano_banana_zyx.py` 节点接入 ComfyUI
**Success Criteria** (what must be TRUE):
  1. 重启 ComfyUI 后，节点列表中可见 "Zhenzhen Nano Banana 2 Edit ZYX"
  2. 节点可正常创建、配置参数
  3. text2img 和 img2img 模式均可执行图片生成

## Scope Decisions

- **In scope**: 在 Comfly.py 中 import 并注册 Comfly_nano_banana2_edit_ZYX
- **Deferred**: 代码重构、合并重复函数、域名统一
- **Out of scope**: 修改节点功能逻辑、新建节点

## Progress

| Phase | Status | Completed |
|-------|--------|-----------|
| 1. 节点注册 | Completed | 2026-05-18 |
