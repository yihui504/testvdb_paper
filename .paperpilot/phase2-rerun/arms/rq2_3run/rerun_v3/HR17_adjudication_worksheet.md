# HR-routed 17-case human adjudication worksheet

裁决口径:你是部署通道的人工裁决者。对每案,基于包内证据判断该路由案经人工审查后的去向:
- **CONFIRM** = 确认为真缺陷(HR 路由正确,人工支持确认)
- **RETURN** = 证据不足,退回/需补充材料(人工无法确认)
- **REJECT** = 经人工审查判非缺陷(HR 路由会被人工推翻)

## milvus_001  (GT=T; verdicts: {'defect_id': 'milvus_001', 'verdict': 'HUMAN_REVIEW', 'confidence': 0.3, 'perspectives': {'A': 'NEUTRAL', 'B': 'NEUTRAL', 'C': 'NEUTRAL', 'D': 'NO_SIGNAL'}, 'd_evidence': "无——包内 raw 与 log 均为空（'no raw HTTP captured'），无任何可核查的请求-响应记录", 'rationale': '链上无任何执行观察且无契约行，四视角均无证据可评，按红线4证据不足转人工（禁静默过滤）'} / {'defect_id': 'milvus_001', 'verdict': 'HUMAN_REVIEW', 'confidence': 0.5, 'perspectives': {'A': 'NEUTRAL', 'B': 'NEUTRAL', 'C': 'NEUTRAL', 'COG': 'NO_SIGNAL', 'D': 'not_found'}, 'd_evidence': '(无定位对象) 包内既无观察记录(raw 为空且 log 未捕获)也无契约行,无任何行为面可在 v2.3.0 clone 中定位', 'rationale': '包内零执行记录、零契约依据,证据不足按 v3 红线4 禁止静默过滤,转人工。'} / {'defect_id': 'milvus_001', 'verdict': 'HUMAN_REVIEW', 'confidence': 0.3, 'perspectives': {'A': 'NEUTRAL', 'B': 'NEUTRAL', 'C': 'NEUTRAL', 'D': 'NO_SIGNAL'}, 'd_evidence': 'not_found: 冻结包无任何观察记录(raw 为空且 log 未捕获),无源码定位锚点', 'rationale': '观察证据完全缺失(A 无契约行可核查、B 无请求-响应记录),按红线4证据不足转人工,不静默过滤'})

- judge rationale (run1): 链上无任何执行观察且无契约行，四视角均无证据可评，按红线4证据不足转人工（禁静默过滤）
- d_evidence: 无——包内 raw 与 log 均为空（'no raw HTTP captured'），无任何可核查的请求-响应记录
  - pack contract rows: (no surviving contract rows - evidence-absent/weak pack)
  - pack file: .paperpilot\phase2-rerun\arms\materials_complete\milvus_001.md


- 裁决: [ ] CONFIRM   [x] RETURN   [ ] REJECT   备注: 包内零观察记录零契约行——材料层面不可判，退回补材料

## milvus_004  (GT=T; verdicts: {'defect_id': 'milvus_004', 'verdict': 'HUMAN_REVIEW', 'confidence': 0.4, 'perspectives': {'A': 'NEUTRAL', 'B': 'NEUTRAL', 'C': 'NEUTRAL', 'D': 'NO_SIGNAL'}, 'd_evidence': 'v2.6.10 删除路径无针对 in 列表顺序的约束逻辑；RESP3 age in [10,5] 返回 deleteCount=1 与 IN 集合成员语义一致', 'rationale': '观察行为在 IN 集合语义下正确（顺序无关），无契约行、七类客观约束不覆盖、认知 filter-expression-leniency 非现象级命中（表达式合法且结果正确），按兜底保守转人工'} / {'defect_id': 'milvus_004', 'verdict': 'HUMAN_REVIEW', 'confidence': 0.5, 'perspectives': {'A': 'NEUTRAL', 'B': 'NEUTRAL', 'C': 'WEAK_REFUTED', 'COG': 'NO_SIGNAL', 'D': 'not_found'}, 'd_evidence': "(无承诺校验可定位) REQ3 显示 filter 'age in [10, 5]' 按集合语义仅删除 age=10 一行(deleteCount=1),语义自洽;摘要中 c2 空集声称在日志中无请求-响应记录支撑", 'rationale': '无序 IN 列表为集合语义,不属七类客观约束类(B=NEUTRAL),无契约行(A=NEUTRAL),接受无序列表系无注释裸行为(C=WEAK_REFUTED) → 按保守规则转人工。'} / {'defect_id': 'milvus_004', 'verdict': 'HUMAN_REVIEW', 'confidence': 0.35, 'perspectives': {'A': 'NEUTRAL', 'B': 'NEUTRAL', 'C': 'NEUTRAL', 'D': 'NO_SIGNAL'}, 'd_evidence': 'not_found: 无可核查契约行;摘要声称的 [c2] 空 IN 删除在冻结日志中无对应 REQ/RESP 记录', 'rationale': 'age in [10,5] 为无序 IN 列表,命中 age==10 删 1 行属正确表达式语义,不落入七类客观约束(B=NEUTRAL);且 [c2] 声称无记录支撑,证据不足转人工'})

- judge rationale (run1): 观察行为在 IN 集合语义下正确（顺序无关），无契约行、七类客观约束不覆盖、认知 filter-expression-leniency 非现象级命中（表达式合法且结果正确），按兜底保守转人工
- d_evidence: v2.6.10 删除路径无针对 in 列表顺序的约束逻辑；RESP3 age in [10,5] 返回 deleteCount=1 与 IN 集合成员语义一致
  - pack contract rows: (no surviving contract rows - evidence-absent/weak pack)
  - pack file: .paperpilot\phase2-rerun\arms\materials_complete\milvus_004.md


- 裁决: [ ] CONFIRM   [ ] RETURN   [x] REJECT   备注: 记录在案的行为面自洽（IN 集合语义删 age=10 正确）；剩余声称（c2 空集删除）无日志支撑

## milvus_005  (GT=T; verdicts: {'defect_id': 'milvus_005', 'verdict': 'HUMAN_REVIEW', 'confidence': 0.5, 'perspectives': {'A': 'NEUTRAL', 'B': 'NEUTRAL', 'C': 'CONFIRMED', 'D': 'NO_SIGNAL'}, 'd_evidence': 'v2.6.10 httpserver/utils.go:592-597 动态字段键仅保留 $meta 校验即任意键名可写入；proxy/util.go:1640-1664 查询侧经 ParseIdentifier 拒绝非标识符键（parse output field name failed）', 'rationale': '链上有实质写读不对称观察（写入 code=0、读回 65535 数据不可达），但 insert/query 为不同端点不构成七类面不对称，D 无现象级命中，按兜底 HUMAN_REVIEW（计入 CONFIRMED 口径）'} / {'defect_id': 'milvus_005', 'verdict': 'HUMAN_REVIEW', 'confidence': 0.55, 'perspectives': {'A': 'NEUTRAL', 'B': 'NEUTRAL', 'C': 'WEAK_REFUTED', 'COG': 'NO_SIGNAL', 'D': 'validation_absent'}, 'd_evidence': "internal/distributed/proxy/httpserver/utils.go:590-616(insert 侧动态字段仅拦 $meta 保留名,任意键名无校验入库) vs internal/proxy/util.go:1663-1664(query 侧 'parse output field name failed: 123field')", 'rationale': "insert 接受 '123field'/'@field' 而 query 无法解析同名(写读不对称,REQ3 vs REQ4 两轮复现),属校验缺口而非七类客观约束(B=NEUTRAL),无契约行,无明文 by-design → 转人工;D=validation_absent 支持 defect 方向。"} / {'defect_id': 'milvus_005', 'verdict': 'HUMAN_REVIEW', 'confidence': 0.5, 'perspectives': {'A': 'NEUTRAL', 'B': 'NEUTRAL', 'C': 'CONFIRMED', 'D': 'NO_SIGNAL'}, 'd_evidence': "internal/distributed/proxy/httpserver/utils.go:592-597(v2.6.10) source:validation_absent — 插入侧动态键仅拒保留键 $meta,无命名法校验;internal/proxy/util.go:1663-1664 查询侧经表达式解析器校验 outputFields 导致 'parse output field name failed'", 'rationale': '写入可成功而同名动态字段查询不可达的写入/读取不对称真实在案(RESP3 code 0 vs RESP4 code 65535)且行为不优雅,但无契约行、不落七类、认知无命中,按保守兜底转人工'})

