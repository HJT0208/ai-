# Codex AI 广告短剧工作台

这是把对话中形成的AI广告短剧生产规则整理成的Codex可读取项目模板。把一个符合 `schemas/project.schema.json` 的 `project.json` 放入任意项目目录后运行：

```bash
python scripts/validate_workbench.py project.json
python scripts/compile_workbench.py project.json build/
```

`build/` 会按30秒分组和5秒片段输出视觉、对白、音频、图片槽位和工作流契约。视觉提示词与对白严格分离；无对白片段使用空对白数组；音乐默认关闭。

推荐与 produce-cid-ad-drama、deepwhite-screenwriting-v1、mad-story、deepwhite-image-prompt-builder、deepseek-video-script、apply-script-quality、manage-drama-resources 协同使用。
