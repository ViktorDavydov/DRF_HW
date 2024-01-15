from django.conf import settings
from django.db import models

NULLABLE = {'blank': True, 'null': True}

PAY_CARD = 'card'
PAY_CASH = 'cash'

PAY_TYPES = (
    (PAY_CASH, 'наличные'),
    (PAY_CARD, 'перевод')
)


class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name='название курса')
    preview = models.ImageField(upload_to='lms/', verbose_name='превью', **NULLABLE)
    description = models.TextField(verbose_name='описание')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=200, verbose_name='название урока')
    description = models.TextField(verbose_name='описание')
    preview = models.ImageField(upload_to='lms/', verbose_name='превью', **NULLABLE)
    video_link = models.URLField(verbose_name='ссылка на видео', **NULLABLE)
    course = models.ForeignKey(Course, verbose_name='курс', on_delete=models.CASCADE, **NULLABLE,
                               related_name="lesson")

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='пользователь',
                             on_delete=models.SET_NULL, **NULLABLE, related_name='payment')
    pay_date = models.DateField(verbose_name='дата оплаты')
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='оплаченный курс', **NULLABLE)
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='оплаченный урок', **NULLABLE)
    payment_summ = models.IntegerField(verbose_name='сумма оплаты')
    payment_type = models.CharField(choices=PAY_TYPES, default=PAY_CASH, max_length=10, verbose_name='способ оплаты')

    def __str__(self):
        return f'{self.user} - {self.pay_date}'

    class Meta:
        verbose_name = 'оплата'
        verbose_name_plural = 'оплаты'
