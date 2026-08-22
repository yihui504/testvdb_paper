# -*- coding: utf-8 -*-
"""作废操作（2026-08-22 用户指令）：违规轮次产物移 voided/ 留证 + chain_verdicts 回退 + 声明。
作废原则：违规直接污染的环节产物。executor 主进程批量 = 该轮执行产物（链证据 B 环）无效。"""
import json, os, shutil, sys, glob as g
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8')
CACHE = r'C:/Users/11428/.claude/plugins/cache/testvdb/testvdb/2.3.0/results/milvus'

def decl(ver, note):
    with open(os.path.join(CACHE, ver, 'VOIDED.md'), 'w', encoding='utf-8') as f:
        f.write('# 作废声明（2026-08-22 用户指令）\n\n' + note + '\n')

def move_patterns(pats):
    vd_moved = 0
    for pat in pats:
        for f in g.glob(pat):
            dest_dir = os.path.join(os.path.dirname(os.path.dirname(f)), 'voided')
            os.makedirs(dest_dir, exist_ok=True)
            shutil.move(f, os.path.join(dest_dir, os.path.basename(f)))
            vd_moved += 1
    return vd_moved

def revert(sess_dir, drop_ids):
    cvp = os.path.join(sess_dir, 'debate_logs', 'chain_verdicts.json')
    cv = json.load(open(cvp, encoding='utf-8'))
    keep = [v for v in cv['verdicts'] if v['defect_id'] not in drop_ids]
    c = Counter(v['verdict'] for v in keep)
    cv['verdicts'] = keep
    cv['total_chains'] = len(keep)
    cv['summary'].update({'defect': c.get('DEFECT', 0), 'not_defect': c.get('NOT_DEFECT', 0),
                          'needs_more_evidence': c.get('NEEDS_MORE_EVIDENCE', 0),
                          'note': 'VOIDED 2026-08-22: 见版本根 VOIDED.md'})
    json.dump(cv, open(cvp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    return len(keep)

# ── #8 milvus v2.3.22：R2 作废（主进程 executor） ──
S8 = os.path.join(CACHE, 'v2.3.22', '2026-08-21T18-44-26Z')
n = move_patterns([S8 + '/debate_logs/state_r2_*', S8 + '/debate_logs/output_state_r2_*',
                   S8 + '/debate_logs/exit_code_state_r2_*', S8 + '/evidence_chain/state_r2_*'])
keep = revert(S8, {'state_r2_release_inflight_004', 'state_r2_insert_search_visibility_005', 'state_r2_upsert_delete_race_007'})
decl('v2.3.22', 'R2 三链作废（executor 由主进程批量替代，违规）。rowCount 族翻案随之作废（回 R1 判定：三链 DEFECT 维持）。GT 47635 单列的 load_immediacy 正面测证据作废（R2 产物）——单列依据降级为 issue 自述 standalone 低复现率。移入 voided/ %d 项；chain_verdicts 回退至 %d 链（R1 only）。' % (n, keep))

# ── #9 milvus v2.6.10：R2b 作废（主进程 executor） ──
S9 = os.path.join(CACHE, 'v2.6.10', '2026-08-21T20-31-04Z')
n = move_patterns([S9 + '/debate_logs/*_r2b_*', S9 + '/debate_logs/output_*_r2b_*',
                   S9 + '/debate_logs/exit_code_*_r2b_*', S9 + '/evidence_chain/*_r2b_*'])
R2B = {'boundary_r2b_rowfield_names_01', 'boundary_r2b_dyn_crosstype_02', 'boundary_r2b_upsert_rowface_03',
       'boundary_r2b_insert_param_confusion_04', 'semantic_r2b_dynfield_readback_03',
       'semantic_r2b_nprobe_diag_05', 'semantic_r2b_nprobe_domain_01'}
keep = revert(S9, R2B)
decl('v2.6.10', 'R2b 七链作废（executor 由主进程批量替代，违规）——盲注独立命中的 fieldName/dataType/nprobe 三链证据链无效。#9 最终=R1 only（%d 链，GT 2/5：ef/filter，均为 executor agent 产物）。原 R2 引导轮此前已 tainted-r2-guided/。移入 voided/ %d 项。' % (keep, n))

# ── #10 milvus v2.6.12：R2 三链+复现脚本作废 ──
S10 = os.path.join(CACHE, 'v2.6.12', '2026-08-21T22-15-23Z')
n = move_patterns([S10 + '/debate_logs/state_r2_*', S10 + '/debate_logs/output_state_r2_*',
                   S10 + '/debate_logs/exit_code_state_r2_*', S10 + '/debate_logs/semantic_r2_gt49059_repro_05*',
                   S10 + '/evidence_chain/state_r2_*'])
keep = revert(S10, {'state_r2_release_inflight_004', 'state_r2_insert_search_visibility_005', 'state_r2_upsert_delete_race_007'})
decl('v2.6.12', 'R2 三链（主进程 executor）+ 49059 复现脚本（主进程写并执行——架构违规）作废。49059 单列判定降级为部分验证（FLAT 精度矩阵阴性系 agent 产物保留；IVF_FLAT 精确复刻阴性作废）。#10 最终=R1 only（%d 链，GT 0/1 单列部分验证）。移入 voided/ %d 项。' % (keep, n))

# ── #11 milvus v2.6.16：R2 盲注轮作废（主进程 executor） ──
S11 = os.path.join(CACHE, 'v2.6.16', '2026-08-21T23-37-54Z')
n = move_patterns([S11 + '/debate_logs/boundary_r2_*', S11 + '/debate_logs/output_boundary_r2_*',
                   S11 + '/debate_logs/exit_code_boundary_r2_*', S11 + '/evidence_chain/boundary_r2_*',
                   S11 + '/evidence_chain/boundary_extrakeys_08*'])
keep = revert(S11, {'boundary_r2_search_zero_22', 'boundary_r2_dbname_empty_26', 'boundary_r2_query_zero_23',
                    'boundary_r2_create_zero_20', 'boundary_r2_alterprops_27', 'boundary_extrakeys_08'})
decl('v2.6.16', 'R2 盲注五链 + extrakeys 重审作废（executor 由主进程批量替代，违规）——GT 49823/49930 的一链双命中证据链无效。#11 最终=R1 only（%d 链 6 DEFECT，GT 0/4）。首轮主进程脚本此前已 tainted-mainproc-scripts/。移入 voided/ %d 项。' % (keep, n))

# ── #12 milvus v2.6.17：C/D 段全作废（R1+R2 主进程 executor + R2 合体自审） ──
S12 = os.path.join(CACHE, 'v2.6.17', '2026-08-22T01-39-12Z')
VD12 = os.path.join(CACHE, 'v2.6.17', 'voided')
os.makedirs(VD12, exist_ok=True)
if os.path.exists(S12) and not os.path.exists(os.path.join(VD12, '2026-08-22T01-39-12Z')):
    shutil.move(S12, os.path.join(VD12, '2026-08-22T01-39-12Z'))
decl('v2.6.17', 'C/D 段全作废：R1+R2 的 executor 均由主进程批量替代（违规）；R2 四链由 builder+auditor 合体自审（判定独立性违规）。15 链 12 DEFECT 与 GT 1/4（password）全部无效。A/B 段（知识+契约）保留有效。session 整体移入 voided/。')

# ── #13 milvus v2.6.18：C 段作废（主进程 executor；合体派发未遂） ──
S13 = os.path.join(CACHE, 'v2.6.18', '2026-08-22T03-36-20Z')
VD13 = os.path.join(CACHE, 'v2.6.18', 'voided')
os.makedirs(VD13, exist_ok=True)
if os.path.exists(S13) and not os.path.exists(os.path.join(VD13, '2026-08-22T03-36-20Z')):
    shutil.move(S13, os.path.join(VD13, '2026-08-22T03-36-20Z'))
decl('v2.6.18', 'C 段作废：R1 的 executor 由主进程批量替代（违规）；builder+auditor 合体派发被用户拦截（未遂）。A/B 段保留有效。session 移入 voided/。')

print('作废操作完成：v2.3.22(R2) / v2.6.10(R2b) / v2.6.12(R2+repro) / v2.6.16(R2) / v2.6.17(C+D) / v2.6.18(C)')
