from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from LearnSerializer.models import Game
from LearnSerializer.serializers import GameSerializer


class GamesView(View):

    def get(self, request):
        games = Game.objects.all()

        serializer = GameSerializer(games, many=True, context={'request': request})

        return JsonResponse(serializer.data,  safe=False)

    def post(self, request):

        g_name = request.POST.get("g_name")
        g_price = request.POST.get("g_price")

        source_data = {
            "g_name": g_name,
            "g_price": g_price
        }

        serializer = GameSerializer(data=source_data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)

        return JsonResponse(serializer.errors)


class GameView(View):

    def get(self, request, pk):
        game = Game.objects.get(pk=pk)

        serializer = GameSerializer(game, context={'request': request})

        return JsonResponse(serializer.data)
