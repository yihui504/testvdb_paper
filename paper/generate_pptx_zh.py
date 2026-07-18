#!/usr/bin/env python3
"""22-page Chinese GEAR-style .pptx for TestVDB (B' plan). CJK: 微软雅黑."""
from __future__ import annotations
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

FIG = os.path.join(os.path.dirname(__file__), "figures")
OUT = os.path.join(os.path.dirname(__file__), "TestVDB_slides_zh.pptx")
CJK = "微软雅黑"

HBG = RGBColor(0x1B,0x3A,0x5C); AB=RGBColor(0x2E,0x5C,0x8A); AO=RGBColor(0xD9,0x8E,0x48)
AG=RGBColor(0x4A,0x8C,0x5C); AR=RGBColor(0xB0,0x50,0x50); TD=RGBColor(0x33,0x33,0x33)
TG=RGBColor(0x66,0x66,0x66); LB=RGBColor(0xF0,0xF4,0xF8); WH=RGBColor(0xFF,0xFF,0xFF)

prs = Presentation(); prs.slide_width = Inches(13.333); prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]

def _f(p,s,c,b=False):
    p.font.name=CJK; p.font.size=Pt(s); p.font.color.rgb=c; p.font.bold=b

def header(sl,t,n,sec):
    bar=sl.shapes.add_shape(MSO_SHAPE.RECTANGLE,0,0,prs.slide_width,Inches(1.05))
    bar.fill.solid(); bar.fill.fore_color.rgb=HBG; bar.line.fill.background()
    tb=sl.shapes.add_textbox(Inches(0.45),Inches(0.12),Inches(10.5),Inches(0.85))
    tf=tb.text_frame; tf.word_wrap=True; tf.vertical_anchor=MSO_ANCHOR.MIDDLE
    p=tf.paragraphs[0]; p.text=t; _f(p,20,WH,True)
    pb=sl.shapes.add_textbox(Inches(10.8),Inches(0.12),Inches(2.3),Inches(0.45))
    pp=pb.text_frame.paragraphs[0]; pp.text=f"P{n}/22 {sec}"; pp.alignment=PP_ALIGN.RIGHT; _f(pp,11,RGBColor(0xBB,0xCC,0xDD))
    st=sl.shapes.add_shape(MSO_SHAPE.RECTANGLE,0,Inches(1.05),prs.slide_width,Inches(0.06))
    st.fill.solid(); st.fill.fore_color.rgb=AO; st.line.fill.background()

def bullets(sl,items,top=1.5,left=0.7,w=12,h=5.5,sz=16):
    tb=sl.shapes.add_textbox(Inches(left),Inches(top),Inches(w),Inches(h))
    tf=tb.text_frame; tf.word_wrap=True
    for i,item in enumerate(items):
        p=tf.paragraphs[0] if i==0 else tf.add_paragraph()
        t,c=(item if isinstance(item,tuple) else (item,TD))
        p.text="•  "+t; _f(p,sz,c); p.space_after=Pt(10)

def table(sl,hs,rs,top=1.5,left=0.6,w=12.1,h=5.2):
    g=sl.shapes.add_table(len(rs)+1,len(hs),Inches(left),Inches(top),Inches(w),Inches(h)).table
    g.first_row=True; g.horz_banding=False
    for j,h in enumerate(hs):
        c=g.cell(0,j); c.text=h; c.fill.solid(); c.fill.fore_color.rgb=AB
        for p in c.text_frame.paragraphs: _f(p,13,WH,True); p.alignment=PP_ALIGN.CENTER
    for i,row in enumerate(rs):
        for j,v in enumerate(row):
            c=g.cell(i+1,j); c.text=str(v); c.fill.solid(); c.fill.fore_color.rgb=LB if i%2==0 else WH
            for p in c.text_frame.paragraphs: _f(p,11.5,TD)

def image(sl,name,top=1.35,left=1.4,w=10.5):
    sl.shapes.add_picture(os.path.join(FIG,name),Inches(left),Inches(top),Inches(w))

