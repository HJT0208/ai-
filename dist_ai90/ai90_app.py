import tkinter as tk
from tkinter import ttk,filedialog,messagebox
import subprocess,threading,queue,sys,os
class App:
 def __init__(self,root):
  self.root=root;root.title('AI90 广告漫剧运行器');root.geometry('760x520');self.q=queue.Queue()
  frm=ttk.Frame(root,padding=14);frm.pack(fill='both',expand=True)
  self.vars={}
  fields=[('剧情概述','premise'),('产品图片路径','image'),('ComfyUI API 地址','comfy'),('工作流 JSON','workflow'),('输出目录','out')]
  defaults={'comfy':'','out':r'D:\ai90秒广告漫剧'}
  for i,(lab,key) in enumerate(fields):
   ttk.Label(frm,text=lab).grid(row=i,column=0,sticky='w',pady=5);v=tk.StringVar(value=defaults.get(key,''));self.vars[key]=v;ttk.Entry(frm,textvariable=v,width=70).grid(row=i,column=1,sticky='ew',pady=5)
   if key in ('image','workflow','out'):ttk.Button(frm,text='选择',command=lambda k=key:self.pick(k)).grid(row=i,column=2,padx=5)
  ttk.Label(frm,text='视频数量').grid(row=5,column=0,sticky='w',pady=5);self.count=tk.IntVar(value=1);ttk.Spinbox(frm,from_=1,to=20,textvariable=self.count,width=8).grid(row=5,column=1,sticky='w')
  self.run=tk.BooleanVar();ttk.Checkbutton(frm,text='提交到 ComfyUI（不勾选则只生成提示词）',variable=self.run).grid(row=6,column=1,sticky='w',pady=8)
  bar=ttk.Frame(frm);bar.grid(row=7,column=1,sticky='w');ttk.Button(bar,text='开始',command=self.start).pack(side='left');ttk.Button(bar,text='清空日志',command=lambda:self.log.delete('1.0','end')).pack(side='left',padx=8)
  self.log=tk.Text(frm,height=17);self.log.grid(row=8,column=0,columnspan=3,sticky='nsew',pady=10);frm.columnconfigure(1,weight=1);frm.rowconfigure(8,weight=1);self.root.after(200,self.poll)
 def pick(self,k):
  if k=='out':p=filedialog.askdirectory()
  else:p=filedialog.askopenfilename(filetypes=[('JSON/图片','*.json *.png *.jpg *.jpeg'),('所有文件','*.*')])
  if p:self.vars[k].set(p)
 def write(self,s):self.q.put(s)
 def start(self):
  if not self.vars['premise'].get() or not self.vars['image'].get() or not self.vars['workflow'].get():messagebox.showerror('缺少输入','请填写剧情、产品图片和工作流 JSON');return
  cmd=[sys.executable,os.path.join(os.path.dirname(__file__),'run_pipeline.py'),'--premise',self.vars['premise'].get(),'--product-image',self.vars['image'].get(),'--count',str(self.count.get()),'--comfy',self.vars['comfy'].get(),'--workflow',self.vars['workflow'].get(),'--output-root',self.vars['out'].get()]
  if self.run.get():cmd.append('--run')
  self.write('开始：'+('提交 ComfyUI' if self.run.get() else '仅生成提示词'))
  threading.Thread(target=self.worker,args=(cmd,),daemon=True).start()
 def worker(self,cmd):
  try:
   p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
   for line in p.stdout:self.write(line.rstrip())
   self.write('完成，退出码 '+str(p.wait()))
  except Exception as e:self.write('错误：'+str(e))
 def poll(self):
  while not self.q.empty():self.log.insert('end',self.q.get()+'\n');self.log.see('end')
  self.root.after(200,self.poll)
if __name__=='__main__':App(tk.Tk()).root.mainloop()
