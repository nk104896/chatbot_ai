from django.urls import path
from .views import chatbot_view

urlpatterns = [
    path('gemini/', chatbot_view, name='gemini'),
]
