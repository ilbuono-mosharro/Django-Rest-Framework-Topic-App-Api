from django.core.exceptions import PermissionDenied
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters import rest_framework as filters
from .permissions import IsOwnerUser
from .serializers import TopicSerializer, TopicReadSerializer, TopicVoteSerializer
from ..models import Topic
from .d_filters import MyFilters


class TopicViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing topic.
    """
    queryset = Topic.objects.select_related('starter', 'category').prefetch_related(
        'users_upvote', 'users_downvote'
    ).order_by('-created_at')
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MyFilters

    """
     Search and filter based on the Django admin's search functionality.
     from rest_framework import filters
     filter_backends = [filters.SearchFilter, filters.OrderingFilter] 
     search_fields = ['subject'] 
     ordering_fields = ['created_at']
     ordering = ['created_at']..0
    """

    # Simple search filter
    # def get_queryset(self):
    #     queryset = self.queryset
    #     search = self.request.query_params.get('search')
    #     if search is not None:
    #         queryset = queryset.filter(subject__startswith=search)
    #     return queryset


    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return TopicReadSerializer
        return TopicSerializer

    def perform_create(self, serializer):
        serializer.save(starter=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.starter != request.user:
            raise PermissionDenied("You do not have permission to perform this action.")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.starter != request.user:
            raise PermissionDenied("You do not have permission to perform this action.")
        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated, IsOwnerUser], url_path="user-topics")
    def user_topics(self, request, *args, **kwargs):
        user = request.user
        topics = Topic.objects.filter(starter__id=user.id).select_related(
            'starter', 'category'
        ).prefetch_related(
            'users_upvote', 'users_downvote'
        ).order_by('-created_at')
        serializer = TopicReadSerializer(topics, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['put'], permission_classes=[IsAuthenticated], url_path="user-upvote")
    def up_vote(self, request, pk=None):
        topic = self.get_object()
        if topic.users_upvote.filter(id=request.user.id).exists():
            topic.users_upvote.remove(request.user)
        else:
            topic.users_upvote.add(request.user)
            if topic.users_downvote.filter(id=request.user.id).exists():
                topic.users_downvote.remove(request.user)

        serializer = TopicVoteSerializer(topic)
        return Response(serializer.data)

    @action(detail=True, methods=['put'], permission_classes=[IsAuthenticated], url_path="user-downvote")
    def down_vote(self, request, pk=None):
        topic = self.get_object()
        if topic.users_downvote.filter(id=request.user.id).exists():
            topic.users_downvote.remove(request.user)
        else:
            topic.users_downvote.add(request.user)
            if topic.users_upvote.filter(id=request.user.id).exists():
                topic.users_upvote.remove(request.user)
        serializer = TopicVoteSerializer(topic)
        return Response(serializer.data)