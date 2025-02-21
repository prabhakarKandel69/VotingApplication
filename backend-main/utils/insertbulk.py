from voters.models import Voter
from django.core.exceptions import ValidationError

def insert_voters():
    voters_data = [
        ('PUSHPA', 'NULL', 'BASKOTA', 'Gulmi', 'Kritipur', 25, '1999-05-20', None, 'A +ve'),
        ('ROHISA', 'NULL', 'GIRI', 'DANG', 'SANEPA', 24, '2000-01-10', None, 'AB +ve'),
        ('kHOSILA', 'NULL', 'GYAWALI', 'POKHARA', 'KRITIPUR', 23, '2001-04-11', None, 'A +ve'),
        ('RAJESH', 'NULL', 'SHARMA', 'KATHMANDU', 'LALITPUR', 28, '1995-08-14', None, 'B +ve'),
        ('SITA', 'DEVI', 'BHANDARI', 'BIRATNAGAR', 'ITAHARI', 30, '1993-01-20', None, 'O -ve'),
        ('RAM', 'PRASAD', 'DAHAL', 'BUTWAL', 'CHITWAN', 26, '1997-06-25', None, 'AB +ve'),
        ('LAXMI', 'NULL', 'PANTA', 'JANAKPUR', 'DHARAN', 22, '2001-12-09', None, 'O +ve'),
        ('AMIT', 'KUMAR', 'JOSHI', 'DAMAK', 'BIRTAMOD', 24, '1999-05-15', None, 'B -ve'),
        ('SUNITA', 'NULL', 'BARAL', 'DHULIKHEL', 'KAVREPALANCHOK', 21, '2002-03-18', None, 'A -ve'),
        ('BISHAL', 'RAJ', 'KHADKA', 'NEPALGUNJ', 'TANAHUN', 29, '1994-07-10', None, 'AB -ve'),
        ('PRATIMA', 'KUMARI', 'RANA', 'DAMAK', 'DHANKUTA', 25, '1998-02-28', None, 'A +ve'),
       
    ]

    # Prepare a list of Voter objects
    voter_list = []
    for first_name, middle_name, last_name, permanent_address, temporary_address, age, dob, contact_number, blood_group in voters_data:
        voter = Voter(
            first_name=first_name,
            middle_name=None if middle_name == 'NULL' else middle_name,
            last_name=last_name,
            permanent_address=permanent_address,
            temporary_address=temporary_address,
            age=age,
            dob=dob,
            contact_number=contact_number,
            blood_group=blood_group
        )
        voter_list.append(voter)

    # Bulk create voters
    try:
        Voter.objects.bulk_create(voter_list)
        print(f"{len(voter_list)} records have been successfully inserted into the database.")
    except ValidationError as e:
        print(f"Error inserting records: {e}")

# Call the insert_voters function
if __name__ == "__main__":
    insert_voters()