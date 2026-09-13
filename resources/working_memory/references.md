# References

核查状态缓存（xept:check-references 跨会话记忆）。
> 位置说明：skill 默认路径为 `.self_xept/references.md`，但本 workspace 规则禁止写入
> `.self_xept/`（仅允许 `agent-memory.md`），故缓存置于 `resources/working_memory/references.md`。
> 本次增量核查时间：2026-08-26。基线：`.bib` 头注 "All entries DBLP-verified (Round 16)"，
> 且 `files/TestVDB.bib` 与最近一次提交逐字节一致（仅 BOM 差异），`.tex` 引用集合与
> HEAD/`TestVDB.marked.tex` 相同（22 个 key）→ 无新增引用，本次只深核 8 条存疑项。

## Citations

### ok — 本次会话深核通过（2026-08-26）
- key: roadmap25
  title: "Towards Reliable Vector Database Management Systems: A Software Testing Roadmap for 2030"
  authors: Wang, Zhao, Xie, Liu, Hou, Zou, Wang (7)
  evidence: arXiv abs 2502.20812 直抓，title/authors/date(2025/02/28) 全匹配
- key: bugstudy25
  title: "Toward Understanding Bugs in Vector Database Management Systems"
  authors: Xie, Hou, Zhao, Wang, Chen, Wang (6)
  evidence: arXiv abs 2506.02617 直抓，全匹配 (2025/06/03)
- key: vdbfuzz26
  title: "VDBFuzz: Understanding and Detecting Crash Bugs in Vector Database Management Systems"
  authors: Wang, Zhao, Xie, Liu, Hou, Zou, Wang (7)
  evidence: ICSE 2026 research track 官方页面（conf.researchr.org）+ NUS TEST Lab 页；DBLP 尚未收录（2026 会议收录滞后，正常）
- key: metmap24
  title: "MeTMaP: Metamorphic Testing for Detecting False Vector Matching Problems in LLM Augmented Generation"
  authors: Wang, Li, Liu, Deng, Li, Xu, Liu, Wang, Wang (9)
  evidence: FORGE 2024 research track 官方页面 + DBLP WangLLDL0L0W24
- key: satori25
  title: "SATORI: Static Test Oracle Generation for REST APIs"
  authors: Alonso, Martin-Lopez, Segura, Bavota, Ruiz-Cortés (5)
  evidence: arXiv abs 2508.16318 + DBLP conf/kbse/AlonsoMSBR25 (ASE 2025) 双确认
- key: mastor26
  title: "MASTOR: A Multi-Agent Approach to Semantic Test Oracle Generation for RESTful APIs"
  authors: Deng, Huang, Yang, Zhang, Xie, Wang (6)
  evidence: arXiv abs 2606.10465 直抓，全匹配 (2026/06/09)；id 虽新但真实
- key: agoraplus25
  title: "Test Oracle Generation for REST APIs"（AGORA+，TOSEM 期刊扩展版）
  authors: Alonso, Juan C.; Ernst, Michael D.; Segura, Sergio; Ruiz-Cortés, Antonio (4)
  evidence: 用户点名复核（2026-08-26 同日第二会话）。Crossref API works/10.1145/3726524 +
    DBLP journals/tosem/AlonsoESR26 双确认：title/authors(4/4)/journal(TOSEM)/DOI 全匹配。
    ACM DL 页 403 系反爬，非不存在（Crossref 即 DOI 注册记录）。
  年份细节: bib year=2025 ↔ 在线首发 2025-12-11（Crossref issued）；正式期号
    TOSEM 35(1), 19:1-19:37, 2026-01-31（Crossref published-print 与 DBLP 均为 2026）。
    2025 可辩护（online-first），但按 DBLP/期号惯例应引 2026 → 已报告用户，待决定。
  可选补全: volume=35, number=1, pages=19:1-19:37（.bib 现缺）。
- key: testora26
  title: "Testora: Using Natural Language Intent to Detect Behavioral Regressions"
  authors: Pradel, Michael (1)
  evidence: arXiv abs 2503.18597 直抓，全匹配 (2025/03/24)
- key: haldar25
  title: "Rating Roulette: Self-Inconsistency in LLM-As-A-Judge Frameworks"
  authors: Haldar, Rajarshi; Hockenmaier, Julia
  evidence: arXiv abs 2510.27106 + aclanthology.org/2025.findings-emnlp.1361/（Findings of EMNLP 2025）
  status: MISMATCH — 论文真实存在，但 .bib 作者字段错误：`Reshma` 应为 `Rajarshi`，`and others` 应为 `Hockenmaier, Julia`（共 2 人）→ 需修正

