import requests
from unittest.mock import patch
from project import get_exchange_rate, get_movie_details, get_weather_data

def test_get_exchange_rate():
    # Simulate a successful API response
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "result": {"EUR": 0.85}
        }
        
        rate = get_exchange_rate("USD", "EUR", "dummy_key")
        assert rate == 0.85

def test_get_exchange_rate_fail():
    with patch("requests.get") as mock_get:
        mock_get.side_effect = requests.RequestException("Connection Error")        
        rate = get_exchange_rate("USD", "EUR", "dummy_key")
        assert rate is None

def test_get_movie_details():
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "Response": "True",
            "Title": "Inception",
            "Year": "2010",
            "Plot": "Dreams."
        }
        
        data = get_movie_details("Inception", "dummy_key")
        
        assert data["Title"] == "Inception"
        assert data["Year"] == "2010"
        assert data["Plot"] == "Dreams."

def test_get_movie_not_found():
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "Response": "False", 
            "Error": "Movie not found!"
        }
        
        data = get_movie_details("NotAMovie123", "dummy_key")
        
        assert data is None


def test_get_weather_data():
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "current": {
                "temp_c": 22.0,
                "condition": {"text": "Sunny"}
            }
        }
        
        data = get_weather_data("London", "dummy_key")
        
        assert data["temp_c"] == 22.0
        assert data["condition"] == "Sunny"
def test_get_weather_data_fail():
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 404
        mock_get.return_value.raise_for_status.side_effect = requests.RequestException("404 Error")
        
        data = get_weather_data("London", "dummy_key")
        
        assert data is None