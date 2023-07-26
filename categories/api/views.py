from rest_framework import viewsets

from categories.models import Category
from .permission import IsAdminOrReadOnly
from .serializers import CategoryReadSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing categories.
    """
    queryset = Category.objects.select_related('user')
    serializer_class = CategoryReadSerializer
    permission_classes = [IsAdminOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)