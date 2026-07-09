#!/usr/bin/env python3
"""
ADR-011 Compliance Validator
Validates that threat model meets ≥40% exploration ProbeSpec quota.
"""

import json
import sys

def main():
    with open('intelligence/qdrant/threat_model.json', 'r') as f:
        tm = json.load(f)

    total, exploration, historical = 0, 0, 0
    pattern_type_distribution = {}

    for tier in ('high_priority_areas', 'medium_priority_areas', 'low_priority_areas'):
        for area in tm.get('attack_surface', {}).get(tier, []):
            for spec in area.get('probe_specs', []):
                total += 1

                # Count exploration vs historical
                rationale = spec.get('rationale', '')
                hist_refs = spec.get('evidence', {}).get('historical_refs', [])

                is_exploration = '[exploration]' in rationale and len(hist_refs) == 0
                is_historical = len(hist_refs) > 0

                if is_exploration:
                    exploration += 1
                elif is_historical:
                    historical += 1

                # Track pattern types
                pattern_type = spec.get('probe_pattern', {}).get('type', 'unknown')
                pattern_type_distribution[pattern_type] = pattern_type_distribution.get(pattern_type, 0) + 1

    ratio = exploration / total if total else 0

    print(f"ProbeSpec Statistics:")
    print(f"  Total: {total}")
    print(f"  Exploration: {exploration} ({ratio:.0%})")
    print(f"  Historical: {historical}")
    print(f"\nPattern Type Distribution:")
    for ptype, count in sorted(pattern_type_distribution.items()):
        print(f"  {ptype}: {count}")

    print(f"\nADR-011 Validation:")
    if ratio >= 0.40:
        print(f"  ✓ PASS: {ratio:.0%} ≥ 40%")
        return 0
    else:
        print(f"  ✗ FAIL: {ratio:.0%} < 40%")
        return 1

if __name__ == '__main__':
    sys.exit(main())
