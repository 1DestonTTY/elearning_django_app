from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed. Using ReadOnlyModelViewSet ensures people can view the user data via the API, but cannot delete or modify user accounts maliciously through it.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    