#!/usr/bin/env python3
"""Quick JSON syntax validator for threat_model.json"""
import json
import sys
from pathlib import Path

def main():
    tm_path = Path("intelligence/qdrant/threat_model.json")

    if not tm_path.exists():
        print(f"ERROR: {tm_path} not found")
        return 1

    try:
        with open(tm_path, encoding='utf-8') as f:
            data = json.load(f)

        # Count ProbeSpecs
        spec_count = 0
        exploration_count = 0
        for tier in ("high_priority_areas", "medium_priority_areas", "low_priority_areas"):
            areas = data.get("attack_surface", {}).get(tier, [])
            for area in areas:
                specs = area.get("probe_specs", [])
                for spec in specs:
                    spec_count += 1
                    if spec.get("evidence", {}).get("exploration_rationale"):
                        exploration_count += 1

        print(f"✓ Valid JSON")
        print(f"✓ Total ProbeSpecs: {spec_count}")
        print(f"✓ Exploration ProbeSpecs: {exploration_count} ({exploration_count/spec_count*100:.1f}%)")

        if spec_count >= 10 and exploration_count >= 5:
            print(f"✓ Meets requirements: ≥10 specs, ≥5 exploration (40%)")
            return 0
        else:
            print(f"✗ Fails requirements")
            return 1

    except json.JSONDecodeError as e:
        print(f"✗ JSON syntax error: {e}")
        return 1
    except Exception as e:
        print(f"✗ Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
