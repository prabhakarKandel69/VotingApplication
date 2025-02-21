from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from .models import Vote
from .serializers import VoteSerializer, VoteCreateSerializer
from voters.models import Voter
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from candidate.models import Candidate

class VoteViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the CRUD operations for the Vote model.
    Automatically handles: List, Create, Retrieve, Update, Delete.
    """
    queryset = Vote.objects.all()  # Retrieve all Vote instances.
    permission_classes = [IsAuthenticated]  # Only allow authenticated users to interact with the API.

    def get_serializer_class(self):
        """
        Return the appropriate serializer class based on the HTTP method.
        Use VoteCreateSerializer for POST requests (creating votes).
        Use VoteSerializer for other requests (GET, PUT, PATCH, DELETE).
        """
        if self.request.method == 'POST':
            return VoteCreateSerializer  # For creating a vote
        return VoteSerializer  # For listing, retrieving, updating, deleting votes

    def perform_create(self, serializer):
        """
        Automatically associate the logged-in user with the vote when creating it.
        """
        user = self.request.user
        
        try:
            # Retrieve the Voter instance associated with the User
            voter = Voter.objects.get(userid=user)  # Assuming 'userid' is the ForeignKey in Voter
        except Voter.DoesNotExist:
            raise ValidationError("You must be a registered voter to vote.")

        # Save the vote instance with the Voter instance
        serializer.save(voter=voter)  # Save the vote instance with the current Voter instance
    

    #votes/winner
    @action(detail=False, methods=['get'], url_path='top-winners')
    def get_top_winners(self, request):
        """
        Returns the top 3 candidates with the most votes.
        """
        # Aggregate votes for each candidate
        vote_counts = Vote.objects.values('candidate__id', 'candidate__name').annotate(total_votes=Count('candidate')).order_by('-total_votes')[:3]

        if not vote_counts:
            return Response({"message": "No votes have been cast yet."})

        return Response({
            "top_winners": [
                {
                    "candidate_id": winner['candidate__id'],
                    "candidate_name": winner['candidate__name'],
                    "total_votes": winner['total_votes']
                }
                for winner in vote_counts
            ]
        })
