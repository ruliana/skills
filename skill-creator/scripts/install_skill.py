#!/usr/bin/env python3
"""
Skill Installer - Installs a skill to personal or project skills folder

Usage:
    python scripts/install_skill.py <path/to/skill-folder> --personal
    python scripts/install_skill.py <path/to/skill-folder> --project

Options:
    --personal    Install to ~/.claude/skills/<skill-name>
    --project     Install to ./.claude/skills/<skill-name>

Example:
    python scripts/install_skill.py ./my-skill --personal
    python scripts/install_skill.py ./my-skill --project
"""

import sys
import os
from pathlib import Path
from quick_validate import validate_skill


def get_confirmation(message):
    """Ask user for yes/no confirmation"""
    while True:
        response = input(f"{message} (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            print("Please enter 'y' or 'n'")


def install_skill(skill_path, install_type):
    """
    Install a skill by creating a symlink.

    Args:
        skill_path: Path to the skill folder
        install_type: Either 'personal' or 'project'

    Returns:
        True if successful, False otherwise
    """
    skill_path = Path(skill_path).resolve()

    # Validate skill folder exists
    if not skill_path.exists():
        print(f"❌ Error: Skill folder not found: {skill_path}")
        return False

    if not skill_path.is_dir():
        print(f"❌ Error: Path is not a directory: {skill_path}")
        return False

    # Validate SKILL.md exists
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        print(f"❌ Error: SKILL.md not found in {skill_path}")
        return False

    # Run validation
    print("🔍 Validating skill...")
    valid, message = validate_skill(skill_path)
    if not valid:
        print(f"❌ Validation failed: {message}")
        print("   Please fix the validation errors before installing.")
        return False
    print(f"✅ {message}\n")

    # Determine destination path
    skill_name = skill_path.name

    if install_type == 'personal':
        dest_base = Path.home() / ".claude" / "skills"
    else:  # project
        dest_base = Path.cwd() / ".claude" / "skills"

    dest_path = dest_base / skill_name

    # Check if skill already exists
    if dest_path.exists() or dest_path.is_symlink():
        print(f"⚠️  Skill '{skill_name}' already exists at: {dest_path}")

        # Show current link target if it's a symlink
        if dest_path.is_symlink():
            current_target = dest_path.resolve()
            print(f"   Current symlink points to: {current_target}")

        if not get_confirmation("   Do you want to overwrite it?"):
            print("❌ Installation cancelled.")
            return False

        # Remove existing skill
        if dest_path.is_symlink():
            dest_path.unlink()
        elif dest_path.is_dir():
            print(f"   Removing existing directory...")
            import shutil
            shutil.rmtree(dest_path)
        else:
            dest_path.unlink()

    # Create destination directory if needed
    dest_base.mkdir(parents=True, exist_ok=True)

    # Create symlink
    try:
        dest_path.symlink_to(skill_path, target_is_directory=True)
        install_location = "personal" if install_type == 'personal' else "project"
        print(f"✅ Successfully installed skill to {install_location} folder:")
        print(f"   {dest_path} -> {skill_path}")
        return True
    except Exception as e:
        print(f"❌ Error creating symlink: {e}")
        return False


def main():
    if len(sys.argv) < 3:
        print("Usage: python scripts/install_skill.py <path/to/skill-folder> <--personal|--project>")
        print("\nOptions:")
        print("  --personal    Install to ~/.claude/skills/<skill-name>")
        print("  --project     Install to ./.claude/skills/<skill-name>")
        print("\nExample:")
        print("  python scripts/install_skill.py ./my-skill --personal")
        print("  python scripts/install_skill.py ./my-skill --project")
        sys.exit(1)

    skill_path = sys.argv[1]
    flag = sys.argv[2]

    # Validate flag
    if flag == "--personal":
        install_type = "personal"
    elif flag == "--project":
        install_type = "project"
    else:
        print(f"❌ Error: Invalid flag '{flag}'")
        print("   Use --personal or --project")
        sys.exit(1)

    install_location = "personal" if install_type == 'personal' else "project"
    print(f"📦 Installing skill to {install_location} folder: {skill_path}")
    print()

    success = install_skill(skill_path, install_type)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
