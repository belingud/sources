from rest_framework import serializers

from App.models import Animal, User


class AnimalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Animal
        fields = ("id", "a_name", "a_leg")


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "u_name", "u_password")