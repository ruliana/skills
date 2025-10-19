#!/usr/bin/env python3
"""
Skill Validator - Validates a skill's structure and metadata

Usage:
    python scripts/validate_skill.py <path/to/skill-folder>

Example:
    python scripts/validate_skill.py ./my-skill
"""

import sys
from pathlib import Path
from quick_validate import validate_skill


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/validate_skill.py <path/to/skill-folder>")
        print("\nExample:")
        print("  python scripts/validate_skill.py ./my-skill")
        sys.exit(1)

    skill_path = Path(sys.argv[1]).resolve()

    # Validate skill folder exists
    if not skill_path.exists():
        print(f"❌ Error: Skill folder not found: {skill_path}")
        sys.exit(1)

    if not skill_path.is_dir():
        print(f"❌ Error: Path is not a directory: {skill_path}")
        sys.exit(1)

    # Run validation
    print(f"🔍 Validating skill: {skill_path.name}")
    print()

    valid, message = validate_skill(skill_path)

    if valid:
        print(f"✅ {message}")
        sys.exit(0)
    else:
        print(f"❌ Validation failed: {message}")
        sys.exit(1)


if __name__ == "__main__":
    main()
