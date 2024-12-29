import requests
import json

def test_get_root():
    print("Testing GET /")
    response = requests.get("http://localhost:1337/")
    print("Status Code:", response.status_code)
    print("Response:", response.text)


def test_get_timezone():
    print("Testing GET /<timezone>")
    valid_tz = "Asia/Bangkok"
    invalid_tz = "Invalid/Timezone"

    # Valid timezone
    response = requests.get(f"http://localhost:1337/{valid_tz}")
    print("Status Code (valid):", response.status_code)
    print("Response (valid):", response.text)

    # Invalid timezone
    response = requests.get(f"http://localhost:1337/{invalid_tz}")
    print("Status Code (invalid):", response.status_code)
    print("Response (invalid):", response.text)


def test_post_time():
    print("Testing POST /api/v1/time")
    payload = {"tz": "America/New_York"}
    
    response = requests.post("http://localhost:1337/api/v1/time", data=json.dumps(payload))
    print("Status Code:", response.status_code)
    print("Response:", response.json())


def test_post_date():
    print("Testing POST /api/v1/date")
    payload = {"tz": "Europe/London"}
    response = requests.post("http://localhost:1337/api/v1/date", data=json.dumps(payload))
    print("Status Code:", response.status_code)
    print("Response:", response.json())


def test_post_datediff():
    print("Testing POST /api/v1/datediff")

    payload = {
        "start": {"date": "2024-12-01 12:00:00", "tz": "UTC"},
        "end": {"date": "2024-12-02 12:00:00", "tz": "UTC"}
    }
    response = requests.post("http://localhost:1337/api/v1/datediff", data=json.dumps(payload))
    print("Status Code:", response.status_code)
    print("Response:", response.json())

    # Invalid date format
    invalid_payload = {
        "start": {"date": "2024/12/01", "tz": "UTC"},
        "end": {"date": "2024-12-02", "tz": "UTC"}
    }
    response = requests.post("http://localhost:1337/api/v1/datediff", data=json.dumps(invalid_payload))
    print("Status Code (invalid):", response.status_code)
    print("Response (invalid):", response.json())


def run_tests():
    test_get_root()
    print()

    test_get_timezone()
    print()

    test_post_time()
    print()

    test_post_date()
    print()

    test_post_datediff()
    print()

if __name__ == "__main__":
    run_tests()
