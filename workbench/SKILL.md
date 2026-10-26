---
name: codex-ai-ad-drama-workbench
description: 将用户的中文AI广告短剧需求编译为可供Codex读取和复用的项目工作台，统筹大纲、剧本、5秒分段、人物面部锁定、服装与场景连续性、Picture槽位、图像提示词、视频提示词、对白与音频隔离，并在交付前执行结构与安全自检。
---

# Codex AI 广告短剧工作台

本技能用于制作中文AI广告短剧的可执行项目包。它把创意需求编译为机器可读的 `project.json`、按30秒分组的脚本、按5秒切片的提示词、图片槽位清单、角色与商品锁定卡，以及自检报告。默认由用户自己的ComfyUI或视频工作流生成成片；本技能只生成文字、结构化数据、静态图提示词和需要的参考图，不擅自提交、暂停、删除或改动用户队列。

## 固定工作约束

- 画幅默认为9:16竖屏；时间轴按每5秒一个片段编排，30秒为一个组。
- 每个片段必须有 `visual_prompt`、`dialogue`、`audio`、`picture_slots`、`continuity` 五个独立字段。
- `visual_prompt` 与 `audio` 绝不能写成可朗读台词；纯对白只放在 `dialogue.lines`。
- 没有对白时，`dialogue.lines` 必须为空数组；`audio.music` 必须为 `false`；不得用“无配乐”代替空字段。
- 默认禁止配乐、环境音乐、音效垫、自动旁白和字幕朗读。只保留脚本明确要求的对白、脚步声、开关门声、轻微呼吸声等。
- 品牌名、品牌字样、虚构品牌水印默认禁止；无品牌商品只描述颜色、材质、包装结构、容量和功能展示。
- 人物身份由 `face_lock_id` 锁定；换装只创建 `wardrobe_lock_id`，不得用服装参考图的旧脸覆盖已锁定面部。
- 连续片段必须检查人物的左右朝向、持物手、动作起止状态、服装、妆面、痘痘/瑕疵和商品状态。
- 产品效果必须按动作顺序呈现：拿取/挤出 → 接触皮肤 → 推开/起泡 → 冲洗或擦净 → 完成后的效果。不能先出现结果再补做动作。
- 敏感或亲密剧情使用成年角色、清晰的叙事镜头和非露骨表达；不制作未成年人性内容或露骨色情内容。

## 标准执行顺序

1. 读取需求，建立 `project.json`：题材、受众、时长、产品、禁项、音频策略、画幅和交付目录。
2. 输出全片大纲与因果链，标记每个30秒组的目标、冲突、转折和产品露出位置。
3. 建立角色卡：固定面部特征、可变服装、发型、鞋履、年龄为成年、表情状态和禁改项。
4. 建立场景卡与商品卡，给每张静态图分配稳定 `asset_id`。
5. 生成30秒分组脚本，再拆为5秒片段；每段只描述一个可拍摄瞬间，动作有明确起点和终点。
6. 生成静态图提示词和视频提示词。图片槽位只负责参考图职责，不把图片说明写进对白。
7. 生成分区字段：视觉导演稿、纯对白、音频清单、负面约束、槽位映射。
8. 执行 `scripts/validate_workbench.py` 和 `scripts/compile_workbench.py`；失败项必须修复后再交付。
9. 交付时提供文件夹、可复制文本、JSON索引和自检报告；若用户要求网站，再将相同JSON渲染为可检索的静态页面。

## 字段契约

见 `schemas/project.schema.json`。核心结构如下：

```json
{
  "project": {"id":"", "title":"", "aspect_ratio":"9:16", "duration_sec":90},
  "audio_policy": {"music":false, "allow_only":["dialogue","footsteps","door","breath"]},
  "characters": [{"character_id":"", "face_lock_id":"", "wardrobe_lock_id":"", "adult":true}],
  "assets": [{"asset_id":"", "kind":"character|scene|product", "path":"", "approved":false}],
  "segments": [{
    "segment_id":"A01", "start_sec":0, "end_sec":5,
    "visual_prompt":"",
    "dialogue":{"lines":[],"speaker":"","delivery":""},
    "audio":{"music":false,"effects":[],"speech":[]},
    "picture_slots":[{"slot":"Picture0","asset_id":""}],
    "continuity":{"before":"","after":"","locked":[""]}
  }]
}
```

## 提示词写法

视频提示词要写成导演可执行的连续动作：主体位置、景别、镜头高度、焦段感、运镜路径、光线、表情变化、手部动作、视线方向、服装、材质、景深、前后承接和结束状态。不要写“模型请说……”；台词只写进 `dialogue.lines`，并在 `audio.speech` 里写清楚声线、语速、停顿和情绪。

面部提示词分为两层：固定身份层（脸型、眉眼、鼻唇、发际线、可见识别特征）和动态情绪层（触发→眉眼变化→视线→嘴角/下颌→呼吸→收束）。用户指定的痘痘、雀斑、皱纹或妆面必须在对应时间段保持，除非脚本明确完成清洁、卸妆或变妆。

## 自检门槛

- 时间段连续、无重叠、无空洞；每段长度为5秒。
- 所有片段都有五个核心字段；纯静音段无对白、无语音、无配乐。
- `visual_prompt` 不含引号包裹的对白句，不含“旁白朗读”等混合指令。
- 每个 Picture 槽位都指向存在的 `asset_id`，且职责明确。
- 角色年龄均为成年；同一 `face_lock_id` 在连续剧情中不漂移。
- 产品效果顺序与剧情动作一致；品牌文字和水印禁项通过。
- 详细提示词字数按项目要求验证；本技能不默认硬编码2000字，但用户要求时由校验器执行。

## 交付目录

```text
project/
  project.json
  00_README.md
  01_outline/outline.md
  02_script/30s_groups/*.md
  03_segments/5s/*.json
  04_prompts/visual/*.txt
  04_prompts/dialogue/*.txt
  04_prompts/audio/*.txt
  05_assets/asset_manifest.json
  06_workflow/workflow_contract.json
  07_validation/validation_report.json
```
