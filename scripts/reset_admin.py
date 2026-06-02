#!/usr/bin/env python
"""
Reset or create a Django superuser for this project.

Usage examples (run from project root):
  python scripts/reset_admin.py --username admin --password "NewP@ssw0rd" --email admin@example.com --yes
  python scripts/reset_admin.py --username admin --password "NewP@ssw0rd" --force --yes

Flags:
  --force   Overwrite an existing user with the given username without prompting.
  --yes     Skip interactive confirmation.

This script configures Django settings and uses the project's ORM, so it must be run from the project root
or with the project root on PYTHONPATH. It is intentionally non-interactive unless you omit --yes, in which
case it will ask for confirmation before making changes.
"""

import os
import sys
import argparse


def main():
    parser = argparse.ArgumentParser(description='Create or reset a Django superuser')
    parser.add_argument('--username', required=True, help='Admin username')
    parser.add_argument('--password', required=True, help='Admin password')
    parser.add_argument('--email', default='', help='Admin email (optional)')
    parser.add_argument('--force', action='store_true', help='Overwrite existing user without prompt')
    parser.add_argument('--yes', action='store_true', help='Skip confirmation prompt')
    args = parser.parse_args()

    # Ensure project root is on sys.path (scripts/ is under project root)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sahwira_project.settings')

    try:
        import django
        django.setup()
    except Exception as exc:
        print('Error: could not setup Django environment. Make sure you run this from the project root and the venv is active.')
        print(exc)
        sys.exit(2)

    from django.contrib.auth import get_user_model

    User = get_user_model()

    username = args.username
    password = args.password
    email = args.email

    existing = User.objects.filter(username=username).first()

    if existing:
        if not args.force:
            if not args.yes:
                confirm = input(f"User '{username}' already exists. Overwrite password and make superuser? [y/N]: ").strip().lower()
                if confirm not in ('y', 'yes'):
                    print('Aborted.')
                    sys.exit(0)
        # Update user
        existing.set_password(password)
        if email:
            try:
                existing.email = email
            except Exception:
                pass
        existing.is_staff = True
        existing.is_superuser = True
        existing.save()
        print(f"Updated existing user '{username}' and set superuser/staff flags.")
    else:
        # Create new superuser
        try:
            User.objects.create_superuser(username=username, email=email or '', password=password)
            print(f"Created new superuser '{username}'.")
        except TypeError:
            # Some custom user models expect different args; try a more generic create
            u = User(username=username, email=email or '')
            u.set_password(password)
            u.is_staff = True
            u.is_superuser = True
            u.save()
            print(f"Created new superuser '{username}' (fallback path).")


if __name__ == '__main__':
    main()
