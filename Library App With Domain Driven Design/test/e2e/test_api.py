import requests

API_URL = "http://127.0.0.1:5000"


def test_add_member():
    url = f"{API_URL}/add_member"
    data = {"name": "John Doe"}
    response = requests.post(url, json=data)

    assert response.status_code == 201
    assert "member_id" in response.json()


def test_add_book():
    url = f"{API_URL}/add_book"
    data = {"name": "Sample Book"}
    response = requests.post(url, json=data)

    assert response.status_code == 201
    assert "book_id" in response.json()


if __name__ == "__main__":
    test_add_member()
    test_add_book()
    print("All tests passed!")
