from rest_framework import serializers

from App.models import Car


class CarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Car
        fields = ("id", "c_name")