- judge rationale (run1): 链上有实质写读不对称观察（写入 code=0、读回 65535 数据不可达），但 insert/query 为不同端点不构成七类面不对称，D 无现象级命中，按兜底 HUMAN_REVIEW（计入 CONFIRMED 口径）
- d_evidence: v2.6.10 httpserver/utils.go:592-597 动态字段键仅保留 $meta 校验即任意键名可写入；proxy/util.go:1640-1664 查询侧经 ParseIdentifier 拒绝非标识符键（parse output field name failed）
  - pack contract rows: (no surviving contract rows - evidence-absent/weak pack)
  - pack file: .paperpilot\phase2-rerun\arms\materials_complete\milvus_005.md


- 裁决: [x] CONFIRM   [ ] RETURN   [ ] REJECT   备注: 写读不对称两轮复现（insert '123field' code=0 vs query 同名 65535）+源码双面定位（insert 无命名校验/query ParseIdentifier 拒绝）

## milvus_006  (GT=T; verdicts: {'defect_id': 'milvus_006', 'verdict': 'HUMAN_REVIEW', 'confidence': 0.4, 'perspectives': {'A': 'NEUTRAL', 'B': 'NEUTRAL', 'C': 'WEAK_REFUTED', 'D': 'NO_SIGNAL'}, 'd_evidence': 'v2.6.10 httpserver/utils.go:598-616 动态字段值按 gjson.String/Number 等自描述类型直存，动态字段无声明类型可违反', 'rationale': '动态字段本身 schemaless，int 与 string 混存是其 JSON 固有语义，类型套套逻辑类前提（声明数值字段）不成立，认知 scalar-type-coercion 指声明标量字段非同构，WEAK_REFUTED 转人工'} / {'defect_id': 'milvus_006', 'verdict': 'HUMAN_REVIEW', 'confidence': 0.5, 'perspectives': {'A': 'NEUTRAL', 'B': 'NEUTRAL', 'C': 'WEAK_REFUTED', 'COG': 'NO_SIGNAL', 'D': 'by_design_in_source'}, 'd_evidence': 'internal/distributed/proxy/httpserver/utils.go:596-616(动态键按 gjson 原生类型分支存储:Number→int64/float64、String→string,text_field 系无声明类型的动态 JSON 键)', 'rationale': "候选'VARCHAR 字段接受 int'前提不成立——text_field 非声明字段,源码结构表明动态键按 JSON 原生类型存储为有意设计,但无注释级明文(红线3 不构成 REFUTED);非七类客观约束(B=NEUTRAL)、无契约行、认知 scalar-coercion 盲区(#47766)系有类型标量字段,与无类型动态键不构成现象级匹配(COG=NO_SIGNAL) → 转人工。"} / {'defect_id': 'milvus_006', 'verdict': 'FALSE_POSITIVE', 'confidence': 0.7, 'perspectives': {'A': 'NEUTRAL', 'B': 'NEUTRAL', 'C': 'REFUTED', 'D': 'NO_SIGNAL'}, 'd_evidence': "pkg/common/common.go:65-66(v2.6.10) source:by_design_in_source — 文档字符串 'MetaFieldName is the field name of dynamic schema' 表明动态字段存于 JSON 型 $meta;utils.go:604-608 显式实现 gjson.Number→int64/float64 强制转换", 'rationale': '前提失真:collection 以 quick-create(dimension-only)创建,无任何声明 VARCHAR 字段,text_field 为动态字段,接受数值属 JSON 动态字段的明文设计(认知 BDP quick-create 模式佐证),C=REFUTED 推翻候选'})

- judge rationale (run1): 动态字段本身 schemaless，int 与 string 混存是其 JSON 固有语义，类型套套逻辑类前提（声明数值字段）不成立，认知 scalar-type-coercion 指声明标量字段非同构，WEAK_REFUTED 转人工
- d_evidence: v2.6.10 httpserver/utils.go:598-616 动态字段值按 gjson.String/Number 等自描述类型直存，动态字段无声明类型可违反
  - pack contract rows: (no surviving contract rows - evidence-absent/weak pack)
  - pack file: .paperpilot\phase2-rerun\arms\materials_complete\milvus_006.md


- 裁决: [ ] CONFIRM   [ ] RETURN   [x] REJECT   备注: 前提失真——quick-create 集合无声明字段，text_field 系动态键，数值直存属 JSON 动态字段固有语义

## milvus_012  (GT=T; verdicts: {'defect_id': 'milvus_012', 'verdict': 'HUMAN_REVIEW', 'confidence': 0.4, 'perspectives': {'A': 'NEUTRAL', 'B': 'NEUTRAL', 'C': 'WEAK_REFUTED', 'D': 'NO_SIGNAL'}, 'd_evidence': "无源码非缺陷明文注释；RESP1 显示 dbName='' 静默回落 default 库返回 code=0", 'rationale': "契约仅为描述性（'The name of an existing database.'，无 required/非空拒绝语义，M3 已核查），空字符串名回落默认库不属七类客观约束，按兜底 HUMAN_REVIEW"} / {'defect_id': 'milvus_012', 'verdict': 'HUMAN_REVIEW', 'confidence': 0.5, 'perspectives': {'A': 'NEUTRAL', 'B': 'NEUTRAL', 'C': 'WEAK_REFUTED', 'COG': 'NO_SIGNAL', 'D': 'by_design_in_source'}, 'd_evidence': 'internal/distributed/proxy/httpserver/handler_v2.go:362-365(dbName 空串→HTTPHeaderDBName→DefaultDbName 逐级兜底链,无任何注释)', 'rationale': "dbName='' 静默归一为 default 并返回成功;包内文档仅描述 'The name of an existing database.' 无非空/拒绝断言(A=NEUTRAL),空串不属七类客观约束(B=NEUTRAL);兜底链结构示设计但无注释/quote 明文(红线3 不构成 REFUTED) → 转人工。"} / {'defect_id': 'milvus_012', 'verdict': 'FALSE_POSITIVE', 'confidence': 0.7, 'perspectives': {'A': 'NEUTRAL', 'B': 'NEUTRAL', 'C': 'REFUTED', 'D': 'NO_SIGNAL'}, 'd_evidence': "internal/distributed/proxy/httpserver/handler_v2.go:362-367(v2.6.16) source:by_design_in_source — 显式三级回退 body dbName→Header DBName→DefaultDbName 常量;冻结包文档依据自述'无 required 标注,无非空/拒绝语义声明'", 'rationale': '空 dbName 显式解析为 default 库是源码中有意实现的缺省回退链,且文档侧本无任何拒绝语义承诺(断言不被违反),C=REFUTED 判 FALSE_POSITIVE'})

- judge rationale (run1): 契约仅为描述性（'The name of an existing database.'，无 required/非空拒绝语义，M3 已核查），空字符串名回落默认库不属七类客观约束，按兜底 HUMAN_REVIEW
- d_evidence: 无源码非缺陷明文注释；RESP1 显示 dbName='' 静默回落 default 库返回 code=0
  - pack contract rows: (no surviving contract rows - evidence-absent/weak pack)
  - pack file: .paperpilot\phase2-rerun\arms\materials_complete\milvus_012.md


- 裁决: [ ] CONFIRM   [ ] RETURN   [x] REJECT   备注: 空 dbName 解析为 default 属等价缺省回退；文档断言仅描述性（'an existing database'）无拒绝承诺可违反

