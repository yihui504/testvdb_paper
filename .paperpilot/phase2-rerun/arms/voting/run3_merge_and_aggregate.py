#!/usr/bin/env python3
"""run1 合并 + 聚合驱动：per-case stage2_evidence_{did}.json / stage2_severity_{did}.json
合并成单票 stage2_*.json，然后按原版 aggregate_votes.py 级联规则聚合出判定。

用法（在 arms/voting/ 下）：python run1_merge_and_aggregate.py <runN>
聚合规则与 testvdb4exp/scripts/aggregate_votes.py 逐行同构（SHA 见 PREREG §6），
独立实现以适配 per-case 工作目录（原版读 session 级多票文件，此处每 case 一票）。
崩溃旁路用与原版一致的精确子串表（含 by_design 白名单短路）。
"""
import json, os, sys, glob

VT = os.path.dirname(os.path.abspath(__file__))

_CRASH_PATTERNS = (
    "out of memory", "oom", "oom-killer", "memory exhausted",
    "panic occurred", "panic backtrace", "capacity overflow",
    "hash table capacity overflow",
    "sigsegv", "sigabrt", "sigkill",
    "segmentation fault", "stack overflow",
    "killed", "thread panicked",
)
_CRASH_5XX = (
    '"status":500', '"status": 500', '"status":502', '"status": 502',
    '"status":503', '"status": 503', '"status":504', '"status": 504',
    'status": 500', 'status": 502', 'status": 503',
    "http/1.1 500", "http/1.1 502", "http/1.1 503", "http/1.1 504",
    "http 500", "http 502", "http 503",
    "status:500", "status: 500", "status=500", "status = 500",
    "status:502", "status: 502", "status=502",
    "status:503", "status: 503", "status=503",
    " 500 internal", " 502 bad", " 503 service",
)
_BY_DESIGN = ("jemalloc", "aarch64", "arm64", "address sizes", "libc", "musl")
_TRIVIAL = {"trivial", "none", "info", "negligible"}
_LADDER = ["trivial", "low", "medium", "high", "critical"]


def is_crash(log_text):
    if not log_text:
        return False, ""
    low = log_text.lower()
    if any(kw in low for kw in _BY_DESIGN):
        return False, ""
    for pat in _CRASH_PATTERNS + _CRASH_5XX:
        if pat in low:
            return True, pat
    return False, ""


def demote(level, steps):
    if not level or level not in _LADDER:
        return level
    return _LADDER[max(0, _LADDER.index(level) - steps)]


def main(run):
    cases = sorted(glob.glob(os.path.join(VT, 'sessions', '*', '*', '*', 'candidates', '*.json')))
    results = {}
    n_missing_ev = n_missing_sev = 0
    for p in cases:
        c = json.load(open(p, encoding='utf-8'))
        did = c['defect_id']
        vendor = c['metadata']['vendor']
        wd = os.path.join(VT, run, 'judge_work', did)
        sess = os.path.dirname(os.path.dirname(p))  # sessions/{v}/{ver}/{did}
        # log 从冻结包读（与原版 _read_defect_log 同路径逻辑）
        log = ''
        lp = os.path.join(sess, f'output_{did}.log')
        if os.path.exists(lp):
            log = open(lp, encoding='utf-8', errors='replace').read()

        ev_f = os.path.join(wd, 'debate_logs', f'stage2_evidence_{did}.json')
        sev_f = os.path.join(wd, 'debate_logs', f'stage2_severity_{did}.json')
        if not os.path.exists(ev_f):
            n_missing_ev += 1
            results[did] = {'verdict': 'MISSING_EVIDENCE', 'reason': 'no evidence file'}
            continue
        ev = json.load(open(ev_f, encoding='utf-8'))
        # 合并单票文件 → debate_logs/stage2_evidence.json（聚合器消费形态）
        json.dump({'judge': 'judge-evidence', 'votes': [ev]},
                  open(os.path.join(wd, 'debate_logs', 'stage2_evidence.json'), 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=1)

        # ---- 级联（与原版 run() 同构）----
        crash, pat = is_crash(log)
        if crash:
            results[did] = {'verdict': 'CONFIRMED', 'rule': 'rule0_crash_bypass', 'signal': pat,
                            'evidence_vote': ev.get('vote')}
            continue
        if ev.get('vote') == 'script_error':
            # 原版规则 1：vote != is_defect → rejected（script_error 也拒）
            results[did] = {'verdict': 'FALSE_POSITIVE', 'rule': 'rule1_evidence',
                            'evidence_vote': 'script_error'}
            continue
        if ev.get('vote') != 'is_defect':
            results[did] = {'verdict': 'FALSE_POSITIVE', 'rule': 'rule1_evidence',
                            'evidence_vote': ev.get('vote')}
            continue
        if not os.path.exists(sev_f):
            n_missing_sev += 1
            results[did] = {'verdict': 'FALSE_POSITIVE', 'rule': 'rule2_severity_missing'}
            continue
        sev = json.load(open(sev_f, encoding='utf-8'))
        level = str(sev.get('severity_level') or sev.get('severity') or sev.get('level') or '').lower()
        # doc 全 DOC_PARTIAL（代码直出）→ 规则 6 固定 -1
        level = demote(level, 1)
        if level in _TRIVIAL:
            results[did] = {'verdict': 'FALSE_POSITIVE', 'rule': 'rule3_trivial',
                            'severity_after_doc_demote': level}
            continue
        results[did] = {'verdict': 'CONFIRMED', 'rule': 'rule4_pass',
                        'evidence_grade': ev.get('grade'),
                        'severity_after_doc_demote': level,
                        'defect_type': sev.get('defect_type')}

    conf = sum(1 for r in results.values() if r['verdict'] == 'CONFIRMED')
    out = {'run': run, 'n_cases': len(results), 'confirmed': conf,
           'rejected': len(results) - conf - n_missing_ev - n_missing_sev,
           'missing_evidence': n_missing_ev, 'missing_severity': n_missing_sev,
           'cases': results}
    op = os.path.join(VT, run, 'ARM_VT_AGGREGATION.json')
    json.dump(out, open(op, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f"{run}: {len(results)} cases, confirmed={conf}, missing_ev={n_missing_ev}, missing_sev={n_missing_sev}")
    print(f"-> {op}")


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'run1')
