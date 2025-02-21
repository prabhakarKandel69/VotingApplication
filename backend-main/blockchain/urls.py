from django.urls import path
from .views import sync_candidates, sync_voters, vote

urlpatterns = [
    path('sync-candidates/', sync_candidates, name='sync_candidates'),
    path('sync-voters/', sync_voters, name='sync_voters'),
    path('vote/', vote, name='vote'),
]
