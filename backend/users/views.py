from api.pagination import CustomPagination
from api.serializers import SubscribeListSerializer, SubscribeSerializer
from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    """Вьюсет для кастомной модели пользователя."""
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination
    serializer_class = SubscribeListSerializer

    @action(['GET'], detail=False)
    def subscriptions(self, request):
        queryset = self.get_queryset().filter(author__user=request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(
            queryset, many=True, context={'request': request})
        return Response(serializer.data)

    @action(['POST', 'DELETE'], detail=True)
    def subscribe(self, request, id):
        if request.method == 'POST':
            serializer = SubscribeSerializer(
                data={
                    'user': request.user.id,
                    'author': self.get_object().id,
                },
                context={'request': request},
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            serializer = SubscribeListSerializer(
                self.get_object(),
                context={'request': request},
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        self.get_object().author.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
