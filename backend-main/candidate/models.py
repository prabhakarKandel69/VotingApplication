from django.db import models

class Candidate(models.Model):
    candidate_id = models.AutoField(primary_key=True)  # AutoField is used for auto-incrementing IDs
    full_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)  # blank=True allows middle_name to be optional
    last_name = models.CharField(max_length=50)
    party = models.CharField(max_length=50)
    position = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.full_name} ({self.party})'
