from django.urls import path
from .views import *

urlpatterns = [
  path('signup', Signup.as_view()),
  path('login', Login.as_view()),
  path('all_applied/<str:app_id>', AllApplied.as_view()),
  path('applied/<str:app_id>', AppliedDetails.as_view()),
  path('book_slot', BookSlot.as_view()),
]