# Project: Comfyui-zhenzhen

## What This Is

贞贞的 AI 工坊 — ComfyUI 自定义节点插件，通过 `ai.t8star.org` 后端代理，提供平价的海外 AI 模型 API（图像生成、视频生成、音乐生成等）。Fork 自用版本。

## Core Value

提供最稳定的 ComfyUI 节点体验。优先考虑轮询稳定性、报错准确传达、节点可靠性。

## Requirements

### Validated

- 84 个 ComfyUI 节点，覆盖 16 个模型组（Midjourney、OpenAI Sora/GPT、Flux、Gemini、Qwen、Suno、Vidu、Grok、MiniMax、WanX、Fal.ai 等）
- API 代理通过 `https://ai.t8star.org`
- Fal 轮询逻辑已重写（2026-05-17），报错可正确中断前端运行
- 图片 Tensor/PIL 转换工具（utils.py）
- 后台 AI Helper Web 服务（AiHelper.py）
- Web 前端自定义节点界面

### Active

- [ ] 将 `nano_banana_zyx.py` 接入 ComfyUI 节点系统
- [ ] 所有节点的轮询时间保持 5 秒

### Out of Scope

(None yet)

## Context

Fork 自他人项目，仅供个人使用。偏好 5 秒轮询间隔（原项目为 10 秒）。项目持续更新，最新版本 1.6.1。

## Constraints

- **ComfyUI 生态**: 必须兼容 ComfyUI 自定义节点规范（NODE_CLASS_MAPPINGS + NODE_DISPLAY_NAME_MAPPINGS）

## Tech Stack

- **Language**: Python 3
- **Framework**: ComfyUI custom nodes
- **Key Dependencies**: torch, numpy, Pillow, openai, aiohttp, requests, transformers, opencv-python
- **Backend Proxy**: https://ai.t8star.org
- **Frontend**: web/ (JavaScript)

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| 轮询间隔 5 秒 | 个人偏好更快响应 | — Active |
| Fork 自用 | 个人定制需求 | — Active |

## Stakeholders

- zhangyi196（主维护者/使用者）

---
*Last updated: 2026-05-18 after initialization*
