"""Quick validation script for threat_model.json"""
import json
import sys
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent))

from lib.threat_model import is_valid_probe_spec

def count_probespecs(threat_model: dict) -> int:
    """Count total ProbeSpecs across all priority areas"""
    count = 0
    attack_surface = threat_model.get("attack_surface", {})
    for tier in ("high_priority_areas", "medium_priority_areas", "low_priority_areas"):
        areas = attack_surface.get(tier, [])
        if not isinstance(areas, list):
            continue
        for area in areas:
            specs = area.get("probe_specs", [])
            if isinstance(specs, list):
                count += len(specs)
    return count

def get_probe_types(threat_model: dict) -> set:
    """Collect unique probe_pattern.type values"""
    types = set()
    attack_surface = threat_model.get("attack_surface", {})
    for tier in ("high_priority_areas", "medium_priority_areas", "low_priority_areas"):
        areas = attack_surface.get(tier, [])
        if not isinstance(areas, list):
            continue
        for area in areas:
            specs = area.get("probe_specs", [])
            if isinstance(specs, list):
                for spec in specs:
                    if isinstance(spec, dict):
                        pp = spec.get("probe_pattern", {})
                        if isinstance(pp, dict):
                            ptype = pp.get("type")
                            if ptype:
                                types.add(ptype)
    return types

def main():
    tm_path = Path("intelligence/qdrant/threat_model.json")

    if not tm_path.exists():
        print(f"ERROR: {tm_path} not found")
        return 1

    with open(tm_path, encoding="utf-8") as f:
        threat_model = json.load(f)

    # Count ProbeSpecs
    total_specs = count_probespecs(threat_model)
    probe_types = get_probe_types(threat_model)

    print(f"✓ Total ProbeSpecs: {total_specs}")
    print(f"✓ Probe pattern types: {sorted(probe_types)}")

    # Validate all ProbeSpecs
    errors = []
    spec_count = 0

    attack_surface = threat_model.get("attack_surface", {})
    for tier in ("high_priority_areas", "medium_priority_areas", "low_priority_areas"):
        areas = attack_surface.get(tier, [])
        if not isinstance(areas, list):
            continue
        for area in areas:
            area_name = area.get("area", "<unnamed>")
            specs = area.get("probe_specs", [])
            if not isinstance(specs, list):
                continue
            for spec in specs:
                if isinstance(spec, dict):
                    spec_count += 1
                    spec_id = spec.get("id", f"<no-id>")
                    ok, msg = is_valid_probe_spec(spec)
                    if not ok:
                        errors.append(f"[{area_name}] '{spec_id}': {msg}")

    print(f"✓ Validated {spec_count} ProbeSpecs")

    if errors:
        print(f"\n✗ {len(errors)} validation error(s):")
        for err in errors:
            print(f"  - {err}")
        return 1

    print("\n✓ All ProbeSpecs PASS validation")
    return 0

if __name__ == "__main__":
    sys.exit(main())