def bn(sl,num,label,sub=None,top=2.2):
    tb=sl.shapes.add_textbox(Inches(1),Inches(top),Inches(11.3),Inches(2.5))
    p=tb.text_frame.paragraphs[0]; p.text=num; p.alignment=PP_ALIGN.CENTER; p.font.size=Pt(96); p.font.bold=True; p.font.color.rgb=AO
    lb=sl.shapes.add_textbox(Inches(1),Inches(top+2.3),Inches(11.3),Inches(1))
    lp=lb.text_frame.paragraphs[0]; lp.text=label; lp.alignment=PP_ALIGN.CENTER; _f(lp,20,TD)
    if sub:
        sb=sl.shapes.add_textbox(Inches(1),Inches(top+3.1),Inches(11.3),Inches(1))
        sp=sb.text_frame.paragraphs[0]; sp.text=sub; sp.alignment=PP_ALIGN.CENTER; _f(sp,14,TG)

def tc(sl,lt,li,rt,ri,lc=AR,rc=AG):
    lb=sl.shapes.add_textbox(Inches(0.6),Inches(1.4),Inches(6),Inches(0.6))
    lp=lb.text_frame.paragraphs[0]; lp.text=lt; _f(lp,16,lc,True)
    bullets(sl,li,top=2.0,left=0.7,w=5.8,h=4.8,sz=14)
    dv=sl.shapes.add_shape(MSO_SHAPE.RECTANGLE,Inches(6.5),Inches(1.6),Inches(0.04),Inches(5))
    dv.fill.solid(); dv.fill.fore_color.rgb=RGBColor(0xDD,0xDD,0xDD); dv.line.fill.background()
    rb=sl.shapes.add_textbox(Inches(6.9),Inches(1.4),Inches(6),Inches(0.6))
    rp=rb.text_frame.paragraphs[0]; rp.text=rt; _f(rp,16,rc,True)
    bullets(sl,ri,top=2.0,left=7.0,w=5.8,h=4.8,sz=14)

def slide(n,sec,title):
    s=prs.slides.add_slide(BLANK); header(s,title,n,sec); return s

def note(sl,text,top=6.6):
    nb=sl.shapes.add_textbox(Inches(0.6),Inches(top),Inches(12),Inches(0.5))
    p=nb.text_frame.paragraphs[0]; p.text=text; _f(p,11,TG)

# === 22 页 ===

s=prs.slides.add_slide(BLANK)
bg=s.shapes.add_shape(MSO_SHAPE.RECTANGLE,0,0,prs.slide_width,prs.slide_height)
bg.fill.solid(); bg.fill.fore_color.rgb=HBG; bg.line.fill.background()
tb=s.shapes.add_textbox(Inches(0.8),Inches(2.4),Inches(11.7),Inches(2.2)); tf=tb.text_frame; tf.word_wrap=True
p=tf.paragraphs[0]; p.text="TestVDB"; _f(p,54,WH,True)
p2=tf.add_paragraph(); p2.text="基于源码证伪的 LLM 行为声明：VDBMS 文档-实现一致性测试"; _f(p2,22,RGBColor(0xCC,0xDD,0xEE))
m=s.shapes.add_textbox(Inches(0.8),Inches(5.5),Inches(11.7),Inches(1.5))
for i,ln in enumerate(["作者（待定）","单位","会议/Session（待定）"]):
    p=m.text_frame.paragraphs[0] if i==0 else m.text_frame.add_paragraph(); p.text=ln; _f(p,16,RGBColor(0xAA,0xCC,0xDD))

s=slide(2,"开场","VDBMS 存储 RAG 依赖的嵌入；缺陷代价高且多数功能性失败")
image(s,"fig1_rag_arch.png",top=1.3,left=2.5,w=8.3)
table(s,["来源","发现"],
      [["bug 研究 (Xie 2025)","> 50% VDBMS bug 是功能性失败"],
       ["测试 roadmap (Wang 2025)","~43% 归为错误行为；oracle 是关键挑战"],
       ["VDBFuzz (Wang 2026)","首个 VDBMS fuzzer —— 用 crash 作 oracle"]],top=4.7,h=2.2)

s=slide(3,"问题","文档-实现缺陷：API 静默接受文档规定应拒绝的输入")
bullets(s,[("文档-实现一致性 —— API accept/reject 是否匹配文档？",TD),
    ("正确性 —— 返回结果是否数学正确？",TD),("TestVDB 针对文档-实现一致性。",TD),("文档边界是自然语言，非形式化语法。",AO)])

s=slide(4,"问题","负的 score threshold 禁用过滤器并返回所有匹配"); image(s,"fig2_cases.png",top=1.5,left=1.2,w=11)

