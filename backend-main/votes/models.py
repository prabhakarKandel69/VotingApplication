from django.db import models
from voters.models import Voter
from candidate.models import Candidate

# Create your models here.
class Vote(models.Model):
    vote_id = models.AutoField(primary_key=True)  # Equivalent to INTEGER PRIMARY KEY in SQL.
    voter = models.ForeignKey(
        Voter,
        on_delete=models.CASCADE,  # Ensures votes are deleted if the voter is deleted.
        related_name="votes"
    )
    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,  # Ensures votes are deleted if the candidate is deleted.
        related_name="votes"
    )
    
    

    class Meta:
        db_table = "Votes"  # Matches the table name in the SQL.
        unique_together = ("voter", "candidate")  # Optional: Ensures a voter cannot vote for the same candidate more than once.

    def __str__(self):
        return f"VoteID: {self.vote_id}, Voter: {self.voter_id}, Candidate: {self.candidate_id}"
