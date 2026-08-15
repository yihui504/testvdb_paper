# fixA_run3 作废记录

| did | 次数 | 原因 | 处置 |
|-----|------|------|------|
| weaviate_005 | 首判 | 编排失误：派发时容器仍为 1.37.4（case 为 1.38.0），运行时验证打错版本（纪律 §5.1） | 判词存 voided/weaviate_005_r1.json；容器已切 1.38.0，新会话重判 |
| qdrant_002/003/004 | 首判 | 编排系统性失误：qdrant 容器自 run3 开局未切换（一直 1.12.1，case 为 1.18.0），运行时验证打错版本（纪律 §5.1） | 判词存 voided/qdrant_00{2,3,4}_r1.json；切容器 1.18.0 后新会话重判 |
| qdrant_005/006 | 首判 | 同上（case 为 1.18.1） | 判词存 voided/qdrant_00{5,6}_r1.json；切容器 1.18.1 后重判 |
| qdrant_007 | 首判 | 同上（case 为 1.18.2） | 判词存 voided/qdrant_007_r1.json；切容器 1.18.2 后重判 |
| milvus_008 | 首判 | 编排失误：milvus 容器仍 2.6.10（case 为 2.6.12） | 判词存 voided/milvus_008_r1.json；切容器 2.6.12 后重判 |
| milvus_009 | 越界二判 | milvus_010 的 reviewer 会话越界重判已完成的 milvus_009（违反 §4.1 同轮二次判定禁令） | 越界判词存 voided/milvus_009_r2_stray.json（不作数）；保留 agent-r3-31 首判（CONFIRMED→实为 FP 已归档）；仅保留该会话对派发目标 milvus_010 的判定 |
| qdrant_012 | 首判 | source_excerpt 空 + files_examined 空（SOP 硬约束：无接地=审查无效） | 判词存 voided/qdrant_012_r1.json；新会话重判 |
| qdrant_012 | 二判 | 重判仍 source_excerpt 空 + files_examined 空（连续两次 SOP 接地缺失） | 判词存 voided/qdrant_012_r2.json；第三次重判 |
| milvus_021 | 首判 | source_excerpt 空 + files_examined 空（SOP 硬约束） | 判词存 voided/milvus_021_r1.json；新会话重判 |
