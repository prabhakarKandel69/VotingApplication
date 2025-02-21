from rest_framework import serializers
from .models import Candidate

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['candidate_id', 'full_name', 'middle_name', 'last_name', 'party', 'position']  # Ensure these fields exist in your model
