from django.urls import path
from .views import *

urlpatterns = [
  path('signup', Signup.as_view()),
  path('login', Login.as_view()),
  path('all_applied/<str:id>', AllApplied.as_view()),
  path('applied/<str:id>', AppliedDetails.as_view()),
  path('book_slot', BookSlot.as_view()),
]