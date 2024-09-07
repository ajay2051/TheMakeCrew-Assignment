from django.urls import path

from chat import views
from chat.api.views import MessageList, MessageSearch, RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('messages/', MessageList.as_view(), name='message-list'),
    path('messages/search/', MessageSearch.as_view(), name='message-search'),

    path("chat/<str:room_name>/", views.room, name="room"),
]
