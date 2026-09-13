#!/usr/bin/env python3
"""design-slides 五维质量审查的确定性部分（借 harness-anything PPT 设计系统质量审查）。

把五维中可 grep 的三维脚本化（conventions §1 务实混合）：
  1. 字号下限  —— 扫 \\tiny / \\scriptsize（正文用它们 = 坏信号）
  2. 备注覆盖  —— frame 数 vs \\note 数，覆盖率 < 1 即漏备注
  5. 配色复杂度—— \\definecolor 数量（一个主题色 + 一个强调色，多了 = 混乱信号）

另两维（信息密度、布局混用）是判断，留 [design-slides](../SKILL.md) 的审查清单，
不下沉脚本。

exit 0（报告，不 fail-closed——slides 质量非编译错误，是审查建议）。

CLI：
  python skills/design-slides/scripts/check_slides.py <slides.tex>
  python skills/design-slides/scripts/check_slides.py <slides.tex> --json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional

_FRAME_RE = re.compile(r"\\begin\{frame\}")
_ENDFRAME_RE = re.compile(r"\\end\{frame\}")
_NOTE_RE = re.compile(r"\\note")
_TINY_RE = re.compile(r"\\tiny\b|\\scriptsize\b")
_DEFCOLOR_RE = re.compile(r"\\definecolor")


def analyze(text: str) -> Dict[str, object]:
    """分析 Beamer 源，返回 {frames, notes, note_coverage, tiny, definecolor, tiny_lines, note_missing, issues}。"""
    frames = 0
    notes = 0
    tiny = 0
    definecolor = 0
    tiny_lines: List[int] = []
    # R1 (Phase 3 Y7): per-frame state machine — "33%（1/3）" named nothing, so
    # the frames missing a \note are listed with their \begin{frame} line number
    note_missing: List[Dict[str, int]] = []
    frame_no = 0
    frame_open_line: Optional[int] = None
    frame_has_note = False
    for lineno, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if not stripped or stripped.startswith("%"):
            continue
        if _FRAME_RE.search(line):
            # an unclosed previous frame counts as note-less too
            if frame_open_line is not None and not frame_has_note:
                note_missing.append({"frame": frame_no, "line": frame_open_line})
            frame_no += 1
            frame_open_line = lineno
            frame_has_note = False
            frames += len(_FRAME_RE.findall(line))
        if _NOTE_RE.search(line):
            notes += len(_NOTE_RE.findall(line))
            frame_has_note = True
        if _ENDFRAME_RE.search(line) and frame_open_line is not None:
            if not frame_has_note:
                note_missing.append({"frame": frame_no, "line": frame_open_line})
            frame_open_line = None
            frame_has_note = False
        tiny += len(_TINY_RE.findall(line))
        if _TINY_RE.search(line):
            tiny_lines.append(lineno)
        definecolor += len(_DEFCOLOR_RE.findall(line))
    if frame_open_line is not None and not frame_has_note:
        note_missing.append({"frame": frame_no, "line": frame_open_line})

    issues: List[str] = []
    note_coverage = (notes / frames) if frames else 0.0
    if frames and notes < frames:
        issues.append("备注覆盖不足：%d/%d frames 有 \\note" % (notes, frames))
    if tiny:
        issues.append("正文用了 %d 处 \\tiny/\\scriptsize（字号下限违规）" % tiny)
    if definecolor > 3:
        issues.append("定义了 %d 个颜色（配色复杂度偏高，应 1 主题 + 1 强调）" % definecolor)
    return {
        "frames": frames,
        "notes": notes,
        "note_coverage": round(note_coverage, 3),
        "tiny_scriptsize": tiny,
        "tiny_lines": tiny_lines,
        "note_missing": note_missing,
        "definecolor": definecolor,
        "issues": issues,
    }


def _ensure_utf8_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            try:
                reconfigure(encoding="utf-8")
            except (ValueError, LookupError, OSError):
                pass


def main(argv: Optional[List[str]] = None) -> int:
    _ensure_utf8_stdio()
    ap = argparse.ArgumentParser(description="design-slides 五维质量审查（确定性部分）")
    ap.add_argument("path", help="slides.tex")
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    args = ap.parse_args(argv)
    try:
        text = Path(args.path).read_text(encoding="utf-8-sig")
    except OSError as e:
        sys.exit("读文件失败：%s" % e)
    result = analyze(text)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(
            "frames=%d notes=%d coverage=%.0f%% tiny/scriptsize=%d definecolor=%d"
            % (
                result["frames"],
                result["notes"],
                float(result["note_coverage"]) * 100,
                result["tiny_scriptsize"],
                result["definecolor"],
            )
        )
        for issue in result["issues"]:  # type: ignore[union-attr]
            print("  - %s" % issue)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
