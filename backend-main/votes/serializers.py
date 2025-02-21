# serializers.py

from rest_framework import serializers
from .models import Vote
from voters.models import Voter  # Import the Voter model

# Serializer for the Vote model
class VoteSerializer(serializers.ModelSerializer):
    voter = serializers.StringRelatedField()  # Serialize the related Voter
    candidate = serializers.StringRelatedField()  # Serialize the related Candidate

    class Meta:
        model = Vote
        fields = ['vote_id', 'voter', 'candidate']

# Serializer for creating a new vote
class VoteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['candidate']  # The fields required for vote creation

    def validate(self, attrs):
        # Get the user associated with the logged-in user
        user = self.context['request'].user
        
        # Retrieve the Voter instance associated with the User
        try:
            voter = Voter.objects.get(userid=user)  # Assuming 'userid' is the ForeignKey in Voter
        except Voter.DoesNotExist:
            raise serializers.ValidationError("You must be a registered voter to vote.")

        candidate = attrs.get('candidate')
        if Vote.objects.filter(voter=voter, candidate=candidate).exists():
            raise serializers.ValidationError("You have already voted for this candidate.")
        
        # Store the voter in the context for use in the create method
        attrs['voter'] = voter
        return attrs

    def create(self, validated_data):
        # Extract the candidate and voter from validated_data
        candidate = validated_data.pop('candidate')
        voter = validated_data.pop('voter')  # Get the voter from validated_data
        return Vote.objects.create(voter=voter, candidate=candidate)