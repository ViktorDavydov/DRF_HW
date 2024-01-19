from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from lms.models import Course, Lesson, Payment
from lms.validators import UrlValidator


class LessonSerializer(serializers.ModelSerializer):
    course = SlugRelatedField(slug_field="title", queryset=Course.objects.all())

    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [UrlValidator(url='video_link')]


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lesson = LessonSerializer(many=True, read_only=True)

    def get_lessons_count(self, instance):
        if instance.lesson.all():
            return instance.lesson.all().count()
        return 0

    class Meta:
        model = Course
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    # user = SlugRelatedField(slug_field="email", queryset=User.objects.all())
    # paid_course = SlugRelatedField(slug_field="title", queryset=Course.objects.all())
    # paid_lesson = SlugRelatedField(slug_field="title", queryset=Lesson.objects.all())

    class Meta:
        model = Payment
        fields = '__all__'
