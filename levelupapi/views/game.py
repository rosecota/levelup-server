"""View module for handling requests about games"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game, Gamer, GameType


class GameView(ViewSet):
    """Level up games view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single games

        Returns:
                        Response -- JSON serialized games
        """
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game)
            return Response(serializer.data)
        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all games

        Returns:
                        Response -- JSON serialized list of games
        """
        games = Game.objects.all()

        # Before sending list to the serializer, check if a query string parameter has been passed to the url
        game_type = request.query_params.get('type', None)
        # Filter by the game type
        if game_type is not None:
            games = games.filter(game_type_id=game_type)

        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        gamer = Gamer.objects.get(user=request.auth.user)
        game_type = GameType.objects.get(pk=request.data["game_type"])

        game = Game.objects.create(
            title=request.data["title"],
            maker=request.data["maker"],
            number_of_players=request.data["number_of_players"],
            skill_level=request.data["skill_level"],
            gamer=gamer,
            game_type=game_type
        )
        serializer = GameSerializer(game)
        return Response(serializer.data)


class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for games
    """
    class Meta:
        model = Game
        fields = ('id',
                  'title',
                  'maker',
                  'number_of_players',
                  'skill_level',
                  'game_type',
                  'gamer')
        depth = 1
