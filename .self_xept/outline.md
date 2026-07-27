# TestVDB Paper Outline（PPT v2.3 驱动，2026-07-27 重写）

## Task
按 PPT v2.3（`testvdb_v2.3_20260726.pptx`，27 slides）故事线从头重写 `paper/paper-draft-acm-sigconf.tex`。规避被 5-family 实验挑战的 TI claim；FP 分析改用 Hallucination + Self-Preference Bias 两独立问题。

## Key shift vs archive（paper-archive-20260727 分支）
- **无 task-intrinsic layer**（旧论文 core claim，被 5-family 实验挑战 + baseline 不复现）
- FP = Hallucination（extraction 端）+ Self-Preference Bias（judging 端），两独立问题
- Multi-perspective judging 作过渡（"works but not good enough"，S21）
- Dev-reviewer = source-grounded falsifier（act like maintainer，S22）

## Structure（9 节，对应 PPT slides）

### Abstract
VDBMS logical bugs 普遍（VDBFuzz 只 crash）+ doc-impl inconsistency 是主要类 + TestVDB（4 步 pipeline + LLM 自动化）+ dev-reviewer（source-grounded falsifier 抑制 FP）+ 结果（107 submitted / 49 TP / 15 fixed；48-candidate FP suppression vs multi-perspective/single-LLM baseline；vs VDBFuzz 双向）

### §1 Introduction（S2-9）
- VDBMS 重要（存 vector embeddings for RAG，S2）
- bugs mostly logical（bugstudy25 + roadmap25，S3）；VDBFuzz 只 crash（S3）
- 文档 NL 难结构化 + 不同 VDBMS 不同标准难 differential（S4）
- doc-impl inconsistency 目标（S5-6）
- 49823 observation（nprobe=0 silently accepted though doc says range [1,16384]，S8）
- TestVDB 4 步 approach（S9）+ contributions list

### §2 Background and Problem Setup
- VDBMS docs（NL prose，不同标准）
- oracle problem（barr15）
- doc-impl consistency vs correctness 区分
- Table 1: oracle 排除（crash/differential/metamorphic/property/REST-spec → LLM 是 residual 的 practical oracle）

### §3 TestVDB Approach（S10-14）
- Step 1: behavioral claims extraction（NL doc → structured JSON claims，S10）
- Step 2: test script generation（claims → executable scripts，S11）
- Step 3: test execution（sandboxed Docker VDBMS，S12）
- Step 4: defect confirmation（expected claims vs actual response/state/logs，S13）
- LLM 自动化（extract + generate + adjudicate，S14）

### §4 The False-Positive Problem（S15-21）
- Extraction 端: Hallucination（ji23hall）—— LLM 编造文档没说的约束
- Judging 端: Self-Preference Bias（panickssery24）—— LLM 偏袒自己 extract 的 claim
- 后果：高 FP rate
- Multi-perspective judging 尝试（4 judges: doc/evidence/severity/novelty + vote）→ "works but not good enough"（48 candidates，precision 高但 recall 低 ~15%）—— 引出 dev-reviewer

### §5 Dev-Reviewer: Source-Grounded Falsifier（S22）
- Act like VDBMS maintainer: reproduce, cross-check source, try to disprove
- 3 checks: ① independently reproducible ② evidence sufficient ③ falsifiable
- 3 anchors: clean-reproduction / source-grounded / threat-model
- 输出：survives all 3 = defect；fails any = suppressed

### §6 Evaluation（S23-26）
- **RQ1** Bug detection capability: 107 submitted / 34 confirmed new / 15 fixed（跨 Milvus/Qdrant/Weaviate，S24）
- **RQ2** FP suppression effectiveness: 48 candidates（27TP: milvus 20 + qdrant 7；21FP: milvus 12 + qdrant 9），precision/accuracy/recall vs baseline（multi-perspective + single-LLM no-source），S25
- **RQ3** vs VDBFuzz: 49 TPs 对比；#9045 silent-accept（TestVDB 在 v1.18.0 挖到）+ size=2⁶³ divide-by-zero（VDBFuzz 在 v1.4.0 挖到，TestVDB contract reasoning 也能 reach），双向可达性，S26

### §7 Related Work
- VDBMS testing: VDBFuzz, roadmap, bugstudy
- REST-API oracle: AGORA+, SATORI, MASTOR
- LLM-as-judge reliability: Panickssery（self-preference）, Haldar（intra-judge）, Hallucination survey
- Documentation-derived oracle: Toradocu, Doc2OracLL, AugmenTest, ChatAssert, Testora

### §8 Discussion and Limitations
- generalization（REST API without OpenAPI / config validation / policy-as-code）—— future work
- single LLM backbone（GLM-5.2）—— inherent limitation
- closed-source VDBMS 不适用（需 source）
- treat implementation as correct（impl bug 可 wrongly falsify）

### §9 Conclusion
recap contributions + future work

## Data（沿用 PPT，已在 data/ + ablation 包）
- 107 submitted / 49 TP / 34 confirmed new / 15 fixed（RQ1）
- 48 candidates（27TP + 21FP）（RQ2）
- VDBFuzz 双向 #9045 + size=2⁶³（RQ3）

## Citations（确认 paper/references.bib 有）
vdbfuzz26, roadmap25, bugstudy25, barr15, ji23hall, panickssery24, metmap24, claessen00, manes21, hou23llmse, agoraplus25, satori25, mastor26, toradocu16, doc2oracll25, augmentest25, chatassert24, testora26, haldar25, wataoka24

## 写作纪律（write-paper 规则）
- 逐节写 + 每节编译（latexmk）
- 无 em-dash / 无 "It is" / "There is"
- 句子 <25 词
- 每主张有支撑（cite 或数据）
- 不编造引用 / 数据