## milvus_013  (GT=T; verdicts: {'defect_id': 'milvus_013', 'verdict': 'CONFIRMED', 'confidence': 0.75, 'perspectives': {'A': 'NEUTRAL', 'B': 'CONFIRMED', 'C': 'CONFIRMED', 'D': 'NO_SIGNAL'}, 'd_evidence': 'v2.6.16 timeout_middleware.go:183-186 strconv.ParseInt 失败被静默吞掉（仅 err==nil 才覆盖默认超时），无任何注释声明有意忽略非法头', 'rationale': "类型套套逻辑：数值语义的 Request-Timeout 头接受 'abc'/'3.5' 非数值且静默回落默认超时返回成功，B 客观约束主导判 CONFIRMED；文档对该头无类型承诺故 A=NEUTRAL 不阻碍，认知数据类型序列化盲区与 header 解析非同构记 NO_SIGNAL"} / {'defect_id': 'milvus_013', 'verdict': 'HUMAN_REVIEW', 'confidence': 0.5, 'perspectives': {'A': 'NEUTRAL', 'B': 'NEUTRAL', 'C': 'WEAK_REFUTED', 'COG': 'NO_SIGNAL', 'D': 'by_design_in_source'}, 'd_evidence': 'internal/distributed/proxy/httpserver/timeout_middleware.go:183-186(strconv.ParseInt(Request-Timeout) 失败即静默保留默认超时,无注释)', 'rationale': "Request-Timeout 系客户端提示头而非七类所涉 API 参数,畸形值('3.5'/'abc')静默忽略属宽松行为但请求仍被正常处理;包内核查证实 2.6.x 文档对该 header 无任何类型约束(A=NEUTRAL,B=NEUTRAL),无明文 by-design 证据(C=WEAK_REFUTED) → 转人工。"} / {'defect_id': 'milvus_013', 'verdict': 'HUMAN_REVIEW', 'confidence': 0.4, 'perspectives': {'A': 'NEUTRAL', 'B': 'NEUTRAL', 'C': 'WEAK_REFUTED', 'D': 'NO_SIGNAL'}, 'd_evidence': 'internal/distributed/proxy/httpserver/timeout_middleware.go:182-186(v2.6.16) source:validation_absent — strconv.ParseInt 失败被静默吞掉(if err==nil 才采用),非法 header 无提示回退默认超时,无任何意图注释', 'rationale': 'Request-Timeout 非文档化契约参数(冻结包核实文档仅列 Authorization),不落七类客观约束(B=NEUTRAL);静默吞错属无注释的裸静默行为,按红线3记 WEAK_REFUTED 转人工'})

- judge rationale (run1): 类型套套逻辑：数值语义的 Request-Timeout 头接受 'abc'/'3.5' 非数值且静默回落默认超时返回成功，B 客观约束主导判 CONFIRMED；文档对该头无类型承诺故 A=NEUTRAL 不阻碍，认知数据类型序列化盲区与 header 解析非同构记 NO_SIGNAL
- d_evidence: v2.6.16 timeout_middleware.go:183-186 strconv.ParseInt 失败被静默吞掉（仅 err==nil 才覆盖默认超时），无任何注释声明有意忽略非法头
  - pack contract rows: (no surviving contract rows - evidence-absent/weak pack)
  - pack file: .paperpilot\phase2-rerun\arms\materials_complete\milvus_013.md


- 裁决: [x] CONFIRM   [ ] RETURN   [ ] REJECT   备注: 数值语义头 Request-Timeout 接受 'abc'/'3.5' 静默回落默认超时返回成功；源码 ParseInt 失败被静默吞掉

## milvus_030  (GT=T; verdicts: {'defect_id': 'milvus_030', 'verdict': 'HUMAN_REVIEW', 'confidence': 0.5, 'perspectives': {'A': 'NEUTRAL', 'B': 'NEUTRAL', 'C': 'WEAK_REFUTED', 'D': 'validation_present'}, 'd_evidence': 'internal/proxy/util.go:1307-1313 (v2.6.17): ValidatePassword 仅校验长度 6..72,无复杂度校验亦无相关注释', 'rationale': '包内无 users+create 契约行,8 位纯小写密码通过在场长度校验、无客观约束类可触发(长度规则已被执行),源码无复杂度校验且无 by-design 明文 → C=WEAK_REFUTED,认知D=NO_SIGNAL,证据不足转人工。'} / {'defect_id': 'milvus_030', 'verdict': 'HUMAN_REVIEW', 'confidence': 0.55, 'perspectives': {'A': 'NEUTRAL', 'B': 'NEUTRAL', 'C': 'WEAK_REFUTED', 'D': 'NO_SIGNAL'}, 'd_evidence': 'v2.6.17 internal/proxy/util.go:1306-1313: ValidatePassword 仅校验长度 6-72,无复杂度校验且无明文 by-design 注释', 'rationale': '包内无 users+create 契约行(A=NEUTRAL),密码复杂度不属七类客观约束、长度校验正常工作(B=NEUTRAL),源码无校验亦无明文 by-design 按红线 3 只能记 WEAK_REFUTED,依红线 4 转人工。'} / {'defect_id': 'milvus_030', 'verdict': 'HUMAN_REVIEW', 'confidence': 0.5, 'perspectives': {'A': 'NEUTRAL', 'B': 'NEUTRAL', 'C': 'WEAK_REFUTED', 'D': 'NO_SIGNAL'}, 'd_evidence': 'internal/proxy/util.go:1305-1312 ValidatePassword 仅校验长度区间(6..72),无复杂度校验且无注释', 'rationale': '包内无 users+create 契约行(A=NEUTRAL),密码复杂度不属七类客观约束且长度下界已被强制(1字符→1100),源码长度校验在场、复杂度缺失属无注释裸静默行为,证据不足转人工。'})

- judge rationale (run1): 包内无 users+create 契约行,8 位纯小写密码通过在场长度校验、无客观约束类可触发(长度规则已被执行),源码无复杂度校验且无 by-design 明文 → C=WEAK_REFUTED,认知D=NO_SIGNAL,证据不足转人工。
- d_evidence: internal/proxy/util.go:1307-1313 (v2.6.17): ValidatePassword 仅校验长度 6..72,无复杂度校验亦无相关注释
  - pack contract rows: (no surviving contract rows - evidence-absent/weak pack)
  - pack file: .paperpilot\phase2-rerun\arms\materials_complete\milvus_030.md


- 裁决: [ ] CONFIRM   [ ] RETURN   [x] REJECT   备注: 包内无密码复杂度文档承诺——doc-impl 缺陷类无文档锚点可违反（长度下界已强制：1 字符→1100）

## milvus_031  (GT=T; verdicts: {'defect_id': 'milvus_031', 'verdict': 'HUMAN_REVIEW', 'confidence': 0.5, 'perspectives': {'A': 'NEUTRAL', 'B': 'NEUTRAL', 'C': 'WEAK_REFUTED', 'D': 'validation_present'}, 'd_evidence': "internal/distributed/proxy/httpserver/utils.go:692 (v2.6.17): 1804 报错 'has pass more field without dynamic schema' 来自 schema 外多余字段 color 的检查", 'rationale': '两次请求均被 1804 拒绝,拒绝根因是 schema 外的 color 字段而非所声称的 autoID-upsert 缺 PK 行为面(该面未被隔离观察),无违反值被接受,认知D=NO_SIGNAL,证据不足转人工。'} / {'defect_id': 'milvus_031', 'verdict': 'HUMAN_REVIEW', 'confidence': 0.5, 'perspectives': {'A': 'NEUTRAL', 'B': 'NEUTRAL', 'C': 'WEAK_REFUTED', 'D': 'NO_SIGNAL'}, 'd_evidence': 'output_milvus_031.log RESP3/RESP4: upsert 与 insert 同因额外字段 color 触发 1804 拒绝,缺 PK 现象未获干净观察', 'rationale': '包内无 entities+upsert 契约行,两次请求均被拒绝、无违反值被接受,且观察被多余字段混淆致声称的现象面未建立,证据不足依红线 4 转人工。'} / {'defect_id': 'milvus_031', 'verdict': 'HUMAN_REVIEW', 'confidence': 0.45, 'perspectives': {'A': 'NEUTRAL', 'B': 'NEUTRAL', 'C': 'NEUTRAL', 'D': 'NO_SIGNAL'}, 'd_evidence': "internal/distributed/proxy/httpserver/utils.go:692 code 1804 源自'has pass more field without dynamic schema'额外字段校验,非 autoID/PK 逻辑", 'rationale': "两次请求均被拒绝(code 1804)无'接受违反值'观察,且拒绝根因是 probe 携带 schema 外字段 color,与候选声称的 autoID 上 upsert 缺 PK 现象错位;无契约行,证据不足转人工。"})

- judge rationale (run1): 两次请求均被 1804 拒绝,拒绝根因是 schema 外的 color 字段而非所声称的 autoID-upsert 缺 PK 行为面(该面未被隔离观察),无违反值被接受,认知D=NO_SIGNAL,证据不足转人工。
- d_evidence: internal/distributed/proxy/httpserver/utils.go:692 (v2.6.17): 1804 报错 'has pass more field without dynamic schema' 来自 schema 外多余字段 color 的检查
  - pack contract rows: (no surviving contract rows - evidence-absent/weak pack)
  - pack file: .paperpilot\phase2-rerun\arms\materials_complete\milvus_031.md