s=slide(5,"问题","38 个确认缺陷中 37 个不崩溃，fuzzer 检测不到")
bn(s,"37 / 38","确认的缺陷不产生 crash","基于 crash 的 fuzzer 无法触及")

s=slide(6,"朴素 oracle","文档-实现残差只剩 LLM 作为可行 oracle")
table(s,["候选 oracle","触及","为何触及不了"],
      [["Crash (VDBFuzz)","crash/hang","38 个中 37 个不 crash"],
       ["差分测试","跨厂商数学不变量","accept/reject 设计上分叉"],
       ["蜕变关系","结果正确性","输出关系，非输入接受性"],
       ["属性测试","数学+schema","需可检查 property+OpenAPI"],
       ["REST 文档 oracle","状态/字段断言","从低歧义源可靠提取"],
       ["LLM oracle (TestVDB)","accept/reject vs 文档","残差需语义判断"]])

s=slide(7,"核心洞察","源歧义鸿沟：结构化源产生断言，歧义文档产生 claim"); image(s,"fig3_source_ambiguity_gap.png",top=1.3,left=0.8,w=11.7)

s=slide(8,"核心洞察","家族特定错误：judge 确认 extractor 偏差")
bullets(s,["一个 LLM 家族同时提取 claim 和裁决，共享偏差","judge 倾向确认 extractor 错误 —— self-preference",
    "代表：Panickssery (2024); Wataoka (2024)",("缓解：跨模型验证",AG)])

s=slide(9,"核心洞察","任务内在错误：不同家族推断相同错误 claim"); image(s,"fig4_two_layer_venn.png",top=1.3,left=0.9,w=11.5)

s=slide(10,"核心洞察","跨模型验证覆盖家族特定，不覆盖任务内在")
tc(s,"家族特定",["consistencyLevel —— GLM/DeepSeek 说法不同","跨模型能发现分歧"],
     "任务内在",["timeout —— 都提取 '>= 1'（同错）","跨模型看到一致（都错）","只有源码能证伪"],lc=AB,rc=AO)

s=slide(11,"证据","12 个 over-strict 子句：跨模型捕获 7，源码捕获 12")
table(s,["Over-strict 子句","TI","跨模型","源码"],
      [["shardsNum >= 1","是","漏","捕获"],["metricType strict enum","否","漏","捕获"],
       ["consistencyLevel strict enum","否","捕获","捕获"],["data non-empty","是","漏","捕获"],
       ["limit >= 1","否","捕获","捕获"],["timeout >= 1 (Qdrant)","是","捕获","捕获"],
       ["group_size >= 1 (Qdrant)","是","漏","捕获"],["score_threshold ∈[0,1]","是","漏","捕获"],
       ["合计","5","7/12","12/12"]],top=1.4,h=4.8)
note(s,"扩展到 n=29（行为+显式边界子型）；见 P18。源码 = 实现。")

s=slide(12,"方法","TestVDB pipeline：提取，裁决，用源码证伪")
image(s,"fig5_pipeline.png",top=1.3,left=0.5,w=12.3)
note(s,"五阶段：extract → attack → judge → dev-review(源码证伪) → novelty。多 agent；~10⁴ 调用，~$10/target。")

s=slide(13,"方法","证伪规则：若源码显示 shardsNum=0 选默认值，over-strict 子句被证伪")
tc(s,"Over-strict 子句（LLM）",["shardsNum >= 1","probe: shardsNum=0 → API 200","LLM 裁决：'违规'"],
     "源码证伪",["源码: if shardsNum==0 { use default }","0 选默认 —— over-strict","FP 消除","与 MASTOR (as designed) 反向"],lc=AR,rc=AG)

s=slide(14,"实验","四个 RQ；提交 111，确认 38")
g1=s.shapes.add_table(5,2,Inches(0.4),Inches(1.5),Inches(5.8),Inches(3.8)).table
g1.first_row=True; g1.horz_banding=False
for j,h in enumerate(["RQ","问题"]):
    c=g1.cell(0,j); c.text=h; c.fill.solid(); c.fill.fore_color.rgb=AB
    for p in c.text_frame.paragraphs: _f(p,12,WH,True)
for i,(rq,q) in enumerate([["RQ1","多少 doc-impl 缺陷？"],["RQ2","源码是否抑制 FP？"],["RQ3","跨模型 vs 源码？"],["RQ4","无模型子类有效？"]]):
    for j,v in enumerate([rq,q]):
        c=g1.cell(i+1,j); c.text=v; c.fill.solid(); c.fill.fore_color.rgb=LB if i%2==0 else WH
        for p in c.text_frame.paragraphs: _f(p,11,TD)
