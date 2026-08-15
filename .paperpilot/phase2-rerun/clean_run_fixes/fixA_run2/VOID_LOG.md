# fixA_run2 作废记录

| did | 次数 | 原因 | 处置 |
|-----|------|------|------|
| weaviate_002 | 首判 | reviewer 会话越界：派发仅含 weaviate_001，agent 自行判同版本 4 case（违反纪律 §4.4） | 判词作废（voided/ 仅存 weaviate_004，002/003 原件被编排归档失误覆盖，见下行）；新会话重判 |
| weaviate_003 | 首判 | 同上 | 同上 |
| weaviate_004 | 首判 | 同上 | 判词存 voided/weaviate_004.json；新会话重判 |
| milvus_002 | 首判 | 编排归档失误：三个 case 判词 mv 至同一目标目录未重命名，互相覆盖（weaviate_001 存活，milvus_002/qdrant_001 丢失） | 新会话重判；此后归档一律走 archive_verdict.py（校验+重命名一步完成） |
| qdrant_001 | 首判 | 同上 | 同上 |
| qdrant_002 | 首判 | 编排失误：派发时容器仍为 1.12.1（case 为 1.18.0），运行时验证打错版本（纪律 §5.1） | 判词存 voided/qdrant_002_r1.json；切容器至 1.18.0 后新会话重判 |
| milvus_009 | 首判 | 判词平铺格式无 verdicts 数组（SOP 输出格式违约，同 clean_run 先例） | 判词存 voided/milvus_009_r1.json；新会话重判 |
| qdrant_008 | 首判 | source_excerpt 空 + files_examined 空（SOP 硬约束：无接地=审查无效） | 判词存 voided/qdrant_008_r1.json；新会话重判 |
| qdrant_013 | 首判 | 判词平铺格式无 verdicts 数组（SOP 输出格式违约） | 判词存 voided/qdrant_013_r1.json；新会话重判 |