- 裁决: [ ] CONFIRM   [x] RETURN   [ ] REJECT   备注: 两次请求均被 1804 拒绝且根因是探针携带 schema 外字段 color——声称的 autoID-upsert 缺 PK 面未被隔离观察，退回重跑探针

## milvus_036  (GT=T; verdicts: {'defect_id': 'milvus_036', 'verdict': 'HUMAN_REVIEW', 'confidence': 0.5, 'perspectives': {'A': 'NEUTRAL', 'B': 'NEUTRAL', 'C': 'WEAK_REFUTED', 'D': 'validation_absent'}, 'd_evidence': 'internal/distributed/proxy/httpserver/request_v2.go:487-510 + handler_v2.go:1929 (v3.0.0): SearchReqV2 无 groupParams 字段,顶层 groupSize 仅在 >0 时才转发', 'rationale': "请求将参数包在嵌套 groupParams 键下,该键不是 v3.0.0 REST v2 search 的 API 参数(结构体仅顶层 groupingField/groupSize),gin 忽略未知字段,服务器从未收到 groupSize 值,记录实为普通搜索,不能证明'API 接受 groupSize=0/-1'(B=NEUTRAL);gRPC 面报错为 metric 不匹配(internal/util/segcore/plan.go:115)与 group_size 无关;顶层 groupSize<=0 被静默丢弃且无注释 → C=WEAK_REFUTED,认知D=NO_SIGNAL,证据不足转人工。"} / {'defect_id': 'milvus_036', 'verdict': 'CONFIRMED', 'confidence': 0.85, 'perspectives': {'A': 'NEUTRAL', 'B': 'CONFIRMED', 'C': 'CONFIRMED', 'D': 'NO_SIGNAL'}, 'd_evidence': "v3.0.0 internal/proxy/search_util.go:934 'input group size:%d is negative' 与 tests/python_client/milvus_client/test_milvus_client_search_group_by.py:890 期望负值报错;output_milvus_036.log RESP5/RESP6 groupSize=0/-1 均 code=0", 'rationale': 'groupSize 属 count/size 类参数,0 与 -1 均被 REST 接受构成数值下界违反;源码明文负值非法且无 -1/-0 哨兵注释(非 ef/nprobe 先例),B=CONFIRMED 且包内无 groupSize 域契约行(A=NEUTRAL)终判 CONFIRMED。'} / {'defect_id': 'milvus_036', 'verdict': 'CONFIRMED', 'confidence': 0.75, 'perspectives': {'A': 'NEUTRAL', 'B': 'CONFIRMED', 'C': 'WEAK_REFUTED', 'D': 'SUPPORTS_DEFECT'}, 'd_evidence': 'internal/proxy/search_util.go:932-935 proxy 对 group_size<=0 明文拒绝;handler_v2.go:1929 REST 仅在 GroupSize>0 时透传,0/-1 静默丢弃', 'rationale': "数值下界+接口不对称:count 类参数 groupSize 接受 0/-1 返回成功(静默丢弃后按无分组执行),而 proxy 面对同一违反值明文拒绝'input group size is negative';认知材料 blindspot'REST v2 and gRPC divergent validation'现象级命中(维护者将跨通道不一致视为缺陷并修复)。"})

- judge rationale (run1): 请求将参数包在嵌套 groupParams 键下,该键不是 v3.0.0 REST v2 search 的 API 参数(结构体仅顶层 groupingField/groupSize),gin 忽略未知字段,服务器从未收到 groupSize 值,记录实为普通搜索,不能证明'API 接受 groupSize=0/-1'(B=NEUTRAL);gRPC 面报错为 metric 不匹配(internal/util/segcore/plan.go:115)与 group_size 无关;顶层 groupSize<=0 被静默丢弃且无注释 → C=WEAK_REFUTED,认知D=NO_SIGNAL,证据不足转人工。
- d_evidence: internal/distributed/proxy/httpserver/request_v2.go:487-510 + handler_v2.go:1929 (v3.0.0): SearchReqV2 无 groupParams 字段,顶层 groupSize 仅在 >0 时才转发
  - pack contract rows: collection MUST be loaded before search | collection.load_state == 'loaded' before search
  - pack file: .paperpilot\phase2-rerun\arms\materials_complete\milvus_036.md


- 裁决: [x] CONFIRM   [ ] RETURN   [ ] REJECT   备注: groupSize=0/-1 REST 接受 code=0（log 在案）vs proxy 面同值明文拒绝+官方测试期望报错——接口不对称

## milvus_038  (GT=T; verdicts: {'defect_id': 'milvus_038', 'verdict': 'HUMAN_REVIEW', 'confidence': 0.5, 'perspectives': {'A': 'NEUTRAL', 'B': 'NEUTRAL', 'C': 'WEAK_REFUTED', 'D': 'validation_present'}, 'd_evidence': 'internal/distributed/proxy/httpserver/request_v2.go:499 + internal/proxy/task_query.go:126-137 (v3.0.0): groupingField 为顶层键,且 validateGroupByFieldSchema 会拒绝不支持分组的字段类型', 'rationale': "请求的 groupParams.groupByField 嵌套键从未绑定(该版本参数为顶层 groupingField),记录实为普通搜索,不能证明'API 接受向量字段分组'(B=NEUTRAL);服务端存在 validateGroupByFieldSchema 校验(D=validation_present),gRPC 面报错为 metric 不匹配而非 group-by 拒绝;认知D=NO_SIGNAL,所声称行为面无记录支撑 → C=WEAK_REFUTED 转人工。"} / {'defect_id': 'milvus_038', 'verdict': 'FALSE_POSITIVE', 'confidence': 0.7, 'perspectives': {'A': 'REFUTED', 'B': 'NEUTRAL', 'C': 'WEAK_REFUTED', 'D': 'NO_SIGNAL'}, 'd_evidence': "milvus_038.md 契约行明示 'no normative statement about vector-field values being rejected';log 摘要 c1_grpc 仅因 metricType 不匹配报错,与 group_by 无关", 'rationale': "包内契约行明示文档无'向量字段须被拒绝'的规范陈述,断言不被观察违反(A=REFUTED),groupByField 为字段名开放引用不属七类客观约束,gRPC 对照因 harness metricType 误配失效无有效不对称证据,依聚合规则判 FALSE_POSITIVE。"} / {'defect_id': 'milvus_038', 'verdict': 'CONFIRMED', 'confidence': 0.6, 'perspectives': {'A': 'NEUTRAL', 'B': 'CONFIRMED', 'C': 'WEAK_REFUTED', 'D': 'NO_SIGNAL'}, 'd_evidence': 'internal/proxy/task_search.go:1171 binary vector group-by 显式拒绝;internal/proxy/search_pipeline.go:2331-2336 isSameGroupByValue 对 FloatVector 等类型恒 false→分组静默退化为普通 top-k', 'rationale': '同族不一致:同端点 group-by 违反值一族(binary vector)显式报错拒绝,另一族(float vector)静默接受且分组语义失效仍返回成功(结果与无分组一致);gRPC 对比腿被 metric 配置噪声污染不作依据,认知 by_design 四条均与该现象不同构(NO_SIGNAL)。'})

- judge rationale (run1): 请求的 groupParams.groupByField 嵌套键从未绑定(该版本参数为顶层 groupingField),记录实为普通搜索,不能证明'API 接受向量字段分组'(B=NEUTRAL);服务端存在 validateGroupByFieldSchema 校验(D=validation_present),gRPC 面报错为 metric 不匹配而非 group-by 拒绝;认知D=NO_SIGNAL,所声称行为面无记录支撑 → C=WEAK_REFUTED 转人工。
- d_evidence: internal/distributed/proxy/httpserver/request_v2.go:499 + internal/proxy/task_query.go:126-137 (v3.0.0): groupingField 为顶层键,且 validateGroupByFieldSchema 会拒绝不支持分组的字段类型
  - pack contract rows: documentation presents group_by_field as grouping search results over a scalar field's values (examples: docId, category); no normative statement about vector-field values being rejected
  - pack file: .paperpilot\phase2-rerun\arms\materials_complete\milvus_038.md


- 裁决: [x] CONFIRM   [ ] RETURN   [ ] REJECT   备注: 同族不一致——binary vector group-by 显式拒绝 vs float vector 静默退化普通 top-k（isSameGroupByValue 恒 false）；gRPC 对照腿被 metric 噪声污染不计

