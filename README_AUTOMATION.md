# 90秒 AI 广告漫剧按需流程

Windows 本地运行器，每次生成 3 组×30 秒、每组 6 个 5 秒段，固定 9:16。默认只生成脚本和提示词；只有 `--run` 才向 ComfyUI `/prompt` 提交任务。运行器只轮询 `/history`，不调用取消或删除接口。

先从 ComfyUI 导出 API workflow JSON，在文本字段使用 `{{PROMPT}}`，图片字段使用 `{{IMAGE}}`。运行：

```powershell
python ai90\run_pipeline.py --premise "女儿发现父亲隐瞒多年的秘密" --product-image "D:\素材\商品.png" --output-root "D:\ai90秒广告漫剧"
python ai90\run_pipeline.py --premise "..." --product-image "D:\素材\商品.png" --comfy "http://127.0.0.1:8188" --workflow "D:\工作流\api.json" --output-root "D:\ai90秒广告漫剧" --run
```

Linux 云环境无法访问 Windows D 盘或本机 ComfyUI，因此需在你的电脑运行。生成完成并人工验收后，将输出文件夹按剧情命名归档。

## 已接入 MiniMax H3 工作流

已保存用户上传的工作流模板：[workflow_minimax_h3_template.json](ai90/workflow_minimax_h3_template.json)。它包含 `MiniMaxH3ReferenceToVideo`、三路参考图、720×1280 竖屏相关节点、VAE/采样/保存视频节点，并保留原模型与节点连线。

运行器会替换节点 138/302 的提示词和节点 137/139/142 的图片路径。由于该工作流有三路参考图，当前会把同一张商品图填入三路；若要人物锁脸和场景参考，请在工作流中改为三张对应参考图，并扩展运行器参数。上传的是 API 节点格式 JSON，已完成语法读取；尚未在你的本机提交任务或验证模型文件可用性。

## 新版一键运行示例（Windows PowerShell）

仅生成提示词和任务清单，不提交 ComfyUI：

```powershell
python ai90\run_pipeline.py `
  --premise "女儿发现父亲隐藏多年的秘密" `
  --product-image "D:\素材\商品.png" `
  --count 1 `
  --output-root "D:\ai90秒广告漫剧"
```

提交 MiniMax H3 工作流：

```powershell
python ai90\run_pipeline.py `
  --premise "女儿发现父亲隐藏多年的秘密" `
  --product-image "D:\素材\商品.png" `
  --count 1 `
  --comfy "http://192.168.3.25:9500" `
  --workflow "D:\工作流\workflow_minimax_h3_template.json" `
  --output-root "D:\ai90秒广告漫剧" `
  --run
```

`--count 2` 会在同一批次生成 36 个五秒段。运行器只查询 `/history/{prompt_id}`，不会删除或取消已有任务。每个项目目录包含 `manifest.json` 和逐段 `segment_XX.txt`；全部视频人工验收后，再按剧情名称归档。

## 你的电脑上运行 A01/A02

README.md 上传内容是 GitHub 个人主页介绍，与 ComfyUI 技能无关；工作台技能已经安装在本项目 `workbench/`，无需重复安装。把项目目录复制到 Windows 后，在 PowerShell 执行：

```powershell
Set-Location C:\路径\到\项目\11
powershell -ExecutionPolicy Bypass -File .\ai90\run_A01_A02.ps1
```

脚本会检查 `C:\Users\Jerry\OneDrive\Desktop\产品图`，再调用 ComfyUI。当前云端不能远程执行你电脑上的 PowerShell、访问你的 D 盘或读取该 Windows 路径。

## 可视化 App

Windows 双击运行：

```powershell
python ai90\ai90_app.py
```

在界面填写剧情、产品图片、云端 ComfyUI API 地址、工作流 JSON 和输出目录。取消“提交到 ComfyUI”时只生成提示词；勾选后才提交任务。界面实时显示运行器输出，运行器不会取消或删除已有任务。需要打包成 exe 时可使用 `pyinstaller --onefile --windowed ai90\ai90_app.py`（需在 Windows 安装 PyInstaller）。

## 下载 Windows EXE

仓库已加入 GitHub Actions 自动打包配置。打开仓库的 **Actions** → **Build AI90 Windows App** → **Run workflow**，等待完成后进入运行记录，在 **Artifacts** 下载 `AI90-Windows-App`。解压后双击 `AI90_广告漫剧运行器.exe` 即可打开详细界面。
