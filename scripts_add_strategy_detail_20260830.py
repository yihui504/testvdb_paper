# -*- coding: utf-8 -*-
"""给 tp-strategy-attribution-2026-08-30.json 每条 TP 加 strategy_detail（具体策略下钻）"""
import json

P = 'results/tp-strategy-attribution-2026-08-30.json'
d = json.load(open(P, encoding='utf-8'))

# (vendor, number) -> (具体策略ID, 依据说明)
DETAIL = {
    # --- boundary 25 ---
    ('qdrant', 9017): ('B1 边界值攻击(range)', 'hnsw_ef=0 低于下界被接受；BS-04 boundary_value_attack 映射'),
    ('qdrant', 9039): ('B3 维度不匹配攻击', '64 维向量入 128 维集合；dimension_mismatch 触发脚本'),
    ('qdrant', 9045): ('B4 特殊值攻击', '零长度向量 []（空集合特殊值）→ wait=false panic'),
    ('qdrant', 9149): ('B1 边界值攻击(range)', 'shard_number=0/-1 低于下界被接受（Type1_IllegalSuccess）'),
    ('qdrant', 9421): ('B1 边界值攻击(range)', 'standalone 部署形态下调 cluster 端点（部署配置边界）；脚本自述 boundary_value/type_confusion'),
    ('qdrant', 9520): ('B6 资源极限/DoS', 'shard_number=INT_MAX → 服务器无响应；VERDICT=Type3_RuntimeFailure，缺陷本体是实现极限非数值校验'),
    ('qdrant', 9522): ('B4 特殊值攻击', 'lookup_from 指向不存在的集合（引用特殊值）→ 应失败却 200'),
    ('qdrant', 9942): ('S1 Behavioral Contract', 'OpenAPI schema 声明与实现校验漂移（doc-consistency 面的行为契约）；人工契约对比非脚本'),
    ('qdrant', 10120): ('S5 搜索语义正确性', 'count exact=false 基数估计系统性 -35%（统计语义正确性）'),
    ('weaviate', 11399): ('B1 边界值攻击(range)', 'dynamicEfMin > dynamicEfMax 范围反转（跨字段 range 不变量）'),
    ('weaviate', 11400): ('B1 边界值攻击(range)', 'flatSearchCutoff=-100 低于下界'),
    ('weaviate', 11401): ('B1 边界值攻击(range)', 'replicationFactor=-1 越界被归一化为 1'),
    ('weaviate', 11729): ('B1 边界值攻击(range)', 'desiredCount=[-1,-8]→200 而 =0→422（下界不一致）'),
    ('weaviate', 11730): ('B4 特殊值攻击', 'tokenization=""（枚举外空串特殊值）'),
    ('weaviate', 11732): ('B4 特殊值攻击', 'distance=null（特殊值）被静默回读为 cosine；证据 JSON 标 unknown_enum/Type1'),
    ('weaviate', 11741): ('B4 特殊值攻击', 'activityStatus=""（空串特殊值）vs 合法值 422 对照'),
    ('weaviate', 12041): ('B7 Malformed Input', 'batch delete 缺 match.where/match.class（结构畸形）→ 500；脚本 boundary_batch_delete_limit_001.py'),
    ('milvus', 49823): ('B1 边界值攻击(range)', 'nprobe=0 越界'),
    ('milvus', 49843): ('B1 边界值攻击(range)', 'collection.ttl.seconds=-1 负值被静默丢弃'),
    ('milvus', 49889): ('B4 特殊值攻击', 'dbName=""（空串特殊值）'),
    ('milvus', 49890): ('B2 类型边界攻击(type)', 'Request-Timeout 头 3.5/"abc" 类型混淆'),
    ('milvus', 49930): ('B1 边界值攻击(range)', 'ef=0/-1、nprobe=0/-1 家族'),
    ('milvus', 50018): ('B4 特殊值攻击', 'aliases/list collectionName=""（空串特殊值）'),
    ('milvus', 50353): ('B1 边界值攻击(range)', 'limit=0/-1（主缺陷）+ 维度不匹配（伴生，B3 双缺陷 issue）'),
    ('milvus', 50354): ('B2 类型边界攻击(type)', '密码 "abcdefgh" 违反复杂度格式约束（pattern 类校验缺失）'),
    ('milvus', 50355): ('ST3 Upsert 幂等性', 'state upsert_idempotence 脚本 Scenario E：autoID 集合上显式 PK upsert → 1804'),
    ('milvus', 51084): ('S1 Behavioral Contract', 'consistencyLevel="Invalid" 静默替换为 Bounded（契约要求拒绝）'),
    ('milvus', 51085): ('S1 Behavioral Contract', 'vectorFieldType 静默替换（silent default substitution 同族）'),
    ('milvus', 52307): ('S4 隐式类型转换', 'upsert JSON 字段接受非法 JSON 字符串 → REST/gRPC 存储不一致'),
    ('milvus', 52308): ('ST1 CRUD 后一致性', 'insert 接受字符串 PK 强转 [123]（写入形态 vs 输入不一致）；state_pkautoid 脚本，oracle=gRPC 拒绝'),
    ('milvus', 52309): ('B1 边界值攻击(range)', 'group_size=0/-1 越界（gRPC 拒绝 REST 接受）'),
    ('milvus', 52310): ('S4 隐式类型转换', 'insert 标量强转 string→Int64/int→VarChar 等'),
    ('milvus', 52311): ('B2 类型边界攻击(type)', 'group_by_field=vector（字段类型不符取值域；向量字段不可作分组键）'),
    ('milvus', 52312): ('ST3 Upsert 幂等性', 'upsert 端点字符串 PK 强转（R22 state_pkautoid 家族延伸）'),
    ('milvus', 52313): ('S4 隐式类型转换', 'insert JSON 字段裸字符串 → REST/gRPC 双写格式不一致（round-trip 失败）'),
    ('milvus', 52314): ('S4 隐式类型转换', 'upsert 标量强转 string→DOUBLE/BOOL 等'),
    ('milvus', 52315): ('S4 隐式类型转换', 'insert 向量接受字符串编码 "[0.1,...]"（gRPC 拒绝）'),
    ('milvus', 52325): ('S1 Behavioral Contract', 'strictGroupSize=true 被静默忽略（契约要求强制，oracle=gRPC）'),
    # unknown 组不加 detail
}

