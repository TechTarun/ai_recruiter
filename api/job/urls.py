from django.urls import path
from .views import *

urlpatterns = [
  path('index', Index.as_view()),
  path('index/<str:id>', Index.as_view()),
]