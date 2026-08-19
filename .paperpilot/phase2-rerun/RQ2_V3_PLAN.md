# RQ2 v3 执行计划（ADR-0008 新链路 × Phase 2 实验集）— 2026-08-17

## 方案（已拍板）
- 载体：Phase 2 实验集 71 case（材料/容器/clone 与 clean_run 完全同源）
- 判定链路：evidence-builder（逐 case fan-out）→ chain-auditor（**按组收口**，15 组）
- 派发：gen_dispatch_v3.py（builder prompts + auditor prompt）
- 容器：复用 start_container.py，同容器组内串行、3 vendor 并行（clean_run 同协议）
- 产出：各 (vendor,version)/debate_logs/chain_verdicts.json → 汇总与 GT 44 对照

## 15 组执行清单

### milvus 2.3（1 case）

```bash
python start_container.py milvus 2.3   # 容器就绪后：
python gen_dispatch_v3.py milvus 2.3 milvus_001           # builder × 1
python gen_dispatch_v3.py milvus 2.3 milvus_001 --auditor # 收口 × 1
```

### milvus 2.6.10（6 case）

```bash
python start_container.py milvus 2.6.10   # 容器就绪后：
python gen_dispatch_v3.py milvus 2.6.10 milvus_002,milvus_003,milvus_004,milvus_005,milvus_006,milvus_007           # builder × 6
python gen_dispatch_v3.py milvus 2.6.10 milvus_002,milvus_003,milvus_004,milvus_005,milvus_006,milvus_007 --auditor # 收口 × 1
```

### milvus 2.6.12（1 case）

```bash
python start_container.py milvus 2.6.12   # 容器就绪后：
python gen_dispatch_v3.py milvus 2.6.12 milvus_008           # builder × 1
python gen_dispatch_v3.py milvus 2.6.12 milvus_008 --auditor # 收口 × 1
```

### milvus 2.6.16（12 case）

```bash
python start_container.py milvus 2.6.16   # 容器就绪后：
python gen_dispatch_v3.py milvus 2.6.16 milvus_009,milvus_010,milvus_011,milvus_012,milvus_013,milvus_014,milvus_015,milvus_016,milvus_017,milvus_018,milvus_019,milvus_020           # builder × 12
python gen_dispatch_v3.py milvus 2.6.16 milvus_009,milvus_010,milvus_011,milvus_012,milvus_013,milvus_014,milvus_015,milvus_016,milvus_017,milvus_018,milvus_019,milvus_020 --auditor # 收口 × 1
```

### milvus 2.6.17（11 case）

```bash
python start_container.py milvus 2.6.17   # 容器就绪后：
python gen_dispatch_v3.py milvus 2.6.17 milvus_021,milvus_022,milvus_023,milvus_024,milvus_025,milvus_026,milvus_027,milvus_028,milvus_029,milvus_030,milvus_031           # builder × 11
python gen_dispatch_v3.py milvus 2.6.17 milvus_021,milvus_022,milvus_023,milvus_024,milvus_025,milvus_026,milvus_027,milvus_028,milvus_029,milvus_030,milvus_031 --auditor # 收口 × 1
```

### milvus 2.6.19（2 case）

```bash
python start_container.py milvus 2.6.19   # 容器就绪后：
python gen_dispatch_v3.py milvus 2.6.19 milvus_032,milvus_033           # builder × 2
python gen_dispatch_v3.py milvus 2.6.19 milvus_032,milvus_033 --auditor # 收口 × 1
```

### milvus 3.0.0（10 case）

```bash
python start_container.py milvus 3.0.0   # 容器就绪后：
python gen_dispatch_v3.py milvus 3.0.0 milvus_034,milvus_035,milvus_036,milvus_037,milvus_038,milvus_039,milvus_040,milvus_041,milvus_042,milvus_043           # builder × 10
python gen_dispatch_v3.py milvus 3.0.0 milvus_034,milvus_035,milvus_036,milvus_037,milvus_038,milvus_039,milvus_040,milvus_041,milvus_042,milvus_043 --auditor # 收口 × 1
```

### qdrant 1.12.1（1 case）

