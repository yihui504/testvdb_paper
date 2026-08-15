# fixC 作废记录

| did | 次数 | 原因 | 处置 |
|-----|------|------|------|
| qdrant_004 | 首判 | 判词 JSON 损坏（Invalid control character，引号转义缺失） | 判词存 voided/qdrant_004_r1.json；新会话重判 |
| milvus_022 | 首判 | 编排失误：派发时容器仍 2.6.16（case 为 2.6.17），运行时验证打错版本（纪律 §5.1） | 判词存 voided/milvus_022_r1.json；切容器 2.6.17 后重判 |
| milvus_025 | 首判 | 判词 JSON 损坏（Expecting ',' delimiter） | 判词存 voided/milvus_025_r1.json；新会话重判 |