## milvus_043  (GT=T; verdicts: {'defect_id': 'milvus_043', 'verdict': 'CONFIRMED', 'confidence': 0.6, 'perspectives': {'A': 'NEUTRAL', 'B': 'NEUTRAL', 'C': 'CONFIRMED', 'D': 'validation_present'}, 'd_evidence': 'internal/core/src/exec/operator/search-groupby/SearchGroupByOperator.h:370-388 Segcore严格模式组容量/组大小强制逻辑在场(IsGroupResEnough/Push按group_size封顶),但端到端观察违反之;internal/proxy/task_search.go:1026-1040 亦有strict_group_size意图注释', 'rationale': "包内契约仅为load-state/空集断言,不覆盖strictGroupSize行为面故A=NEUTRAL;请求参数值全合法、REST与gRPC双面一致复现(各3/组),不属七类客观约束故B=NEUTRAL;观察(groupSize=2,strictGroupSize=true仍返回3/组)构成链上实质违反,源码strict逻辑在场但端到端未生效(说明非有意设计),milvus认知blindspot'文档声称X服务端非X即一致性缺陷,维护者会修'现象级命中SUPPORTS_DEFECT→CONFIRMED"} / {'defect_id': 'milvus_043', 'verdict': 'HUMAN_REVIEW', 'confidence': 0.6, 'perspectives': {'A': 'NEUTRAL', 'B': 'NEUTRAL', 'C': 'CONFIRMED', 'D': 'NO_SIGNAL'}, 'd_evidence': 'milvus v3.0.0 clone: strictGroupSize 处理未定位(内部/parser/parse_search.go 不存在)——认知材料四条 by_design_patterns(rename幂等/rowCount滞后/quick-create加载态/shardsNum)均与 group-size 严格语义不同构,无 developer_quote 命中', 'source': {'status': 'not_found', 'evidence': 'strictGroupSize/strict_group_size 未在 v3.0.0 clone 限定探查内定位到 file:line'}, 'rationale': '包内契约仅覆盖 load-state/空集合断言,不覆盖 strictGroupSize 行为面(A=NEUTRAL);strictGroupSize=true+groupSize=2 每组返回 3 条不属七类客观约束(B=NEUTRAL,REST与gRPC均接受无不对称);行为不优雅但 A=NEUTRAL+B=NEUTRAL+D=NO_SIGNAL,按保守规则转人工。'} / {'defect_id': 'milvus_043', 'verdict': 'CONFIRMED', 'confidence': 0.55, 'perspectives': {'A': 'NEUTRAL', 'B': 'NEUTRAL', 'C': 'CONFIRMED', 'D': 'SUPPORTS_DEFECT'}, 'd_evidence': 'handler_v2.go:1931 REST v2 传入 strict_group_size；search_util.go:944-954 解析入分组管线；test_milvus_client_search_order.py:651 断言严格模式每组恰好 group_size，源码无放宽意图注释', 'rationale': '包内契约无 strictGroupSize 断言故 A=NEUTRAL，分组语义不属七客观类且 REST/gRPC 两面一致故 B=NEUTRAL，但链上有实质违反观察(strictGroupSize=true,groupSize=2 仍每群 3 条、共 15 条)，且维护者认知 doc-behavior 一致性盲区现象级命中(明示严格行为未兑现=缺陷方向)，按 A=NEUTRAL+D=SUPPORTS_DEFECT 判 CONFIRMED'})

- judge rationale (run1): 包内契约仅为load-state/空集断言,不覆盖strictGroupSize行为面故A=NEUTRAL;请求参数值全合法、REST与gRPC双面一致复现(各3/组),不属七类客观约束故B=NEUTRAL;观察(groupSize=2,strictGroupSize=true仍返回3/组)构成链上实质违反,源码strict逻辑在场但端到端未生效(说明非有意设计),milvus认知blindspot'文档声称X服务端非X即一致性缺陷,维护者会修'现象级命中SUPPORTS_DEFECT→CONFIRMED
- d_evidence: internal/core/src/exec/operator/search-groupby/SearchGroupByOperator.h:370-388 Segcore严格模式组容量/组大小强制逻辑在场(IsGroupResEnough/Push按group_size封顶),但端到端观察违反之;internal/proxy/task_search.go:1026-1040 亦有strict_g
  - pack contract rows: collection MUST be loaded before search | collection.load_state == 'loaded' before search
  - pack file: .paperpilot\phase2-rerun\arms\materials_complete\milvus_043.md


- 裁决: [x] CONFIRM   [ ] RETURN   [ ] REJECT   备注: strictGroupSize=true+groupSize=2 每组仍返回 3 条（REST/gRPC 双面复现）；源码 strict 逻辑在场但端到端未生效

## qdrant_014  (GT=T; verdicts: {'defect_id': 'qdrant_014', 'verdict': 'HUMAN_REVIEW', 'confidence': 0.6, 'perspectives': {'A': 'NEUTRAL', 'B': 'NEUTRAL', 'C': 'CONFIRMED', 'D': 'validation_present'}, 'd_evidence': 'lib/storage/src/content_manager/toc/mod.rs:562/777 与 src/actix/api/cluster_api.rs:125/146 主动构造 StorageError::service_error("Qdrant is running in standalone mode")，经 ServiceError→500 映射', 'rationale': '包内契约明确无 cluster/recover 行为约束条目故 A=NEUTRAL；standalone 前提属服务端状态而非请求侧参数校验且文档无错误形态承诺，不落入七类客观约束故 B=NEUTRAL；认知无现象级命中(NO_SIGNAL)；但把可预期的模式前提报成 500 Service internal error 不优雅且无明文 by-design 证据，按保守规则转人工。'} / {'defect_id': 'qdrant_014', 'verdict': 'HUMAN_REVIEW', 'confidence': 0.5, 'perspectives': {'A': 'NEUTRAL', 'B': 'NEUTRAL', 'C': 'WEAK_REFUTED', 'D': 'NO_SIGNAL'}, 'd_evidence': 'src/actix/api/cluster_api.rs:69-72 recover→toc.request_snapshot; lib/storage/src/content_manager/toc/mod.rs:777 service_error("Qdrant is running in standalone mode")→500; 同文件 remove_peer(cluster_api.rs:76-79)对同类 standalone 前置用 bad_request(400),无任何注释表明 500 有意', 'source': {'status': 'validation_absent', 'evidence': 'standalone 场景无 4xx 前置校验,直接 service_error 冒泡为 500;同族端点 remove_peer 却用 bad_request(400),代码内无意图注释'}, 'rationale': '包内对 /cluster/recover 无行为约束行(A 躺平),standalone→500 不属七类客观约束(非参数校验且实测为 500 非 2xx 业务码,B=NEUTRAL),源码无明文 by-design 注释(C=WEAK_REFUTED),认知无命中——按 v3 灰区保守转人工;可疑点:同文件 400 先例暗示 500 属不一致。'} / {'defect_id': 'qdrant_014', 'verdict': 'FALSE_POSITIVE', 'confidence': 0.7, 'perspectives': {'A': 'NEUTRAL', 'B': 'NEUTRAL', 'C': 'NEUTRAL', 'D': 'by_design_in_source'}, 'd_evidence': "lib/storage/src/content_manager/toc/mod.rs:777 (v1.18.2) — get_consensus_proposal_sender 显式守卫:非集群模式直接抛出 'Qdrant is running in standalone mode' 服务错误", 'rationale': '契约页对 /cluster/recover 无 standalone 前提或错误形态声明故 A=NEUTRAL;实测为真 500 而非 2xx+业务错误码,不触发 HTTP 语义类;源码以专设守卫显式拒绝 standalone 模式(结构明示有意),D=SUPPORTS_NOT_DEFECT → FALSE_POSITIVE'})

- judge rationale (run1): 包内契约明确无 cluster/recover 行为约束条目故 A=NEUTRAL；standalone 前提属服务端状态而非请求侧参数校验且文档无错误形态承诺，不落入七类客观约束故 B=NEUTRAL；认知无现象级命中(NO_SIGNAL)；但把可预期的模式前提报成 500 Service internal error 不优雅且无明文 by-design 证据，按保守规则转人工。
- d_evidence: lib/storage/src/content_manager/toc/mod.rs:562/777 与 src/actix/api/cluster_api.rs:125/146 主动构造 StorageError::service_error("Qdrant is running in standalone mode")，经 ServiceError→500 映射
  - pack contract rows: (no surviving contract rows - evidence-absent/weak pack)
  - pack file: .paperpilot\phase2-rerun\arms\materials_complete\qdrant_014.md


