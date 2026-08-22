# -*- coding: utf-8 -*-
"""checklist 修订（行前缀定位整行替换）"""
import io, sys
sys.stdout.reconfigure(encoding='utf-8')
p = r'C:/Users/11428/Desktop/testvdb_paper/docs/rq1-fullrun-checklist.md'
lines = io.open(p, encoding='utf-8').read().split('\n')
newrows = {
 '| 8 | milvus | v2.3.22':
 '| 8 | milvus | v2.3.22 | 1 (47635) | [x] 2026-08-22 **部分作废** | 0/1 **单列（依据降级）**：R2 的 load_immediacy 正面测证据作废（executor 主进程违规）——单列依据仅剩 issue 自述 standalone 低复现率；stale-bot 关闭非修复 | **18/18**（R1 only） | 12（R1 DEFECT；rowCount 翻案随 R2 作废回 R1 判定） | 有效=R1 段 | **R2 作废 2026-08-22**（executor 主进程批量违规）：3 链+rowCount 翻案+47635 正面测全部无效，留证 voided/；source-derived 路径与错误信封锚仍有效 |',
 '| 9 | milvus | v2.6.10':
 '| 9 | milvus | v2.6.10 | 5 (47729,47752,47755,47763,47766) | [x] 2026-08-22 **部分作废** | **2/5**（R1 ef/filter；R2b 的 fieldName/dataType/nprobe 命中作废） | **21/21**（R1 only） | 10（R1 DEFECT） | 有效=R1 段 | **两轮 R2 均作废 2026-08-22**：原轮=引导产物（查 issue 后补契约）；R2b 重跑轮=executor 主进程批量违规——盲注独立命中方法实证价值在记录、链证据无效；双留证 |',
 '| 10 | milvus | v2.6.12':
 '| 10 | milvus | v2.6.12 | 1 (49059) | [x] 2026-08-22 **部分作废** | 0/1 **单列部分验证**：FLAT 精度矩阵阴性保留（agent 产物）；IVF_FLAT 精确复刻阴性作废（主进程写并执行）；机械 s05 假命中盲评驳回不变 | **18/18**（R1 only） | 11（R1 DEFECT） | 有效=R1 段 | **R2+复现脚本作废 2026-08-22**（主进程 executor+主进程写脚本）；verify 下划线兼容修复仍有效 |',
 '| 11 | milvus | v2.6.16':
 '| 11 | milvus | v2.6.16 | 4 (49823,49889,49930,50018) | [x] 2026-08-22 **部分作废** | **0/4**（R2 一链双命中证据作废后 R1 无命中） | **11/11**（R1 only） | 6（R1 DEFECT：query_mode 族） | 有效=R1 段 | **R2 盲注轮作废 2026-08-22**（executor 主进程批量违规）：首轮主进程脚本 tainted+重跑轮违规——49823/49930 命中无效；auditor-官方分歧记录（49889）仍有效 |',
 '| 12 | milvus | v2.6.17':
 '| 12 | milvus | v2.6.17 | 4 (49890,50323,50353,50354) | [ ] **C/D 作废 2026-08-22** | —（GT 1/4 作废） | —（15 链全废） | — | **C/D 段全作废**：R1+R2 executor 主进程批量违规 + R2 四链 builder+auditor 合体自审（判定独立性违规）；A/B 段保留（100 端点/45 constraints）；**待按纪律重跑 C/D** |',
 '| 13 | milvus | v2.6.18':
 '| 13 | milvus | v2.6.18 | 2 (49843,50355) | [ ] **C 段作废 2026-08-22** | /2 | / | / | — | A/B 段保留（100 端点/48 constraints/污染断言已移除）；R1 executor 违规+合体派发未遂（用户拦截）；**待按纪律重跑 C** |',
}
hit = 0
for i, ln in enumerate(lines):
    for prefix, new in newrows.items():
        if ln.startswith(prefix):
            lines[i] = new; hit += 1; break
io.open(p, 'w', encoding='utf-8').write('\n'.join(lines))
print(f'checklist 修订 {hit}/6 行')
