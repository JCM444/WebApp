from datetime import datetime

FAKE_SESSIONS=[
    {
        "id": 1,
        "title": "Python: Schleifen und Funktionen",
        "module": "Programmierung",
        "date": datetime(2026, 11, 26, 10, 0),
        "location": "B 1.55 HWR Schöneberg",
        "max_participants": 5,
    },
    {
        "id": 2,
        "title": "Python: Schleifen und Funktionen",
        "module": "Programmierung",
        "date": datetime(2026, 11, 26, 10, 0),
        "location": "B 1.55 HWR Schöneberg",
        "max_participants": 5,

    },
    {
        "id": 3,
        "title": "Python: Schleifen und Funktionen",
        "module": "Programmierung",
        "date": datetime(2026, 11, 26, 10, 0),
        "location": "B 1.55 HWR Schöneberg",
        "max_participants": 5,

    },
    ]

def get_all_sessions():
    return FAKE_SESSIONS