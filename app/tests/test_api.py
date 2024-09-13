from fastapi.testclient import TestClient
from app.main import app
from app.models import Location, Forecast

client = TestClient(app)


def test_api_basic(test_db, session):
    test_location = [
        Location(id=1, latitude=39.1031, longitude=-84.512),
        Location(id=2, latitude=60.1031, longitude=-10.512),
    ]

    test_data = [
        Forecast(
            temperature=65,
            location_id=1,
            start_time="2024-09-12 17:00:00",
            end_time="2024-09-12 18:00:00",
            added_date="2024-09-12 17:00:00",
        ),
        Forecast(
            temperature=66,
            location_id=1,
            start_time="2024-09-12 17:00:00",
            end_time="2024-09-12 18:00:00",
            added_date="2024-09-12 17:00:00",
        ),
        Forecast(
            temperature=62,
            location_id=1,
            start_time="2024-09-12 17:00:00",
            end_time="2024-09-12 18:00:00",
            added_date="2024-09-12 17:00:00",
        ),
        Forecast(
            temperature=100,
            location_id=2,
            start_time="2024-09-12 17:00:00",
            end_time="2024-09-12 18:00:00",
            added_date="2024-09-12 17:00:00",
        ),
        Forecast(
            temperature=101,
            location_id=2,
            start_time="2024-09-12 17:00:00",
            end_time="2024-09-12 18:00:00",
            added_date="2024-09-12 17:00:00",
        ),
    ]

    session.add_all(test_location)
    session.add_all(test_data)
    session.commit()

    url1 = "/api/temperature?latitude=39.1031&longitude=-84.512&date=2024-09-12&hour=17"
    url2 = "/api/temperature?latitude=39.1031&longitude=-84.512&date=2024-09-12&hour=18"
    url3 = "/api/temperature?latitude=40.1031&longitude=-84.512&date=2024-09-12&hour=18"
    url4 = "/api/temperature?latitude=60.1031&longitude=-10.512&date=2024-09-12&hour=17"

    response1 = client.get(url1)
    response2 = client.get(url2)
    response3 = client.get(url3)
    response4 = client.get(url4)

    expected_response1 = {"min_temp": 62, "max_temp": 66}
    expected_response4 = {"min_temp": 100, "max_temp": 101}

    assert response1.status_code == 200
    assert response1.json() == expected_response1

    assert response2.status_code == 404
    assert response3.status_code == 404

    assert response4.status_code == 200
    assert response4.json() == expected_response4


def test_api_dates(test_db, session):
    test_location = [Location(id=1, latitude=39.1031, longitude=-84.512)]
    test_data = [
        Forecast(
            temperature=60,
            location_id=1,
            start_time="2024-09-13 00:00:00",
            end_time="2024-09-13 01:00:00",
            added_date="2024-09-12 17:00:00",
        ),
        Forecast(
            temperature=65,
            location_id=1,
            start_time="2024-09-12 22:00:00",
            end_time="2024-09-12 23:00:00",
            added_date="2024-09-12 17:00:00",
        ),
        Forecast(
            temperature=70,
            location_id=1,
            start_time="2024-09-12 23:00:00",
            end_time="2024-09-13 00:00:00",
            added_date="2024-09-12 17:00:00",
        ),
        Forecast(
            temperature=75,
            location_id=1,
            start_time="2024-09-13 01:00:00",
            end_time="2024-09-13 02:00:00",
            added_date="2024-09-12 17:00:00",
        ),
    ]

    session.add_all(test_location)
    session.add_all(test_data)
    session.commit()

    url1 = "/api/temperature?latitude=39.1031&longitude=-84.512&date=2024-09-13&hour=1"
    url2 = "/api/temperature?latitude=39.1031&longitude=-84.512&date=2024-09-12&hour=23"
    url3 = "/api/temperature?latitude=39.1031&longitude=-84.512&date=2024-09-12&hour=22"
    url4 = "/api/temperature?latitude=39.1031&longitude=-84.512&date=2024-09-13&hour=0"

    response1 = client.get(url1)
    response2 = client.get(url2)
    response3 = client.get(url3)
    response4 = client.get(url4)

    expected_response1 = {"min_temp": 75, "max_temp": 75}

    expected_response2 = {"min_temp": 70, "max_temp": 70}

    expected_response3 = {"min_temp": 65, "max_temp": 65}

    expected_response4 = {"min_temp": 60, "max_temp": 60}

    assert response1.status_code == 200
    assert response1.json() == expected_response1

    assert response2.status_code == 200
    assert response2.json() == expected_response2

    assert response3.status_code == 200
    assert response3.json() == expected_response3

    assert response4.status_code == 200
    assert response4.json() == expected_response4
