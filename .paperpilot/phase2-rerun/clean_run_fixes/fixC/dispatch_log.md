# fixC 派发记录表（纪律 §7.1）

> Run 标识：**fixC**（2026-08-15 起）。配置 = v2 材料 + fixA 锚点 + **SOP 证据消解次序 patch**（见 FIXC_PLAN.md §2）。
> 派发 prompt = clean_run/prompts/ 原文（零改动）；模型统一标准档 GLM-5.2（每 case 新会话）。
> 子集 = SPLIT 32（三轮分歧）+ 对照 6 = 38 case，预注册于 FIXC_PLAN.md §3。

| # | did | vendor | version | reviewer 会话 | 派发时间 | 判词 | 校验 | 备注 |
|---|-----|--------|---------|--------------|---------|------|------|------|
| 1 | milvus_002 | milvus | 2.6.10 | agent-c-01 | 2026-08-15 | CONFIRMED | PASS | SPLIT(r1C r2C r3F gt=B)；B视角CONFIRMED聚合 |
| 2 | qdrant_002 | qdrant | 1.18.0 | agent-c-02 | 2026-08-15 | FALSE_POSITIVE | PASS | 对照(E4类 by-design)保持✓ |
| 3 | weaviate_001 | weaviate | 1.37.4 | agent-c-03 | 2026-08-15 | CONFIRMED | PASS | 对照保持✓ |
| 4 | milvus_004 | milvus | 2.6.10 | agent-c-04 | 2026-08-15 | FALSE_POSITIVE | PASS | SPLIT(r1F r2C r3F gt=B)；filter 语义误解 |
| 5 | qdrant_003 | qdrant | 1.18.0 | agent-c-05 | 2026-08-15 | CONFIRMED | PASS | SPLIT(r1F r2C r3C gt=C)；B视角物理约束→C（gt=C 错向） |
| 6 | weaviate_004 | weaviate | 1.37.4 | agent-c-06 | 2026-08-15 | CONFIRMED | PASS | SPLIT(r1F r2C r3C gt=C)；C（gt=C 错向） |
| 8 | qdrant_004 | qdrant | 1.18.0 | agent-c-08 | 2026-08-15 | FALSE_POSITIVE | VOID | JSON 损坏→作废重判(VOID_LOG) |
| 9 | weaviate_006 | weaviate | 1.38.0 | agent-c-09 | 2026-08-15 | CONFIRMED | PASS | SPLIT(r1F r2F r3C gt=B)；契约枚举 A压倒 |
| 10 | milvus_006 | milvus | 2.6.10 | agent-c-10 | 2026-08-15 | CONFIRMED | PASS | SPLIT(r1C r2C r3F gt=B)；E1实测200+E2锚点 |
| 11 | qdrant_004 | qdrant | 1.18.0 | agent-c-11 | 2026-08-15 | FALSE_POSITIVE | PASS | 重判(JSON损坏作废)；SPLIT(r1C r2F r3C gt=A)；实测400拒绝→FP 错向 |
| 12 | milvus_007 | milvus | 2.6.10 | agent-c-12 | 2026-08-15 | FALSE_POSITIVE | PASS | SPLIT(r1F r2C r3F gt=C)；FP 对向 |
| 13 | qdrant_007 | qdrant | 1.18.2 | agent-c-13 | 2026-08-15 | FALSE_POSITIVE | PASS | SPLIT(r1F r2C r3F gt=C)；FP 对向（前置校验=原子语义） |
| 14 | weaviate_008 | weaviate | 1.38.0 | agent-c-14 | 2026-08-15 | CONFIRMED | PASS | SPLIT(r1C r2C r3F gt=B)；对向；weaviate 4/4 完成 |
| 15 | milvus_009 | milvus | 2.6.16 | agent-c-15 | 2026-08-15 | CONFIRMED | PASS | SPLIT(r1C r2C r3F gt=B)；对向；B 物理约束驱动 |
| 16 | qdrant_009 | qdrant | 1.18.2 | agent-c-16 | 2026-08-15 | FALSE_POSITIVE | PASS | SPLIT(r1F r2C r3C gt=C)；对向；E5/A、B NEUTRAL |
| 17 | milvus_013 | milvus | 2.6.16 | agent-c-17 | 2026-08-15 | FALSE_POSITIVE | PASS | SPLIT(r1F r2C r3C gt=A)；FP 错向（graceful degradation；E3无声 vs E5） |
| 18 | qdrant_010 | qdrant | 1.18.2 | agent-c-18 | 2026-08-15 | CONFIRMED | PASS | SPLIT(r1F r2C r3F gt=C)；C 错向（契约"fully initialized"） |
| 19 | milvus_016 | milvus | 2.6.16 | agent-c-19 | 2026-08-15 | FALSE_POSITIVE | PASS | SPLIT(r1F r2C r3C gt=B)；FP 错向（架构分层解读，E5 适用但 B 视角未触发） |
| 20 | qdrant_011 | qdrant | 1.18.2 | agent-c-20 | 2026-08-15 | FALSE_POSITIVE | PASS | SPLIT(r1C r2F r3F gt=C)；对向（显式 null 处理） |
| 21 | milvus_022 | milvus | 2.6.17 | agent-c-21 | 2026-08-15 | FALSE_POSITIVE | VOID | 容器版本错配(2.6.16)→作废重判(VOID_LOG) |
| 22 | milvus_022 | milvus | 2.6.17 | agent-c-22 | 2026-08-15 | FALSE_POSITIVE | PASS | 重判(错配作废)；对照(E3类)保持✓；显式引用 E3 消解 |
| 23 | qdrant_012 | qdrant | 1.18.2 | agent-c-23 | 2026-08-15 | CONFIRMED | PASS | SPLIT(r1C r2F r3F gt=C)；C 错向（must_not 结构非显式意图） |
| 24 | milvus_021 | milvus | 2.6.17 | agent-c-24 | 2026-08-15 | CONFIRMED | PASS | SPLIT(r1F r2F r3C gt=C)；C 错向（错误码选择缺陷化） |
| 25 | qdrant_017 | qdrant | 1.18.2 | agent-c-25 | 2026-08-15 | FALSE_POSITIVE | PASS | 对照(E4类)保持✓；qdrant 8/8 完成 |
| 26 | milvus_023 | milvus | 2.6.17 | agent-c-26 | 2026-08-15 | FALSE_POSITIVE | PASS | SPLIT(r1F r2F r3C gt=C)；对向；显式引用 E3 消解 |
| 27 | milvus_024 | milvus | 2.6.17 | agent-c-27 | 2026-08-15 | FALSE_POSITIVE | PASS | SPLIT(r1F r2F r3C gt=B)；FP 错向（未定义字段忽略=标准绑定行为） |
| 28 | milvus_025 | milvus | 2.6.17 | agent-c-28 | 2026-08-15 | CONFIRMED | VOID | JSON 损坏→作废重判(VOID_LOG) |
| 29 | milvus_025 | milvus | 2.6.17 | agent-c-29 | 2026-08-15 | CONFIRMED | PASS | 重判(JSON损坏作废)；SPLIT(r1C r2C r3F gt=C)；C 错向 |
| 30 | milvus_028 | milvus | 2.6.17 | agent-c-30 | 2026-08-15 | FALSE_POSITIVE | PASS | SPLIT(r1F r2C r3F gt=C)；对向；默认值填充=E3类 |
| 31 | milvus_029 | milvus | 2.6.17 | agent-c-31 | 2026-08-15 | CONFIRMED | PASS | SPLIT(r1F r2F r3C gt=B)；对向；A 契约压倒 |
| 32 | milvus_030 | milvus | 2.6.17 | agent-c-32 | 2026-08-15 | CONFIRMED | PASS | SPLIT(r1C r2F r3C gt=B)；对向；契约[8,64]vs实现[6,72] A压倒 |
| 33 | milvus_032 | milvus | 2.6.19 | agent-c-33 | 2026-08-15 | CONFIRMED | PASS | SPLIT(r1C r2F r3C gt=A)；对向；A 枚举契约压倒（vs run3 FP） |
| 34 | milvus_033 | milvus | 2.6.19 | agent-c-34 | 2026-08-15 | CONFIRMED | PASS | SPLIT(r1F r2C r3F gt=A)；对向；B 视角驱动（vs run3 FP） |
| 35 | milvus_035 | milvus | 3.0.0 | agent-c-35 | 2026-08-15 | FALSE_POSITIVE | PASS | 对照劣化✗（fixA三轮全C对）；E2未执行跨通道对照→落入E5 |
| 36 | milvus_038 | milvus | 3.0.0 | agent-c-36 | 2026-08-15 | CONFIRMED | PASS | SPLIT(r1C r2C r3F gt=A)；对向；显式执行 E2 跨通道对照 |
| 37 | milvus_039 | milvus | 3.0.0 | agent-c-37 | 2026-08-15 | CONFIRMED | PASS | SPLIT(r1C r2F r3F gt=B)；对向；E2 执行（gRPC 拒绝 vs REST 强转） |
| 38 | milvus_040 | milvus | 3.0.0 | agent-c-38 | 2026-08-15 | CONFIRMED | PASS | SPLIT(r1C r2C r3F gt=A)；对向；A 契约类型断言 |
| 39 | milvus_041 | milvus | 3.0.0 | agent-c-39 | 2026-08-15 | CONFIRMED | PASS | SPLIT(r1C r2C r3F gt=B)；对向 |
| 40 | milvus_042 | milvus | 3.0.0 | agent-c-40 | 2026-08-15 | CONFIRMED | PASS | SPLIT(r1C r2C r3F gt=A)；对向；E2 执行（gRPC 拒绝字符串向量） |
| 41 | milvus_043 | milvus | 3.0.0 | agent-c-41 | 2026-08-15 | CONFIRMED | PASS | 对照保持✓ |
