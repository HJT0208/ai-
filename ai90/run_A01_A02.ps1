param(
 [string]$ProductImage = 'C:\Users\Jerry\OneDrive\Desktop\产品图',
 [string]$Comfy = 'http://192.168.3.25:9500',
 [string]$Workflow = "$PSScriptRoot\workflow_minimax_h3_template.json",
 [string]$OutputRoot = 'D:\ai90秒广告漫剧'
)
$ErrorActionPreference='Stop'
if (!(Test-Path $ProductImage)) { throw "产品图片路径不存在: $ProductImage" }
python "$PSScriptRoot\run_pipeline.py" `
  --premise '使用工作台《他不是弟弟》的剧情，先生成A01和A02，仅角色对白，严格沿用工作台人物与连续性设定' `
  --product-image $ProductImage --count 1 --comfy $Comfy --workflow $Workflow --output-root $OutputRoot --run
