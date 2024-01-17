from rest_framework import viewsets
from rest_framework.generics import CreateAPIView

from users.models import User
from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# class UserCreateAPIView(CreateAPIView):
#     serializer_class = UserCreateSerializer
#
#     def perform_create(self, serializer):
#         user = serializer.save()
#         user.set_password(serializer.data['password'])
#         user.save()
