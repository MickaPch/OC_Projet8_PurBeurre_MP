from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth.hashers import make_password

import os
import json

class Command(BaseCommand):


    def handle(self, *args, **kwargs):

        users = [
            {
                "model": "user.User",
                "pk": 1,
                "fields": {
                    "password": make_password('admin'),
                    "is_superuser": True,
                    "is_staff": True,
                    "is_active": True,
                    "username": "admin",
                    "email": "foo@example.com"
                }
            }
        ]

        path_file = os.path.join(
            os.path.dirname(
                os.path.dirname(
                    os.path.dirname(__file__)
                )
            ),
            'fixtures',
            'users.json'
        )

        with open(path_file, 'w') as file_user:
            file_user.write(json.dumps(users))

        call_command('loaddata', 'users')