### ok — 基线（Round 16 DBLP-verified 声称，自上次提交未改动，本次按增量请求跳过深核）
- key: buzzbee24 — "BUZZBEE: Towards Generic Database Management System Fuzzing", USENIX Security 2024
- key: norec20 — "Finding Bugs in Database Systems via Non-Optimizing Reference Engine Construction", ESEC/FSE 2020
- key: ddlcheck25 — "Detecting Schema-Related Logic Bugs in Relational DBMSs via Equivalent Database Construction", PVLDB 18, 2025
- key: du2023improving — "Improving Factuality and Reasoning in Language Models through Multiagent Debate", arXiv:2305.14325
- key: restler19 — "RESTler: Stateful REST API Fuzzing", ICSE 2019, doi:10.1109/ICSE.2019.00083
- key: quickrest20 — "QuickREST: Property-based Testing of REST APIs", ICST 2020
- key: evomaster21 — "Automated Black- and White-Box Testing of RESTful APIs with EvoMaster", IEEE Software 38(3), doi:10.1109/MS.2020.3013820
- key: tlp20 — "Finding Bugs in Database Systems via Query Partitioning", PACMPL 4(OOPSLA), doi:10.1145/3428279
- key: dqe20 — "Testing Database Engines via Pivoted Query Execution", ICSE 2020
- key: wang22sc — "Self-Consistency Improves Chain of Thought Reasoning in Language Models", ICLR 2023
- key: barr15 — "The Oracle Problem in Software Testing: A Survey", IEEE TSE 41(7), 2015
- key: ji23hall — "Survey of Hallucination in Natural Language Generation", ACM CSUR 55(12), doi:10.1145/3571730
- key: manes21 — "The Art, Science, and Engineering of Fuzzing: A Survey", IEEE TSE 47(11), doi:10.1109/TSE.2019.2946563
- key: amann19 — "A Systematic Evaluation of Static API-Misuse Detectors", IEEE TSE 46(12), doi:10.1109/TSE.2018.2827384
- key: claessen00 — "QuickCheck: A Lightweight Tool for Random Testing of Haskell Programs", ICFP 2000
- key: hou23llmse — "Large Language Models for Software Engineering: A Systematic Literature Review", TOSEM 33(5), doi:10.1145/3695988
- key: meyer92dbc — "Applying 'Design by Contract'", IEEE Computer 25(10), 1992
- key: he2025lma — "LLM-Based Multi-Agent Systems for Software Engineering", TOSEM 34(5), doi:10.1145/3712003
- key: schemathesis — "Schemathesis: Property-Based API Testing for OpenAPI and GraphQL", https://schemathesis.io
- key: lin2023forest — "foREST: A Tree-based Black-box Fuzzing Approach for RESTful APIs", ISSRE 2023, doi:10.1109/ISSRE59848.2023.00023
- key: lyu2023miner — "MINER: A Hybrid Data-Driven Approach for REST API Fuzzing", USENIX Security 2023
- key: chen2024dyner — "DynER: Optimized Test Case Generation for RESTful API Fuzzers...", Electronics 13(17):3476, doi:10.3390/electronics13173476
- key: kim2025llamaresttest — "LlamaRestTest: Effective REST API Testing with Small Language Models", ESEC/FSE 2025
- key: panickssery24 — "LLM Evaluators Recognize and Favor Their Own Generations", arXiv:2404.13076
- key: toradocu16 — "Automatic Generation of Oracles for Exceptional Behaviors", ISSTA 2016, doi:10.1145/2931037.2931062
- key: doc2oracll25 — "Doc2OracLL: Investigating the Impact of Documentation on LLM-Based Test Oracle Generation", FSE 2025, doi:10.1145/3729354
- key: chatassert24 — "ChatAssert: LLM-Based Test Oracle Generation With External Tools Assistance", IEEE TSE 51(1), doi:10.1109/TSE.2024.3519159
- key: augmentest25 — "AugmenTest: Enhancing Tests with LLM-Driven Oracles", arXiv:2501.17461
- key: konstantinou24 — "Do LLMs Generate Test Oracles that Capture the Actual or the Expected Program Behaviour?", arXiv:2410.21136
- key: wataoka24 — "Self-Preference Bias in LLM-as-a-Judge", arXiv:2410.21819
- key: iso9646 — "ISO/IEC 9646 Conformance Testing Methodology and Framework", 1994

## Unverified
（无）

## 结构检查（2026-08-26）
- 22 个被引 key 全部存在于 .bib，无 FAIL。
- 18 条 .bib 条目从未被 \cite（WARNING，ACM 样式下不渲染进 PDF，属死条目）：
  buzzbee24, norec20, ddlcheck25, du2023improving, restler19, evomaster21, tlp20, dqe20,
  wang22sc, amann19, meyer92dbc, he2025lma, lin2023forest, lyu2023miner, chen2024dyner,
  kim2025llamaresttest, konstantinou24, iso9646
- 格式：未发现 "句号后引用" / "\cite 前缺 ~" 问题。
- 风格不一致（minor）：booktitle 三种写法混用（"Proceedings of the …" / "Proc.\ of the …" / "Proc. …"）；
  USENIX Security 两种写法（buzzbee24 全称 vs lyu2023miner 裸写）；arXiv 条目 howpublished=
  （roadmap25/bugstudy25/du2023improving）与 note={arXiv:…}（mastor26/panickssery24/augmentest25/
  konstantinou24/wataoka24）混用；key 与年份不一致属命名习惯（wang22sc→2023, amann19→2020,
  chatassert24→2025），非错误。
