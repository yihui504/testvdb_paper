"""Fill the HR-17 adjudication worksheet with verdicts + one-line bases.
Adjudication stance: deployment-channel human reviewer judging from pack
materials only (CONFIRM / RETURN / REJECT), GT not consulted."""
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

WS = (r"c:/Users/11428/Desktop/testvdb_paper/.paperpilot/phase2-rerun/"
      r"arms/rq2_3run/rerun_v3/HR17_adjudication_worksheet.md")

V = {
 "milvus_001": ("RETURN", "包内零观察记录零契约行——材料层面不可判，退回补材料"),
 "milvus_004": ("REJECT", "记录在案的行为面自洽（IN 集合语义删 age=10 正确）；剩余声称（c2 空集删除）无日志支撑"),
 "milvus_005": ("CONFIRM", "写读不对称两轮复现（insert '123field' code=0 vs query 同名 65535）+源码双面定位（insert 无命名校验/query ParseIdentifier 拒绝）"),
 "milvus_006": ("REJECT", "前提失真——quick-create 集合无声明字段，text_field 系动态键，数值直存属 JSON 动态字段固有语义"),
 "milvus_012": ("REJECT", "空 dbName 解析为 default 属等价缺省回退；文档断言仅描述性（'an existing database'）无拒绝承诺可违反"),
 "milvus_013": ("CONFIRM", "数值语义头 Request-Timeout 接受 'abc'/'3.5' 静默回落默认超时返回成功；源码 ParseInt 失败被静默吞掉"),
 "milvus_030": ("REJECT", "包内无密码复杂度文档承诺——doc-impl 缺陷类无文档锚点可违反（长度下界已强制：1 字符→1100）"),
 "milvus_031": ("RETURN", "两次请求均被 1804 拒绝且根因是探针携带 schema 外字段 color——声称的 autoID-upsert 缺 PK 面未被隔离观察，退回重跑探针"),
 "milvus_036": ("CONFIRM", "groupSize=0/-1 REST 接受 code=0（log 在案）vs proxy 面同值明文拒绝+官方测试期望报错——接口不对称"),
 "milvus_038": ("CONFIRM", "同族不一致——binary vector group-by 显式拒绝 vs float vector 静默退化普通 top-k（isSameGroupByValue 恒 false）；gRPC 对照腿被 metric 噪声污染不计"),
 "milvus_043": ("CONFIRM", "strictGroupSize=true+groupSize=2 每组仍返回 3 条（REST/gRPC 双面复现）；源码 strict 逻辑在场但端到端未生效"),
 "qdrant_014": ("CONFIRM", "standalone 前提 /cluster/recover 报 500 Service error vs 同文件 remove_peer 同前提 400——同族错误码不一致且无明文意图注释"),
 "qdrant_015": ("CONFIRM", "shard_number=INT_MAX 创建后两轮服务全超时不可用；源码仅 NonZeroU32 下界无上界护栏（控制组 422 声称无日志支撑，不计）"),
 "qdrant_016": ("CONFIRM", "不存在的 lookup 集合：ID 引用路径 404 vs raw-vector 路径静默 200 回退当前集合——同族不一致+认知盲区现象级命中"),
 "qdrant_026": ("REJECT", "并列得分（全 1.0）次序漂移无文档确定性承诺——未承诺行为不构成 doc-impl 缺陷；HNSW 认知模式与全量扫描并列不同构"),
 "qdrant_027": ("CONFIRM", "field_schema 数组形式（值域闭集外）实测 200 acknowledged 接受且索引未落——枚举闭集违反被接受在案"),
 "weaviate_007": ("REJECT", "源码明文注释空白值落默认 cosine——满足红线 3 明文 by-design 标准"),
}

t = open(WS, encoding="utf-8").read()
for case, (verdict, base) in V.items():
    sec = t.split(f"## {case} ", 1)
    assert len(sec) == 2, case
    head, rest = sec[0], sec[1]
    marks = {"CONFIRM": "x" if verdict == "CONFIRM" else " ",
             "RETURN": "x" if verdict == "RETURN" else " ",
             "REJECT": "x" if verdict == "REJECT" else " "}
    line = (f"- 裁决: [{marks['CONFIRM']}] CONFIRM   [{marks['RETURN']}]"
            f" RETURN   [{marks['REJECT']}] REJECT   备注: {base}")
    rest2 = re.sub(r"- 裁决: \[ \] CONFIRM   \[ \] RETURN   \[ \] REJECT   备注:",
                   line, rest, count=1)
    assert rest2 != rest, f"blank line not found for {case}"
    t = head + f"## {case} " + rest2
open(WS, "w", encoding="utf-8").write(t)

from collections import Counter
c = Counter(v for v, _ in V.values())
print("verdicts:", dict(c), "total:", sum(c.values()))
