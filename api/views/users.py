from rest_framework.permissions import IsAuthenticated

from api.permissions import IsAdminOnly
from api.serializers import UserSerializer
from api.services.user_service import UserService
from .mixins import StandardResponseModelViewSet


class UserViewSet(StandardResponseModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminOnly]
    list_message = "Users Fetched Successfully"
    retrieve_message = "User Fetched Successfully"

    def get_queryset(self):
        return UserService.list_users()
