#!/usr/bin/env python3
import json, sys
from pathlib import Path

def main(src, out):
    data=json.loads(Path(src).read_text(encoding='utf-8')); root=Path(out); root.mkdir(parents=True,exist_ok=True)
    for d in ['01_outline','02_script/30s_groups','03_segments/5s','04_prompts/visual','04_prompts/dialogue','04_prompts/audio','05_assets','06_workflow','07_validation']:
        (root/d).mkdir(parents=True,exist_ok=True)
    (root/'project.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    for s in data['segments']:
        sid=s['segment_id']; group=f"{int(s['start_sec']//30)+1:02d}"
        (root/'03_segments/5s'/f'{sid}.json').write_text(json.dumps(s,ensure_ascii=False,indent=2),encoding='utf-8')
        (root/'04_prompts/visual'/f'{sid}.txt').write_text(s['visual_prompt'],encoding='utf-8')
        lines='\n'.join(s.get('dialogue',{}).get('lines',[])) or '[空：禁止对白]'
        (root/'04_prompts/dialogue'/f'{sid}.txt').write_text(lines,encoding='utf-8')
        (root/'04_prompts/audio'/f'{sid}.txt').write_text(json.dumps(s['audio'],ensure_ascii=False,indent=2),encoding='utf-8')
    (root/'05_assets/asset_manifest.json').write_text(json.dumps(data['assets'],ensure_ascii=False,indent=2),encoding='utf-8')
    (root/'06_workflow/workflow_contract.json').write_text(json.dumps({'input':'project.json','picture_slot_rule':'每段只引用manifest中的asset_id','audio_rule':'music=false；对白仅来自dialogue.lines','output':'由用户自己的ComfyUI生成视频'},ensure_ascii=False,indent=2),encoding='utf-8')
    print(root)
if __name__=='__main__': main(sys.argv[1],sys.argv[2])
