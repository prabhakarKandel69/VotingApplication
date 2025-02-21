from rest_framework import serializers
from .models import Voter

class VoterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voter
        fields = '__all__'  # You can also specify fields explicitly, e.g., ['voter_id', 'full_name', ...]
        read_only_fields = ['userid']  # Mark 'userid' as read-only

    def create(self, validated_data):
        # Ensure the 'userid' is automatically set based on the logged-in user
        user = self.context['request'].user  # Access the logged-in user from the request context
        validated_data['userid'] = user  # Assign the 'userid' field to the logged-in user
        return super().create(validated_data)
