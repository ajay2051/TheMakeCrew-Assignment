from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated

from chat.api.serializers import CustomUserSerializer, MessageSerializer
from chat.models import CustomUser, Message


class RegisterView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.AllowAny]


class MessageList(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated] # Only registered users can see message list

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


class MessageSearch(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated] # Only registered users can search message

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        return Message.objects.filter(content__icontains=query)
