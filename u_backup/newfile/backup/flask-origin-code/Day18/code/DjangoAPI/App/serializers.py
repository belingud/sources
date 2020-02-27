from rest_framework import serializers

from App.models import User, Animal


class AnimalSerializer(serializers.ModelSerializer):
    # 多对一级联显示，默认id
    a_user = serializers.ReadOnlyField(source="a_user.u_name", read_only=True)

    class Meta:
        model = Animal
        fields = ("id", "a_name", "a_user")


class UserSerializer(serializers.ModelSerializer):

    u_animals = AnimalSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ("id", "u_name", "u_password", "u_animals")