- 裁决: [x] CONFIRM   [ ] RETURN   [ ] REJECT   备注: standalone 前提 /cluster/recover 报 500 Service error vs 同文件 remove_peer 同前提 400——同族错误码不一致且无明文意图注释

## qdrant_015  (GT=T; verdicts: {'defect_id': 'qdrant_015', 'verdict': 'HUMAN_REVIEW', 'confidence': 0.6, 'perspectives': {'A': 'NEUTRAL', 'B': 'NEUTRAL', 'C': 'CONFIRMED', 'D': 'validation_absent'}, 'd_evidence': 'lib/segment/src/data_types/collection_defaults.rs:32-41 get_shard_number 将 shard_number 直接透传，无上界/liveness 校验', 'rationale': 'shard_number=2147483647 满足契约 shard_number>=1 且挂起行为无断言覆盖故 A=NEUTRAL；该极端大值非负/零、非枚举/互斥/类型违反，不属七类客观约束故 B=NEUTRAL；但两轮 INT_MAX create 后服务均不可用（REQ2-5、REQ7-10 全超时）且无任何拒绝或上界，行为不优雅，认知无匹配，按保守规则转人工。'} / {'defect_id': 'qdrant_015', 'verdict': 'HUMAN_REVIEW', 'confidence': 0.5, 'perspectives': {'A': 'NEUTRAL', 'B': 'NEUTRAL', 'C': 'WEAK_REFUTED', 'D': 'NO_SIGNAL'}, 'd_evidence': 'lib/storage/src/content_manager/collection_meta_ops.rs:126 shard_number: Option<u32> 无上限校验; lib/storage/src/content_manager/shard_distribution.rs:91 (0..shard_number.get()) 逐 shard 分配; 包内摘要声称 control(replication_factor=0)→422 但日志 RESP5/RESP10 均 status=None,记录内部不自洽', 'source': {'status': 'validation_absent', 'evidence': 'shard_number 仅 NonZeroU32 下界(shard_distribution.rs:77),无上限/资源护栏,创建 2^31 shard 的 distribution 循环无任何明文 by-design 注释'}, 'rationale': 'INT_MAX 满足 shard_number>=1 不构成契约违反且无 200 响应故原子性断言未触发(A=NEUTRAL);请求挂起不属七类客观约束、无违反值被接受的记录(B=NEUTRAL);源码无上限校验亦无明文 by-design(C=WEAK_REFUTED);且摘要 422 控制组声明无日志支撑——按 v3 红线4 转人工。'} / {'defect_id': 'qdrant_015', 'verdict': 'FALSE_POSITIVE', 'confidence': 0.7, 'perspectives': {'A': 'NEUTRAL', 'B': 'REFUTED', 'C': 'NEUTRAL', 'D': 'validation_present'}, 'd_evidence': 'lib/collection/src/config.rs:97 (v1.18.2) — pub shard_number: NonZeroU32,serde 层强制 >=1,与包内 range 断言一致', 'rationale': '包内仅承诺 shard_number>=1,2147483647 不违反任何断言;观察摘要声称 control(replication_factor=0)返回 422 但日志 RESP5 status=None,声称无日志支撑,B=REFUTED;承诺的下界校验在场且与观察一致 → FALSE_POSITIVE'})

- judge rationale (run1): shard_number=2147483647 满足契约 shard_number>=1 且挂起行为无断言覆盖故 A=NEUTRAL；该极端大值非负/零、非枚举/互斥/类型违反，不属七类客观约束故 B=NEUTRAL；但两轮 INT_MAX create 后服务均不可用（REQ2-5、REQ7-10 全超时）且无任何拒绝或上界，行为不优雅，认知无匹配，按保守规则转人工。
- d_evidence: lib/segment/src/data_types/collection_defaults.rs:32-41 get_shard_number 将 shard_number 直接透传，无上界/liveness 校验
  - pack contract rows: collection_name type is string | At least one update field must be provided.
  - pack file: .paperpilot\phase2-rerun\arms\materials_complete\qdrant_015.md


- 裁决: [x] CONFIRM   [ ] RETURN   [ ] REJECT   备注: shard_number=INT_MAX 创建后两轮服务全超时不可用；源码仅 NonZeroU32 下界无上界护栏（控制组 422 声称无日志支撑，不计）

## qdrant_016  (GT=T; verdicts: {'defect_id': 'qdrant_016', 'verdict': 'HUMAN_REVIEW', 'confidence': 0.6, 'perspectives': {'A': 'NEUTRAL', 'B': 'NEUTRAL', 'C': 'CONFIRMED', 'D': 'validation_absent'}, 'd_evidence': 'lib/collection/src/collection/query.rs:479-480 仅对被引用 point id 校验解析（PointNotFound），对 lookup_from.collection 本身无存在性校验，不存在时被静默忽略', 'rationale': '包内契约对 lookup_from 仅声明语义与同维建议、无存在性约束故 A=NEUTRAL；不存在的集合引用属嵌套可选字段且包内记录无被拒族对照，不属七类客观约束故 B=NEUTRAL；认知无现象级命中(NO_SIGNAL)；但指向不存在集合被静默忽略并以 200 返回当前集合结果不优雅、无明文 by-design，按保守规则转人工。'} / {'defect_id': 'qdrant_016', 'verdict': 'CONFIRMED', 'confidence': 0.7, 'perspectives': {'A': 'NEUTRAL', 'B': 'CONFIRMED', 'C': 'CONFIRMED', 'D': 'SUPPORTS_DEFECT'}, 'd_evidence': 'lib/collection/src/common/fetch_vectors.rs:250-264 ID 引用路径对不存在 lookup 集合显式 Err(CollectionError::not_found); 而 raw-vector 路径(lib/collection/src/operations/universal_query/collection_query.rs ids_into_vectors 的 Nearest(Vector) 分支,fetch_vectors.rs:206-208)不触及 lookup_from 直接返回原向量; 认知 blindspot"Silent failure in recommend API with missing point IDs"现象级同构(缺失引用静默失败)', 'source': {'status': 'validation_absent', 'evidence': '不存在的 lookup_from.collection 仅在 ID 引用查询路径报 not_found;raw-vector 查询路径完全绕过该集合的存在性校验,静默回退当前集合'}, 'rationale': '同端点同违反值(不存在的 lookup_from.collection)一族被 404 拒绝、raw-vector 族静默 200 并回退当前集合结果(同族不一致,B=CONFIRMED,RESP7=200+3 结果与 RESP8 正常路径完全一致证实回退);认知盲区命中(D=SUPPORTS_DEFECT);链上有实质违反观察;行为不优雅无明文 by-design。'} / {'defect_id': 'qdrant_016', 'verdict': 'CONFIRMED', 'confidence': 0.6, 'perspectives': {'A': 'NEUTRAL', 'B': 'NEUTRAL', 'C': 'NEUTRAL', 'D': 'validation_absent'}, 'd_evidence': 'lib/collection/src/collection/query.rs:476-483 (v1.18.2) — 仅对 get_referenced_point_ids() 校验 PointNotFound,lookup_from 集合名无任何存在性校验,raw-vector 查询下不存在的 lookup 集合被静默忽略', 'rationale': "契约明示 lookup_from 无存在性约束条目故 A=NEUTRAL;不属七类客观约束且 200 为正常形态故 B=NEUTRAL;但链上有实质违反观察(引用 nonexistent_collection_xyz 仍 200 返 3 结果),D=validation_absent(文档 'location used to lookup vectors' 隐含集合应存在,实现静默回退)→ 按 v3 D=SUPPORTS_DEFECT 分支 CONFIRMED"})

- judge rationale (run1): 包内契约对 lookup_from 仅声明语义与同维建议、无存在性约束故 A=NEUTRAL；不存在的集合引用属嵌套可选字段且包内记录无被拒族对照，不属七类客观约束故 B=NEUTRAL；认知无现象级命中(NO_SIGNAL)；但指向不存在集合被静默忽略并以 200 返回当前集合结果不优雅、无明文 by-design，按保守规则转人工。
- d_evidence: lib/collection/src/collection/query.rs:479-480 仅对被引用 point id 校验解析（PointNotFound），对 lookup_from.collection 本身无存在性校验，不存在时被静默忽略
  - pack contract rows: (no surviving contract rows - evidence-absent/weak pack)
  - pack file: .paperpilot\phase2-rerun\arms\materials_complete\qdrant_016.md


