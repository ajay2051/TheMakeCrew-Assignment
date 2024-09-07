from django.urls import path

from chat.api.views import RegisterView, MessageList, MessageSearch

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('messages/', MessageList.as_view(), name='message-list'),
    path('messages/search/', MessageSearch.as_view(), name='message-search'),
]