g2=s.shapes.add_table(7,3,Inches(6.8),Inches(1.5),Inches(6.1),Inches(4.5)).table
g2.first_row=True; g2.horz_banding=False
for j,h in enumerate(["VDBMS","提交","确认"]):
    c=g2.cell(0,j); c.text=h; c.fill.solid(); c.fill.fore_color.rgb=AB
    for p in c.text_frame.paragraphs: _f(p,12,WH,True)
for i,row in enumerate([["Milvus","51","22"],["Weaviate","30","3"],["Qdrant","26","13"],["MeiliSearch","3","0"],["Chroma","1","0"],["合计","111","38"]]):
    for j,v in enumerate(row):
        c=g2.cell(i+1,j); c.text=v; c.fill.solid(); c.fill.fore_color.rgb=LB if i%2==0 else WH
        for p in c.text_frame.paragraphs: _f(p,11,TD)

s=slide(15,"实验","~85% 是 doc-impl 缺陷；VDBFuzz 同版本 0 crash")
tc(s,"组成（非普遍率）",["~85% 文档-实现缺陷","~10% 经典可寻址","~5% 并发","确认子集 89%"],
     "VDBFuzz 对比 (Qdrant v1.18.2)",["我们跑了 VDBFuzz: 26,000 请求","0 crash, 0 非-200","TestVDB 发现 doc-impl 缺陷","不相交缺陷类"],lc=AB,rc=AG)

s=slide(16,"实验","源码 anchor 抑制 81% 误报（从 31%），真阳性 96.7%")
bn(s,"81%","源码 anchor 抑制的误报","相比其他 anchor 的 31%；真阳性 96.7%（n=30）")

s=slide(17,"实验","精度随源码 anchor 扩展：25.5% → 45.6% → 69.2%"); image(s,"fig7_ablation.png",top=1.5,left=2.5,w=8.3)

s=slide(18,"实验","RQ3 在 n=29：源码捕获全部 16 over-strict；显式边界 0/13；κ=1.0")
table(s,["子型","n","任务内在","跨模型","源码"],
      [["参数 over-strict","12","5/12","7/12","12/12"],["行为 over-strict","4","4/4","0/4","4/4"],
       ["显式边界 negative","13","0/13","—","—"],["厂商内对比","—","56% vs 0%","—","—"],
       ["跨模型 κ (n=20)","20","—","κ=1.0","—"]],top=1.5)

s=slide(19,"实验","无模型不变量子类独立发现缺陷")
table(s,["不变量","观测","跨厂商"],[["COSINE 距离","相同向量距离 > 1.0","Milvus+Qdrant"],
     ["索引完整性","索引返回 25 中 2 个","Milvus+Qdrant"],["Payload 过滤","过滤缺失字段返回点","Milvus+Qdrant"]])

s=slide(20,"相关工作","已有工作停留在低歧义源；TestVDB 进入歧义领域")
table(s,["工作线","代表","差异"],
      [["VDBMS 测试","VDBFuzz/roadmap/bug study","crash vs doc-impl"],
       ["REST oracle","AGORA+/SATORI/MASTOR","低歧义源；我们用 NL 文档"],
       ["文档 oracle","Toradocu/Doc2OracLL/AugmenTest/Konstantinou","信任 LLM；我们用源码证伪"],
       ["DB 正确性","NoREC/TLP/DQE/DDLCheck","有参考语义；我们没有"],
       ["LLM-judge","Panickssery/Wataoka/Haldar","正交 —— source grounding"]],top=1.4,h=5.6)

s=slide(21,"收尾","威胁与结论")
tc(s,"威胁",["over-strict 子集 (n=16) 最 contingent","统计 claim 限 Milvus+Qdrant","机制相关非因果"],
     "结论",["doc-impl 抗确定性检查","LLM 错误：家族特定+任务内在","超越 VDBMS —— 任何 NL 文档系统"],lc=AR,rc=AG)

s=slide(22,"收尾","TestVDB —— 四个核心结果"); image(s,"fig8_summary.png",top=1.4,left=1.5,w=10.3)

prs.save(OUT)
print(f"[wrote] {OUT} ({len(prs.slides._sldIdLst)} slides)")
