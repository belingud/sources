from rest_framework import serializers

from LearnSerializer.models import Game

#
# class GameSerializer(serializers.Serializer):
#
#     id = serializers.IntegerField(read_only=True)
#     g_name = serializers.CharField(max_length=32)
#     g_price = serializers.FloatField(default=1)
#
#     def create(self, validated_data):
#         return Game.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         # instance.g_name = validated_data.get("g_name", instance.g_name)
#         instance.g_name = validated_data.get("g_name") or instance.g_name
#         instance.g_price = validated_data.get("g_price") or instance.g_price
#         instance.save()
#         return instance

#
# # 最实用的　　　开发中使用最多
# class GameSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Game
#         fields = ("id", "g_name", "g_price")


# 缺一个级联路由　　　　/ser/games/id/
class GameSerializer(serializers.HyperlinkedModelSerializer):
    """
        自定义使用的时候，需要进行一些额外的配置
            ①　包含详情页面
                可以接收　ｉｄ
            ②　详情页面还要拥有指定的名字
                name = 模型名-detail
            ③　在实例化序列化器的时候，传递上下文
                context = {'request': request}

    """
    class Meta:
        model = Game
        fields = ("url", "g_name", "g_price")