```bash
python start_container.py qdrant 1.12.1   # 容器就绪后：
python gen_dispatch_v3.py qdrant 1.12.1 qdrant_001           # builder × 1
python gen_dispatch_v3.py qdrant 1.12.1 qdrant_001 --auditor # 收口 × 1
```

### qdrant 1.18.0（3 case）

```bash
python start_container.py qdrant 1.18.0   # 容器就绪后：
python gen_dispatch_v3.py qdrant 1.18.0 qdrant_002,qdrant_003,qdrant_004           # builder × 3
python gen_dispatch_v3.py qdrant 1.18.0 qdrant_002,qdrant_003,qdrant_004 --auditor # 收口 × 1
```

### qdrant 1.18.1（2 case）

```bash
python start_container.py qdrant 1.18.1   # 容器就绪后：
python gen_dispatch_v3.py qdrant 1.18.1 qdrant_005,qdrant_006           # builder × 2
python gen_dispatch_v3.py qdrant 1.18.1 qdrant_005,qdrant_006 --auditor # 收口 × 1
```

### qdrant 1.18.2（11 case）

```bash
python start_container.py qdrant 1.18.2   # 容器就绪后：
python gen_dispatch_v3.py qdrant 1.18.2 qdrant_007,qdrant_008,qdrant_009,qdrant_010,qdrant_011,qdrant_012,qdrant_013,qdrant_014,qdrant_015,qdrant_016,qdrant_017           # builder × 11
python gen_dispatch_v3.py qdrant 1.18.2 qdrant_007,qdrant_008,qdrant_009,qdrant_010,qdrant_011,qdrant_012,qdrant_013,qdrant_014,qdrant_015,qdrant_016,qdrant_017 --auditor # 收口 × 1
```

### qdrant 1.18.3（1 case）

```bash
python start_container.py qdrant 1.18.3   # 容器就绪后：
python gen_dispatch_v3.py qdrant 1.18.3 qdrant_018           # builder × 1
python gen_dispatch_v3.py qdrant 1.18.3 qdrant_018 --auditor # 收口 × 1
```

### weaviate 1.37.4（4 case）

```bash
python start_container.py weaviate 1.37.4   # 容器就绪后：
python gen_dispatch_v3.py weaviate 1.37.4 weaviate_001,weaviate_002,weaviate_003,weaviate_004           # builder × 4
python gen_dispatch_v3.py weaviate 1.37.4 weaviate_001,weaviate_002,weaviate_003,weaviate_004 --auditor # 收口 × 1
```

### weaviate 1.38.0（4 case）

```bash
python start_container.py weaviate 1.38.0   # 容器就绪后：
python gen_dispatch_v3.py weaviate 1.38.0 weaviate_005,weaviate_006,weaviate_007,weaviate_008           # builder × 4
python gen_dispatch_v3.py weaviate 1.38.0 weaviate_005,weaviate_006,weaviate_007,weaviate_008 --auditor # 收口 × 1
```

### weaviate 1.38.2（2 case）

```bash
python start_container.py weaviate 1.38.2   # 容器就绪后：
python gen_dispatch_v3.py weaviate 1.38.2 weaviate_009,weaviate_010           # builder × 2
python gen_dispatch_v3.py weaviate 1.38.2 weaviate_009,weaviate_010 --auditor # 收口 × 1
```

## 指标与对照（跑完后）
- 各组 chain_verdicts.json 汇总 → vs GT（44 TP / 27 FP）
- recall / precision / fp_supp + **fp_evidence_source 分布**（doc/source/both/behavior）
  + root_cause 分布（RQ2 人工核查的直接输入）
- 过滤前后对比：前 = clean 0.533 / fixF 三轮中位 0.591；后 = 新链路
- 方差观测：多轮复跑可对比旧 κ 0.19-0.32（新链路理论上方差收窄——auditor 收口固定规则）

## 已知条件（勿当事故）
- milvus_001 output log = "[no raw HTTP captured]"（gRPC 真实形态，builder 如实 grade D）
- qdrant_015 曾致容器 OOM(137)（INT_MAX shard 实测）——遇退出码 137 重建容器重派
