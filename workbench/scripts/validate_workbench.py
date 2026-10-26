#!/usr/bin/env python3
import json, re, sys
from pathlib import Path

def fail(msg, errors): errors.append(msg)
def main(path):
    p=Path(path); data=json.loads(p.read_text(encoding='utf-8')); errors=[]
    for k in ('project','audio_policy','characters','assets','segments'):
        if k not in data: fail(f'missing top-level field: {k}', errors)
    if data.get('project',{}).get('aspect_ratio')!='9:16': fail('aspect_ratio must be 9:16', errors)
    if data.get('audio_policy',{}).get('music') is not False: fail('global music must be false', errors)
    assets={a.get('asset_id') for a in data.get('assets',[])}
    segs=sorted(data.get('segments',[]), key=lambda x:x.get('start_sec',0))
    prev=None
    for s in segs:
        sid=s.get('segment_id','?'); st=s.get('start_sec'); en=s.get('end_sec')
        if not isinstance(st,(int,float)) or not isinstance(en,(int,float)) or en-st!=5: fail(f'{sid}: duration is not 5 sec',errors)
        if prev is not None and st!=prev: fail(f'{sid}: timeline gap/overlap at {st}, expected {prev}',errors)
        prev=en
        if s.get('audio',{}).get('music') is not False: fail(f'{sid}: music must be false',errors)
        if not isinstance(s.get('dialogue',{}).get('lines'),list): fail(f'{sid}: dialogue.lines must be array',errors)
        vp=s.get('visual_prompt','')
        if re.search(r'[“”"].{1,80}[“”"]',vp): fail(f'{sid}: visual_prompt appears to contain quoted speech',errors)
        for slot in s.get('picture_slots',[]):
            if slot.get('asset_id') not in assets: fail(f'{sid}: unknown asset {slot.get("asset_id")}',errors)
    out={'ok':not errors,'errors':errors,'stats':{'segments':len(segs),'assets':len(assets),'duration_sec':prev or 0}}
    print(json.dumps(out,ensure_ascii=False,indent=2)); return 0 if not errors else 1
if __name__=='__main__': sys.exit(main(sys.argv[1]))
