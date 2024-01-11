# seeders/seed_data.py
from datetime import datetime
from klachtsysteem.models import Status, Klacht

def seed_status_data():
    # Create Status objects if they don't already exist
    status_data = [
        {'waarde': 'Open', 'beschrijving': 'The complaint is open and not yet resolved.'},
        {'waarde': 'In Progress', 'beschrijving': 'The complaint is currently being addressed.'},
        {'waarde': 'Closed', 'beschrijving': 'The complaint has been resolved and closed.'},
    ]

    for status_info in status_data:
        Status.objects.get_or_create(
            waarde=status_info['waarde'],
            beschrijving=status_info['beschrijving']
        )

def seed_klacht_data():
    # Create Status objects if they don't already exist
    status1, created1 = Status.objects.get_or_create(waarde='Open', beschrijving='The complaint is open and not yet resolved.')
    status2, created2 = Status.objects.get_or_create(waarde='In Progress', beschrijving='The complaint is currently being addressed.')

    # Create multiple Klacht objects
    klachten_data = [
        {
            'naam': 'Test Complaint 1',
            'omschrijving': 'This is a test complaint 1',
            'email': 'test1@example.com',
            'GPS_locatie': 'POINT(0 0)',
            'datum_melding': datetime(2023, 1, 1),
            'status': status1 if created1 else status2
        },
        {
            'naam': 'Test Complaint 2',
            'omschrijving': 'This is a test complaint 2',
            'email': 'test2@example.com',
            'GPS_locatie': 'POINT(1 1)',
            'datum_melding': datetime(2023, 2, 1),
            'status': status2 if created2 else status1
        },
        {
            'naam': 'Test Complaint 3',
            'omschrijving': 'This is a test complaint 3',
            'email': 'test3@example.com',
            'GPS_locatie': 'POINT(0 0)',
            'datum_melding': datetime(2023, 1, 1),
            'status': status1 if created1 else status2
        },
        {
            'naam': 'Test Complaint 4',
            'omschrijving': 'This is a test complaint 4',
            'email': 'test4@example.com',
            'GPS_locatie': 'POINT(1 1)',
            'datum_melding': datetime(2023, 2, 1),
            'status': status2 if created2 else status1
        },
         {
            'naam': 'Test Complaint 5',
            'omschrijving': 'This is a test complaint 5',
            'email': 'test5@example.com',
            'GPS_locatie': 'POINT(0 0)',
            'datum_melding': datetime(2023, 1, 1),
            'status': status1 if created1 else status2
        },
        {
            'naam': 'Test Complaint 6',
            'omschrijving': 'This is a test complaint 6',
            'email': 'test6@example.com',
            'GPS_locatie': 'POINT(1 1)',
            'datum_melding': datetime(2023, 2, 1),
            'status': status2 if created2 else status1
        },
        {
            'naam': 'Test Complaint 7',
            'omschrijving': 'This is a test complaint 7',
            'email': 'test7@example.com',
            'GPS_locatie': 'POINT(1 1)',
            'datum_melding': datetime(2023, 2, 1),
            'status': status2 if created2 else status1
        },
        {
            'naam': 'Test Complaint 8',
            'omschrijving': 'This is a test complaint 8',
            'email': 'test8@example.com',
            'GPS_locatie': 'POINT(0 0)',
            'datum_melding': datetime(2023, 1, 1),
            'status': status1 if created1 else status2
        },
        {
            'naam': 'Test Complaint 9',
            'omschrijving': 'This is a test complaint 9',
            'email': 'test9@example.com',
            'GPS_locatie': 'POINT(1 1)',
            'datum_melding': datetime(2023, 2, 1),
            'status': status2 if created2 else status1
        },
         {
            'naam': 'Test Complaint 10',
            'omschrijving': 'This is a test complaint 10',
            'email': 'test10@example.com',
            'GPS_locatie': 'POINT(0 0)',
            'datum_melding': datetime(2023, 1, 1),
            'status': status1 if created1 else status2
        },
        {
            'naam': 'Test Complaint 11',
            'omschrijving': 'This is a test complaint 11',
            'email': 'test11@example.com',
            'GPS_locatie': 'POINT(1 1)',
            'datum_melding': datetime(2023, 2, 1),
            'status': status2 if created2 else status1
        },
    ]

    for klacht_info in klachten_data:
        Klacht.objects.create(**klacht_info)

if __name__ == "__main__":
    seed_status_data()
    seed_klacht_data()