n = 0
for tp in d['tps']:
    key = (tp['vendor'], tp['number'])
    if key in DETAIL:
        tp['strategy_detail'] = DETAIL[key][0]
        tp['detail_basis'] = DETAIL[key][1]
        n += 1
    else:
        tp['strategy_detail'] = '—（unknown，无生成证据）'
        tp['detail_basis'] = ''

# 具体策略汇总
from collections import Counter
c = Counter(tp.get('strategy_detail') for tp in d['tps'] if not tp['strategy_detail'].startswith('—'))
d['summary_by_detail_strategy'] = dict(c.most_common())
d['_meta']['detail_note'] = 'strategy_detail 按 mftui/TestVDB/agents 三 attack 规范的 21 条内置策略（B1-B7/S1-S7/ST1-ST7）定级；口径=生成/触发该 TP 的具体策略，oracle 对拍系列按最接近内置策略归位。unknown 8 条不定级。'
d['_meta']['zero_yield_strategies'] = [
    'B5 错误消息质量(Type-2)', 'S2 错误诊断质量(Type-2)', 'S3 合法输入被错误拒绝(Type-1反向)',
    'S6 Metamorphic 关系', 'S7 过滤参数语义', 'ST2 DELETE 后一致性', 'ST4 并发操作',
    'ST5 事务边界', 'ST6 索引构建期一致性', 'ST7 生命周期并发']

json.dump(d, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'updated {n}/46 with strategy_detail')
for k, v in c.most_common():
    print(f'  {k}: {v}')
print('sum(detailed):', sum(c.values()))
