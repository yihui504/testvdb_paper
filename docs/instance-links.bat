@echo off
REM ============================================================
REM Instance walkthrough (issue #10369) - source link index
REM Each line opens the file at the exact line in VSCode.
REM Usage: double-click this file (or run in terminal). Press any
REM        key between sections to open the next batch.
REM ============================================================

echo [1/5] Knowledge...
code --goto "C:\Users\11428\Desktop\mftui\TestVDB\scripts\fetch_openapi_spec.py:52"
pause

echo [2/5] Behavioral specification...
code --goto "C:\Users\11428\.claude\plugins\cache\testvdb\testvdb\2.3.0\results\qdrant\v1.18.0\structured_contract.json:7291"
pause

echo [3/5] Chunking + pre-binding...
code --goto "C:\Users\11428\Desktop\mftui\TestVDB\scripts\chunk_contract.py:36"
code --goto "C:\Users\11428\Desktop\mftui\TestVDB\scripts\chunk_contract.py:96"
code --goto "C:\Users\11428\Desktop\mftui\TestVDB\scripts\bind_strategies.py:64"
code --goto "C:\Users\11428\.claude\plugins\cache\testvdb\testvdb\2.3.0\results\qdrant\v1.18.0\chunks.json:572"
code --goto "C:\Users\11428\Desktop\mftui\TestVDB\agents\attack-state.md:99"
pause

echo [4/5] Attack generation + gate...
code --goto "C:\Users\11428\Desktop\mftui\TestVDB\agents\attack-state.md:87"
code --goto "C:\Users\11428\Desktop\mftui\TestVDB\commands\mine.md:577"
code --goto "C:\Users\11428\Desktop\mftui\TestVDB\scripts\_preverify_spec_shape.py:272"
code --goto "C:\Users\11428\Desktop\mftui\TestVDB\scripts\_preverify_spec_shape.py:400"
code --goto "C:\Users\11428\Desktop\mftui\TestVDB\scripts\_preverify_spec_shape.py:451"
code --goto "C:\Users\11428\Desktop\mftui\TestVDB\scripts\_preverify_spec_shape.py:515"
code --goto "C:\Users\11428\.claude\plugins\cache\testvdb\testvdb\2.3.0\results\qdrant\v1.18.0\2026-08-27T20-06-45Z\preverify_findings.json:1"
code --goto "C:\Users\11428\.claude\plugins\cache\testvdb\testvdb\2.3.0\results\qdrant\v1.18.0\2026-08-27T20-06-45Z\state_recommend_02_lookup_dim_recreate.preverify_warnings.json:1"
code --goto "C:\Users\11428\.claude\plugins\cache\testvdb\testvdb\2.3.0\results\qdrant\v1.18.0\2026-08-27T20-06-45Z\debate_logs\state_recommend_02_lookup_dim_recreate.meta.json:12"
pause

echo [5/5] Execution - evidence chain - verdict...
code --goto "C:\Users\11428\Desktop\mftui\TestVDB\commands\mine.md:607"
code --goto "C:\Users\11428\Desktop\mftui\TestVDB\commands\mine.md:630"
code --goto "C:\Users\11428\Desktop\mftui\TestVDB\commands\mine.md:669"
code --goto "C:\Users\11428\Desktop\mftui\TestVDB\commands\mine.md:750"
code --goto "C:\Users\11428\Desktop\mftui\TestVDB\agents\evidence-builder.md:55"
code --goto "C:\Users\11428\Desktop\mftui\TestVDB\agents\chain-auditor.md:90"
code --goto "C:\Users\11428\Desktop\mftui\TestVDB\agents\chain-auditor.md:97"
code --goto "C:\Users\11428\Desktop\mftui\TestVDB\agents\chain-auditor.md:169"
code --goto "C:\Users\11428\.claude\plugins\cache\testvdb\testvdb\2.3.0\results\qdrant\v1.18.0\2026-08-27T20-06-45Z\candidates.jsonl:16"
code --goto "C:\Users\11428\.claude\plugins\cache\testvdb\testvdb\2.3.0\results\qdrant\v1.18.0\2026-08-27T20-06-45Z\r21_exec_logs\state_recommend_02_lookup_dim_recreate.log:7"
code --goto "C:\Users\11428\.claude\plugins\cache\testvdb\testvdb\2.3.0\results\qdrant\v1.18.0\2026-08-27T20-06-45Z\evidence_chain\state_recommend_02_lookup_dim_recreate.chain.json:49"
code --goto "C:\Users\11428\.claude\plugins\cache\testvdb\testvdb\2.3.0\results\qdrant\v1.18.0\2026-08-27T20-06-45Z\debate_logs\chain_verdicts.json:17"
pause

echo [src] qdrant v1.18.3 local copy (v1.18.0 clone removed; line numbers drifted)...
code --goto "C:\Users\11428\Desktop\mftui\TestVDB\.sourcedeps\qdrant\v1.18.3\lib\collection\src\recommendations.rs:104"
code --goto "C:\Users\11428\Desktop\mftui\TestVDB\.sourcedeps\qdrant\v1.18.3\lib\collection\src\recommendations.rs:339"
code --goto "C:\Users\11428\Desktop\mftui\TestVDB\.sourcedeps\qdrant\v1.18.3\lib\segment\src\common\mod.rs:194"

echo Done.
pause
