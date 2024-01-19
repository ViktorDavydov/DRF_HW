from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import User
from users.serializers import UserSerializer, UserOwnerSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer(self, *args, **kwargs):

        if User.objects.filter(email=self.request.user):
            serializer_class = UserOwnerSerializer
        else:
            serializer_class = UserSerializer

        return serializer_class(*args, **kwargs)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=self.request.user.pk)
        if User.objects.filter(email=self.request.user):
            serializer = UserSerializer(user)
        else:
            serializer = UserOwnerSerializer(user)
        return Response(serializer.data)

    def update(self, request, pk=None, *args, **kwargs):
        if User.objects.get(pk=self.request.user.pk) != self.get_object():
            raise PermissionDenied
        return super().update(request, *args, **kwargs)

