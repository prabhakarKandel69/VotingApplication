from django.urls import path
from .views import (
    VoterCreateView,
    VoterRetrieveView,
    VoterUpdateView,
    VoterDeleteView,
    VoterListView,
    VoterListByUserView
)

urlpatterns = [
    path('voters/', VoterListView.as_view(), name='voter-list'),  # List all voters
    path('voters/user/', VoterListByUserView.as_view(), name='voter-list-by-user'),  # List voters by user ID
    path('voters/create/', VoterCreateView.as_view(), name='voter-create'),  # Create a new voter
    path('voters/<int:pk>/', VoterRetrieveView.as_view(), name='voter-detail'),  # Retrieve a specific voter
    path('voters/<int:pk>/update/', VoterUpdateView.as_view(), name='voter-update'),  # Update a specific voter
    path('voters/<int:pk>/delete/', VoterDeleteView.as_view(), name='voter-delete'),  # Delete a specific voter
]