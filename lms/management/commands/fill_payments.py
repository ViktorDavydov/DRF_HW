from django.core.management import BaseCommand

from lms.models import Payment, Course, Lesson
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        payment_list = [
            {
                "user": User.objects.get(email='davydov.viktor.andreevich@gmail.com'),
                "pay_date": "2023-11-29",
                "paid_course": Course.objects.get(title="Python"),
                "paid_lesson": None,
                "payment_summ": 20000,
                "payment_type": "перевод"
            },
            {
                "user": User.objects.get(email='davydov.viktor.andreevich@gmail.com'),
                "pay_date": "2023-12-15",
                "paid_course": Course.objects.get(title="Python"),
                "paid_lesson": None,
                "payment_summ": 35000,
                "payment_type": "перевод"
            },
            {
                "user": User.objects.get(email='davydov.viktor.andreevich@gmail.com'),
                "pay_date": "2023-12-31",
                "paid_course": None,
                "paid_lesson": Lesson.objects.get(title="Generics"),
                "payment_summ": 5000,
                "payment_type": "наличные"
            },
            {
                "user": User.objects.get(email='davydov.viktor.andreevich@gmail.com'),
                "pay_date": "2024-01-01",
                "paid_course": None,
                "paid_lesson": Lesson.objects.get(title="Serializers"),
                "payment_summ": 8000,
                "payment_type": "наличные"
            },
            {
                "user": User.objects.get(email='davydov.viktor.andreevich@gmail.com'),
                "pay_date": "2024-01-15",
                "paid_course": None,
                "paid_lesson": Lesson.objects.get(title="ViewSets"),
                "payment_summ": 1000,
                "payment_type": "перевод"
            }

        ]
        payments_for_create = []
        for payment_item in payment_list:
            payments_for_create.append(Payment(**payment_item))

        Payment.objects.all().delete()
        Payment.objects.bulk_create(payments_for_create)
