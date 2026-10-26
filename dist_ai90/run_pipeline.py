#!/usr/bin/env python3
import argparse,json,re,time,uuid
from pathlib import Path
from urllib.request import Request,urlopen
N=18
def prompt(p,prod,i):
 g=i//6+1;s=(i%6)*5
 x=(f'这是面向40岁以上中老年观众的竖屏AI广告漫剧，第{g}组30秒中的第{s}至{s+5}秒。故事前提：{p}。商品参考：{prod}。画幅固定9:16，写实电影感；人物脸型、发际线、眉眼鼻唇、衣服颜色、饰品沿用锁定卡，商品包装、文字、颜色、尺寸不得改变。先承接上一段，再完成本段唯一主导动作，结尾保留稳定姿态。\n'
'摄影机从胸口高度中近景开始，24毫米自然透视，稳定缓慢推进；人物先看道具再看镜头，眉毛由放松到微收紧，眼睑自然开合，视线停留一秒，嘴角和下颌细微变化，肩颈与重心同步。手指按真实关节顺序接触物体：定位、握持、移动、停住；动作中速偏慢，镜头连续，无突然变焦、旋转抖动或跳帧。环境光从左上方柔和照射，保留皮肤纹理、衣料纤维和商品边缘，浅景深但不丢失空间关系。\n'
'保持角色身份、左右方向、道具位置和口型一致；禁止年轻化、塑料皮肤、畸形手、重影、额外肢体、面部漂移、服装变色、商品变形、乱码字幕、水印、自动音乐、闪烁、过曝、欠曝。前1秒看懂人物与商品关系，第2秒出现问题，第3至4秒完成有因果的操作或反应，第5秒留下新的信息缺口。台词只使用台词字段，商品只展示图片可见功能，不写无证据疗效、价格或绝对承诺。每个手部动作写清左右手、起点、接触面、力度、路径和终止位置；人物视线必须指向真实目标。开头与上一段重合约0.3秒，结尾停留0.5秒，不凭空切换地点、季节、衣服或时间。生成失败只重试当前段，保留其他任务ID，不删除队列任务。')
 while len(x)<2100:x+='\n连续性复核：稳定运镜、自然微表情、真实接触、清楚商品轮廓、可剪辑首尾姿态和中老年观众易懂的信息层级。'
 return x
def api(u,data=None):
 q=Request(u,data=json.dumps(data).encode() if data is not None else None,headers={'Content-Type':'application/json'})
 with urlopen(q,timeout=30) as r:return json.loads(r.read())
def main():
 a=argparse.ArgumentParser();a.add_argument('--premise',required=True);a.add_argument('--product-image',required=True);a.add_argument('--count',type=int,default=1);a.add_argument('--comfy',default='http://192.168.3.25:9500');a.add_argument('--workflow',default='');a.add_argument('--output-root',default=r'D:\ai90秒广告漫剧');a.add_argument('--run',action='store_true');a.add_argument('--poll',type=float,default=5);a=a.parse_args();root=Path(a.output_root);root.mkdir(parents=True,exist_ok=True);out=root/(time.strftime('%Y%m%d_%H%M%S')+'_'+re.sub(r'[^0-9A-Za-z\u4e00-\u9fff_-]+','_',a.premise)[:50]);out.mkdir();wf=json.load(open(a.workflow,encoding='utf8')) if a.workflow else None;m={'premise':a.premise,'product_image':a.product_image,'aspect_ratio':'9:16','segments':[]}
 for i in range(18*max(1,a.count)):
  z={'index':i+1,'group':i//6+1,'start':i%6*5,'end':i%6*5+5,'prompt':prompt(a.premise,a.product_image,i),'status':'prepared'}
  if a.run:
   if not a.comfy or wf is None:raise SystemExit('--run 需要 --comfy 与 --workflow')
   w=json.loads(json.dumps(wf));z['client_id']=str(uuid.uuid4());w=json.loads(json.dumps(w,ensure_ascii=False).replace('{{PROMPT}}',z['prompt']).replace('{{IMAGE}}',a.product_image));r=api(a.comfy.rstrip('/')+'/prompt',{'prompt':w,'client_id':z['client_id']});z['prompt_id']=r.get('prompt_id');z['status']='queued'
   while True:
    try:
     if z['prompt_id'] in api(a.comfy.rstrip('/')+'/history/'+str(z['prompt_id'])):z['status']='completed';break
    except Exception:pass
    time.sleep(a.poll)
  m['segments'].append(z);(out/f"segment_{i+1:02d}.txt").write_text(z['prompt'],encoding='utf8');json.dump(m,open(out/'manifest.json','w',encoding='utf8'),ensure_ascii=False,indent=2)
 print(out)
if __name__=='__main__':main()