- 裁决: [x] CONFIRM   [ ] RETURN   [ ] REJECT   备注: 不存在的 lookup 集合：ID 引用路径 404 vs raw-vector 路径静默 200 回退当前集合——同族不一致+认知盲区现象级命中

## qdrant_026  (GT=T; verdicts: {'defect_id': 'qdrant_026', 'verdict': 'HUMAN_REVIEW', 'confidence': 0.55, 'perspectives': {'A': 'NEUTRAL', 'B': 'NEUTRAL', 'C': 'CONFIRMED', 'D': 'validation_absent'}, 'd_evidence': 'lib/collection/src/grouping/group_by.rs:274-275 仅按 query_result_order/score_ordering 排序，等分（全部 score=1.0）无稳定 tie-break 机制或注释', 'rationale': '包内仅 group_size/limit>=1 断言且请求满足、无确定性断言故 A=NEUTRAL；10 次同请求 tie 次序漂移不涉及任何违反值被接受/拒绝，不属七类客观约束故 B=NEUTRAL；认知 by-design 命中的是 HNSW 分页重复现象、与本 tie 次序现象不同构(NO_SIGNAL)；同请求结果不可复现不优雅且无明文 by-design，按保守规则转人工。'} / {'defect_id': 'qdrant_026', 'verdict': 'HUMAN_REVIEW', 'confidence': 0.5, 'perspectives': {'A': 'NEUTRAL', 'B': 'NEUTRAL', 'C': 'WEAK_REFUTED', 'D': 'NO_SIGNAL'}, 'd_evidence': '8 点向量全同、得分全部 1.0 并列,10 次同请求产生 10 种组内/组间次序(成员集恒定 {a:1,3,5}/{b:2,4,6}); 包内契约行仅 group_size>=1 且 limit>=1(均满足); v1.19.0 clone 内 group 查询路径未定位到 tie-order 明文 by-design 注释', 'source': {'status': 'not_found', 'evidence': '并列得分 tie-breaking 的次序稳定性在源码中无明文设计声明可定位'}, 'rationale': '并列得分下的次序不稳定不属七类客观约束——参数全部合法、无违反值被接受(B=NEUTRAL);契约行不覆盖次序确定性行为面(A=NEUTRAL);认知 HNSW-by-design 模式与本案(全量 brute-force、全同向量并列)不同构无命中(D=NO_SIGNAL);无明文 by-design 注释,按 v3 灰区转人工。'} / {'defect_id': 'qdrant_026', 'verdict': 'HUMAN_REVIEW', 'confidence': 0.5, 'perspectives': {'A': 'NEUTRAL', 'B': 'NEUTRAL', 'C': 'NEUTRAL', 'D': 'not_found'}, 'd_evidence': 'lib/collection/src/grouping/group_by.rs:331,417 (v1.19.0) — AHashMap 无序迭代为组内/组间平局顺序非确定性的来源;包内无任何确定性排序断言可对应校验', 'rationale': '10 次同请求成员集合恒为 {1,3,5}/{2,4,6} 仅全平局(score 均 1.0)下的顺序与组序漂移,包内契约仅含 group_size/limit 下界且均满足,A=NEUTRAL;不属七类客观约束(无越界值/无形状违诺),B=NEUTRAL;无确定性承诺可校验,D=not_found;C 无命中 → A=NEUTRAL+B=NEUTRAL+D=NO_SIGNAL+C 无信号按保守分支转 HUMAN_REVIEW(禁止静默过滤)'})

- judge rationale (run1): 包内仅 group_size/limit>=1 断言且请求满足、无确定性断言故 A=NEUTRAL；10 次同请求 tie 次序漂移不涉及任何违反值被接受/拒绝，不属七类客观约束故 B=NEUTRAL；认知 by-design 命中的是 HNSW 分页重复现象、与本 tie 次序现象不同构(NO_SIGNAL)；同请求结果不可复现不优雅且无明文 by-design，按保守规则转人工。
- d_evidence: lib/collection/src/grouping/group_by.rs:274-275 仅按 query_result_order/score_ordering 排序，等分（全部 score=1.0）无稳定 tie-break 机制或注释
  - pack contract rows: group_size >= 1 AND limit >= 1 | group_size >= 1 AND limit >= 1
  - pack file: .paperpilot\phase2-rerun\arms\materials_complete\qdrant_026.md


- 裁决: [ ] CONFIRM   [ ] RETURN   [x] REJECT   备注: 并列得分（全 1.0）次序漂移无文档确定性承诺——未承诺行为不构成 doc-impl 缺陷；HNSW 认知模式与全量扫描并列不同构

## qdrant_027  (GT=T; verdicts: {'defect_id': 'qdrant_027', 'verdict': 'CONFIRMED', 'confidence': 0.7, 'perspectives': {'A': 'NEUTRAL', 'B': 'CONFIRMED', 'C': 'CONFIRMED', 'D': 'validation_present'}, 'd_evidence': 'lib/segment/src/types.rs:2740-2743 PayloadFieldSchema 为 untagged {FieldType(PayloadSchemaType)|FieldParams(PayloadSchemaParams)} 闭集；src/common/update.rs:309 field_schema: Option<PayloadFieldSchema>（PUT index 路由 src/actix/api/update_api.rs:371）', 'rationale': '包内仅有异步索引断言、ack 后紧接的 GET payload_schema={} 不能证明违反异步语义，且无 field_schema 形式断言故 A=NEUTRAL；field_schema 值域为 snake_case 字符串或 params 对象的闭集，实测数组形式 ["keyword"] 被 200 acknowledged 接受且索引未落 payload_schema，构成枚举闭集违反故 B=CONFIRMED；源码类型声明与观测相悖，但按红线不以"实现如此"翻案仅记录怀疑；认知无匹配(NO_SIGNAL)；按聚合规则 A=NEUTRAL 且 B=CONFIRMED，判 CONFIRMED。'} / {'defect_id': 'qdrant_027', 'verdict': 'FALSE_POSITIVE', 'confidence': 0.6, 'perspectives': {'A': 'REFUTED', 'B': 'NEUTRAL', 'C': 'NEUTRAL', 'D': 'NO_SIGNAL'}, 'd_evidence': '包内断言"Index creation is asynchronous"直接覆盖 GET 时 payload_schema={} 行为面(GET 中 update_queue length=1 显示操作在队列未完成); v1.19.0 源码 lib/segment/src/types.rs:2738-2743 PayloadFieldSchema 为 untagged(字符串枚举|参数对象),数组应被反序列化拒绝,与记录 200 矛盾(疑探针渲染伪影)', 'source': {'status': 'validation_present', 'evidence': 'types.rs:2738-2743 严格 untagged 反序列化在位——真实数组载荷应 4xx 被拒;src/common/update.rs:945-948 缺失 field_schema 亦显式 bad_request'}, 'rationale': "'索引未建/静默忽略'主张被包内 async 断言覆盖——单次立即 GET 的空 payload_schema 且 update_queue=1 不构成未创建证据(A=REFUTED);记录载荷与源码反序列化物理矛盾且无违反值确凿被接受(B=NEUTRAL);无契约违反面,按保守规则判 FP 并留痕源码怀疑点。"} / {'defect_id': 'qdrant_027', 'verdict': 'HUMAN_REVIEW', 'confidence': 0.5, 'perspectives': {'A': 'NEUTRAL', 'B': 'NEUTRAL', 'C': 'NEUTRAL', 'D': 'not_found'}, 'd_evidence': 'src/common/update.rs:305-309 + lib/segment/src/types.rs:2738-2743 (v1.19.0) — CreateFieldIndex.field_schema 为 untagged 枚举 PayloadFieldSchema{FieldType(字符串枚举)|FieldParams(参数结构体)},数组形式应反序列化失败返回 400,与实测 200 acknowledged 矛盾,无法在 v1.19.0 源码中调和(疑记录版本不匹配),如实记 not_found', 'rationale': "field_schema=['keyword'] 实测 200 acknowledged 且随后 GET payload_schema 仍为空,但源码预期该入参应 400 且 GET 仅一次无法区分异步未落盘与静默失败;A=NEUTRAL(包内仅 async 断言)、B=NEUTRAL(pack 内无 field_schema 值域断言)、C 无命中、D 与观察冲突不可调和 → 保守转 HUMAN_REVIEW(源码-观察矛盾记录在案,禁静默过滤)"})

