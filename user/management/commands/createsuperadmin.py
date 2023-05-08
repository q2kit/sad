from django.core.management.base import BaseCommand, CommandError
from user.models import User

from user.func import hash_password

from getpass import getpass

class Command(BaseCommand):
    help = "Create super admin"

    def handle(self, *args, **options):
        while True:
            username = input("Username: ")
            if User.objects.filter(username=username).exists():
                print("Username already exists")
                continue
            if not username:
                print("Username is required")
                continue
            break

        while True:
            email = input("Email: ")
            if User.objects.filter(email=email).exists():
                print("Email already exists")
                continue
            if not email:
                print("Email is required")
                continue
            break

        while True:
            password1 = getpass()
            if not password1:
                print("Password is required")
                continue
            password2 = getpass("Password (again): ")
            if password1 != password2:
                print("Passwords do not match")
                continue
            if len(password1) < 8:
                confirm = input("Password must be at least 8 characters. Do you want to continue? (y/n): ")
                if confirm.lower() != "y":
                    continue
            break

        user = User.objects.create(
            username=username,
            email=email,
            is_superadmin=True,
            password=hash_password(password1)
        )
        print("Super admin created successfully")
        