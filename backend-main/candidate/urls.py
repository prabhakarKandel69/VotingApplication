from django.urls import path
from .views import CandidateListCreate

urlpatterns = [
    path('candidates/', CandidateListCreate.as_view(), name='candidate-list-create'),
]
