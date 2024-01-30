from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import OrderingFilter
from rest_framework import viewsets, generics, serializers
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from lms.models import Course, Lesson, Payment, CourseSubscription
from lms.paginators import CoursePaginator, LessonPaginator
from lms.permissions import IsModerator, IsOwnerOrStaffUser
from lms.serializers import CourseSerializer, LessonSerializer, PaymentSerializer, \
    SubscribeSerializer, PaymentCreateSerializer
from lms.services import get_session, retrieve_session


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CoursePaginator

    def get_queryset(self):
        if self.request.user.is_staff:
            return Course.objects.all()
        elif not self.request.user.is_staff:
            return Course.objects.filter(owner=self.request.user)
        else:
            raise PermissionDenied

    def create(self, request, *args, **kwargs):
        if request.user.groups.filter(name='moderator'):
            raise PermissionDenied
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if request.user.groups.filter(name='moderator'):
            raise PermissionDenied
        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = LessonPaginator

    def get_queryset(self):
        if self.request.user.is_staff:
            return Lesson.objects.all()
        elif not self.request.user.is_staff:
            return Lesson.objects.filter(owner=self.request.user)
        else:
            raise PermissionDenied


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrStaffUser]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrStaffUser]


class LessonDestroyAPIView(generics.DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator]


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('paid_course', 'paid_lesson', 'payment_type',)
    ordering_fields = ('pay_date',)

    def get_queryset(self):
        if not self.request.user.is_staff:
            return Payment.objects.filter(user=self.request.user)
        elif self.request.user.is_staff:
            return Payment.objects.all()
        else:
            raise PermissionDenied


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentCreateSerializer

    def perform_create(self, serializer):
        course = serializer.validated_data.get('paid_course')
        if not course:
            raise serializers.ValidationError('Не указан курс.')
        payment = serializer.save()
        payment.user = self.request.user
        if payment.payment_type == 'перевод':
            payment.session = get_session(payment).id
        payment.save()


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])
        if obj.session:
            session = retrieve_session(obj.session)
            if session.payment_status == 'paid' and session.status == 'complete':
                obj.is_successful = True
                obj.save()
        self.check_object_permissions(self.request, obj)
        return obj


class SubscriptionCreateAPIView(generics.CreateAPIView):
    serializer_class = SubscribeSerializer
    permission_classes = [IsAuthenticated, IsModerator]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SubscriptionListAPIView(generics.ListAPIView):
    serializer_class = SubscribeSerializer

    def get_queryset(self):
        return CourseSubscription.objects.filter(user=self.request.user)


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    serializer_class = SubscribeSerializer
    queryset = CourseSubscription.objects.all()
    permission_classes = [IsAuthenticated, IsModerator]
