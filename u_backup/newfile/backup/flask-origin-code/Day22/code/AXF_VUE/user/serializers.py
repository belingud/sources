from rest_framework import serializers

from user.models import UserModel


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        # fields = "__all__"
        fields = ("id", "u_name", "u_password", "u_email", "u_icon", "is_delete", "is_active")