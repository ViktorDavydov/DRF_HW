from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        user = User.objects.create(
            email='test@test.ru',
            first_name='test',
            last_name='test',
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )
        user.set_password('qwe123rty456')
        user.save()