- judge rationale (run1): 包内仅有异步索引断言、ack 后紧接的 GET payload_schema={} 不能证明违反异步语义，且无 field_schema 形式断言故 A=NEUTRAL；field_schema 值域为 snake_case 字符串或 params 对象的闭集，实测数组形式 ["keyword"] 被 200 acknowledged 接受且索引未落 payload_schema，构成枚举闭集违反故 B=CONFIRMED；源码类型声明与观测相悖，但按红线不以"实现如此"翻案仅记录怀疑；认知无匹配(NO_SIGNAL)；按聚合规则 A=NEUTRAL 且 B=CONFIRMED，判 CONFIRMED。
- d_evidence: lib/segment/src/types.rs:2740-2743 PayloadFieldSchema 为 untagged {FieldType(PayloadSchemaType)|FieldParams(PayloadSchemaParams)} 闭集；src/common/update.rs:309 field_schema: Option<PayloadFieldSchema>（PU
  - pack contract rows: Index creation is asynchronous; query optimization applies after the index is built.
  - pack file: .paperpilot\phase2-rerun\arms\materials_complete\qdrant_027.md


- 裁决: [x] CONFIRM   [ ] RETURN   [ ] REJECT   备注: field_schema 数组形式（值域闭集外）实测 200 acknowledged 接受且索引未落——枚举闭集违反被接受在案

## weaviate_007  (GT=T; verdicts: {'defect_id': 'weaviate_007', 'verdict': 'FALSE_POSITIVE', 'confidence': 0.6, 'perspectives': {'A': 'NEUTRAL', 'B': 'NEUTRAL', 'C': 'REFUTED', 'D': 'by_design_in_source'}, 'd_evidence': "entities/vectorindex/hnsw/config.go:25,96 (v1.38.0) 注释 'Set these defaults if the user leaves them blank' + SetDefaults 将空 Distance 落默认 cosine", 'rationale': 'distance=null 按 JSON 惯例等价字段缺省并落默认 cosine，不属七类客观违反(B=NEUTRAL，包内亦无 distance 契约断言)，源码注释明文空白值落默认构成红线3意图证据(C=REFUTED 满足明文标准)→FALSE_POSITIVE'} / {'defect_id': 'weaviate_007', 'verdict': 'HUMAN_REVIEW', 'confidence': 0.55, 'perspectives': {'A': 'NEUTRAL', 'B': 'NEUTRAL', 'C': 'WEAK_REFUTED', 'D': 'NO_SIGNAL'}, 'd_evidence': "v1.37.4 entities/vectorindex/common/config.go:103-106 OptionalStringFromMap 对非 string 值静默跳过(无注释);v1.38.0 hnsw/config.go:25/96 默认 distance=cosine('Set these defaults if the user leaves them blank' 仅覆盖缺省不覆盖 null);cognition 'Type coercion issues' 限定 RAFT 通信不构成现象级命中", 'rationale': '断言未覆盖 distance,null 在该 API 惯例中≈未设置(如 stopwords.additions:null)故不落入七类客观约束,认知无命中且无针对 mistyped/null 输入的明文 by-design 证据 → 按保守规则转人工。'} / {'defect_id': 'weaviate_007', 'verdict': 'HUMAN_REVIEW', 'confidence': 0.5, 'perspectives': {'A': 'NEUTRAL', 'B': 'NEUTRAL', 'C': 'WEAK_REFUTED', 'D': 'NO_SIGNAL'}, 'd_evidence': 'v1.38.0 entities/vectorindex/hnsw/config.go:213-216 OptionalStringFromMap 跳过 null 后走默认 cosine(entities/vectorindex/common DefaultDistanceMetric=DistanceCosine)，null 处理无任何意图注释', 'rationale': 'JSON null 对可选字段等价未提供而非集合外实值，不落入枚举闭集/类型套套逻辑等七类(B=NEUTRAL：null 非越界取值而是缺席语义)，无契约断言覆盖 distance(A=NEUTRAL)，认知无现象级命中(D=NO_SIGNAL)，C 优雅默认但无源码明文记 WEAK_REFUTED，按聚合表保守转 HUMAN_REVIEW。'})

- judge rationale (run1): distance=null 按 JSON 惯例等价字段缺省并落默认 cosine，不属七类客观违反(B=NEUTRAL，包内亦无 distance 契约断言)，源码注释明文空白值落默认构成红线3意图证据(C=REFUTED 满足明文标准)→FALSE_POSITIVE
- d_evidence: entities/vectorindex/hnsw/config.go:25,96 (v1.38.0) 注释 'Set these defaults if the user leaves them blank' + SetDefaults 将空 Distance 落默认 cosine
  - pack contract rows: properties.class matches /^[A-Z][a-zA-Z0-9]*$/ | properties.vectorIndexType in {hnsw, flat, dynamic, bwes}
  - pack file: .paperpilot\phase2-rerun\arms\materials_complete\weaviate_007.md


- 裁决: [ ] CONFIRM   [ ] RETURN   [x] REJECT   备注: 源码明文注释空白值落默认 cosine——满足红线 3 明文 by-design 标准

---

## 认知锚定重判新增 routed 案裁决（2026-09-13，pack 材料口径，同 17 案先例）

背景：认知锚定清理版重判（7 案）后，milvus_019/021 成为新 routed 确认（原判为 FP×3，无 HR 组件，不在原 17 案工作表内）。作者按 pack 材料口径裁决：

### milvus_019 — REJECTED（missing documentation anchor）
- observed：insert 5 行 ack → load 成功 → get_stats rowCount=0 → 同刻 query 返回 5 行。行为矛盾真实。
- pack 契约依据：无（"无 endpoint=collections+get_stats 的可核查约束行"）——文档未承诺 rowCount 统计口径。
- 理由：矛盾可由统计口径差异（growing vs flushed）并存解释，缺文档锚不构成"违反文档"。落入先例 rejected 的 missing-documentation-anchor 类。

### milvus_021 — REJECTED（missing documentation anchor；两取证方向同归）
- observed：create → insert → 不 load 直接 search → 200 返回数据。
- pack 契约依据：无（"无 endpoint=entities+search 的可核查约束行"）。
- 理由：若 create 末尾自动 LoadCollection（重判 run2 取证 handler_v2.go:2109-2118）则 never-loaded 前提不成立；若 search 全路径确无 load 校验（重判 run1 取证）则行为真实但缺"须 load 方可 search"文档锚。两方向均不支撑缺陷。

### 对 joint 读数的影响
joint TP = 27 (forced) + 9 (原 upheld；004/006 本就不在 upheld 名单) + 0 (新 2 案均拒) = **31**；joint recall = 31/51 = **0.608**。suppression/precision 由终算脚本输出。

---

## flat 臂对称裁决（2026-09-13，同 pack 材料口径；应对 R2 W3/R3 3.4 的 equal-treatment 关切）

flat 臂 routed confirmations 共 11 案。沿用既往结论 8 案（milvus_001=RETURN、milvus_036/038/043+qdrant_014=CONFIRM、milvus_019/027=REJECT），milvus_020 属 FP 侧已裁。新裁 3 案：

### milvus_010 — REJECT（missing documentation anchor）
- observed：create 负 TTL code=0；control alter_properties 同参数 code=1100 拒绝。
- pack 契约行仅 collectionName/metricType 类型约束，**无 TTL 语义约束行**。create/alter 非同一端点，不构成同族不一致的"同一端点"要件。缺文档锚。

### milvus_033 — CONFIRM（枚举闭集客观约束，不需契约背书）
- observed：vectorFieldType=InvalidVectorType 创建 code=0，describe 回显 FloatVector（静默替换默认值）。
- 理由：枚举闭集类客观违反——传入集合外值被接受并静默替换，回显自证替换行为。按七类协议 B=CONFIRMED 不需契约行背书。

### weaviate_003 — CONFIRM（数值下界+静默归一，源码取证具体）
- observed：replicationConfig.factor=-1 → 200 且被静默改写为 1（RESP 回显可核对）。
- 理由：源码取证具体（class.go 先跳过正数校验、再 if Factor < 1 归一为 MinimumFactor，无哨兵注释）；更新路径对 factor<=0 显式报错而创建路径静默吞掉，路径间不一致强化违反判断。三 run 中两 CONFIRMED 一 HUMAN_REVIEW。

### flat+joint 计数影响
upheld = milvus_036/038/043/qdrant_014（沿用）+ milvus_033/weaviate_003（新）= 6；REJECT = 019/027/010；RETURN = 001。
