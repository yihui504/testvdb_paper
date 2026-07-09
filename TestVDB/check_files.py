import os
from pathlib import Path

session_dir = Path(r"C:\Users\11428\Desktop\mftui\TestVDB\results\chroma\v1.5.9\2026-07-03T03-55-41Z")

print(f"Checking session dir: {session_dir}")
print(f"Exists: {session_dir.exists()}")

if session_dir.exists():
    print("\n=== Directory structure ===")
    for root, dirs, files in os.walk(session_dir):
        level = root.replace(str(session_dir), '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 2 * (level + 1)
        for file in files[:20]:  # Limit files per dir
            print(f"{subindent}{file}")
        if len(files) > 20:
            print(f"{subindent}... and {len(files)-20} more")
else:
    print("Session directory does not exist!")

    # Check parent dirs
    parent = session_dir.parent
    print(f"\nParent exists: {parent.exists()}")
    if parent.exists():
        print(f"Parent contents: {list(parent.iterdir())}")
