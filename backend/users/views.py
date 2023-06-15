from api.pagination import CustomPagination
from api.serializers import (CustomUserSerializer, FollowSerializer,
                             SubscribeSerializer)
from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    """Вьюсет для кастомной модели пользователя."""
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = CustomPagination

    @action(['POST', 'DELETE'], detail=True)
    def subscribe(self, request, id):
        if request.method == 'POST':
            serializer = FollowSerializer(
                data={
                    'user': request.user.id,
                    'following': self.get_object().id,
                },
                context={'request': request},
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            serializer = SubscribeSerializer(
                self.get_object(),
                context={'request': request},
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        self.get_object().following.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
