from .serializers import AccountRegistrationSerializer, AccountDetailSerializer
from .models import Account
from rest_framework import generics, permissions
from .permissions import IsOwner


class AccountRegisterAPIView(generics.CreateAPIView):
    serializer_class = AccountRegistrationSerializer
    permissions_classes = (permissions.AllowAny,)


class AccountDetailAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = AccountDetailSerializer
    queryset = Account.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner)

