# 项目协作规则

每次完成任务后，更新 `.gitignore`、`AGENTS.md`、`README.md`，保持内容精简、准确、不过度扩写。

## 项目背景

- 本仓库是 ComfyUI 自定义节点包。
- 修改节点时保持 `NODE_CLASS_MAPPINGS` 和 `NODE_DISPLAY_NAME_MAPPINGS` 稳定。
- 重命名或迁移节点类时，保留旧节点 key，避免旧 workflow 失效。
- 优先做小步、低风险、兼容性优先的改动。

## 代码要求

- 遵循现有导入风格、命名方式和文件组织。
- 避免循环导入；抽离节点时，公共逻辑优先放到独立工具模块。
- 不做无关重构，不覆盖已有未提交改动。
- 新增逻辑应简单直接，除非确有必要，不引入复杂抽象。

## 验证要求

- Python 文件改动后优先运行语法检查，例如：
  `python -m py_compile Comfly.py nano_banana_zyx.py`
- 节点注册变更后，检查新旧 key 和显示名是否都正确。
- 涉及运行时行为时，尽量用 ComfyUI 启动验证。

## 敏感文件

- 不提交 `Comflyapi.json`、`.env`、API key、Bearer token、签名 URL、缓存文件或构建压缩包。
- workflow 示例只有在不包含真实密钥、私有资源、签名链接时才可入库。
- 示例密钥必须使用明显占位符，例如 `REPLACE_WITH_API_KEY`。

## Git 规则

- 视已有未提交改动为他人或用户的工作成果。
- 不回滚无关文件。
- 只暂存当前任务直接相关文件，优先使用 `git add <具体文件>`。
