# seeders/seed_data.py
from datetime import datetime
import random
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
    # List of more realistic names and descriptions
    names = [
        'John Doe',
        'Alice Smith',
        'Robert Johnson',
        'Emily Davis',
        'Michael Wilson',
        'Sarah Anderson',
        'David Martinez',
        'Jennifer Lee',
        'William Brown',
        'Linda Taylor',
    ]   

    descriptions = [
        'Loud noise from construction site during early morning hours.',
        'Large pothole on the corner of Main Street and Elm Avenue.',
        'Garbage not collected for two weeks in my neighborhood.',
        'Vandalism at the local park with graffiti on benches.',
        'Heavy traffic jam on the highway causing long delays.',
        'Bus delays on Route 101 affecting daily commuters.',
        'Water leak observed on the street near my house.',
        'Streetlight on Maple Street not working for a week.',
        'Requesting maintenance of the city park with overgrown grass.',
        'Illegal parking of vehicles blocking driveways in the area.',
    ]

    # Random GPS locations in Rotterdam
    rotterdam_coordinates = [
        (51.9225, 4.47917),  # Rotterdam Central Station
        (51.9174, 4.4818),   # Erasmus Bridge
        (51.9108, 4.4808),   # Euromast Tower
        (51.9194, 4.4944),   # Markthal
        (51.9277, 4.4818),   # Museum Boijmans Van Beuningen
        (51.9075, 4.4881),   # Diergaarde Blijdorp Zoo
        (51.9116, 4.4795),   # Spido Boat Tour
        (51.9147, 4.4135),   # Kralingse Plas Park
    ]
    # Create Status objects if they don't already exist
    status1, created1 = Status.objects.get_or_create(waarde='Open', beschrijving='The complaint is open and not yet resolved.')
    status2, created2 = Status.objects.get_or_create(waarde='In Progress', beschrijving='The complaint is currently being addressed.')

    # Create multiple Klacht objects
    klachten_data = []
    for i in range(1, 31):
        random_location = random.choice(rotterdam_coordinates)
        month = (i - 1) % 12 + 1  # Cycle through months from 1 to 12
        klacht = {
            'naam': random.choice(names),
            'omschrijving': random.choice(descriptions),
            'email': f'test{i}@example.com',
            'GPS_locatie': f'POINT({random_location[1]} {random_location[0]})',
            'datum_melding': datetime(2023, month, i),
            'status': status1 if i % 2 == 1 else status2,  # Alternate status
        }
        klachten_data.append(klacht)

    for klacht_info in klachten_data:
        Klacht.objects.create(**klacht_info)

if __name__ == "__main__":
    seed_status_data()
    seed_klacht_data()
