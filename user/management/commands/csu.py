from django.core.management import BaseCommand
from user.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin@local.com',
            is_staff=True,
            is_superuser=True
        )

        user.set_password('admin')
        user.save()

        self.stdout.write(self.style.SUCCESS('Admin created'))
