from rest_framework import serializers

from lms.serializers import PaymentSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    payment = PaymentSerializer(many=True)

    class Meta:
        model = User
        fields = '__all__'
