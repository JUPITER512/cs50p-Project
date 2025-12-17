# Universal API Tool
#### Video Demo:  <URL_HERE>

## Description
The **Universal API Tool** is a command-line interface (CLI) application developed as my final project for CS50P. It serves as an "all-in-one" utility dashboard that allows users to fetch real-time data from three distinct external services without leaving their terminal.

The motivation behind this project was to master the interaction between Python and RESTful APIs, specifically focusing on handling JSON data, managing environment variables securely, and creating a user-friendly terminal experience using external libraries.

### Features
The application features a menu-driven interface with three main modes:
1.  **Currency Converter:** Connects to the **FastForex API** to calculate real-time exchange rates between any two world currencies.
2.  **Movie Database:** Connects to the **OMDb API** to fetch metadata (Release Year, Plot Summary, etc.) for any movie title.
3.  **Weather Station:** Connects to **WeatherAPI** to retrieve current temperature and weather conditions for any city globally.

## Project Structure & Design Choices

The project is structured to ensure separation of concerns, testability, and a clean user interface.

### `project.py`
This is the main entry point of the application. I chose to separate the **User Interface (UI)** logic from the **Data Fetching** logic.
* **UI Logic:** Functions like `handle_weather()` or `display_menu()` use the `rich` library to render beautiful tables, panels, and loading spinners. This ensures the user has a modern experience.
* **Core Logic:** Functions like `get_weather_data()` are "pure" functions. They take arguments (city, API key) and return a dictionary. They do *not* print anything. This design choice was crucial for testing (see below).

### `test_project.py`
This file contains the test suite. Because my project relies on external APIs (which might be down or rate-limited), I could not simply call the real functions in my tests.
* **Mocking:** I utilized `unittest.mock.patch` to "mock" the `requests.get` calls. This allows me to simulate API responses (both success and failure) without requiring an internet connection. This ensures the tests are deterministic and fast.

### `requirements.txt`
Dependencies are managed here to ensure reproducibility.
* `requests`: For handling HTTP GET requests.
* `rich`: To render colored text, tables, and spinners in the terminal.
* `python-dotenv`: To securely load API keys from a `.env` file, keeping secrets out of the source code.
* `pytest`: For running the unit tests.

## Installation & Usage

1.  **Clone the repository:**
    ```bash
    git clone <YOUR_REPO_URL>
    cd project
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure API Keys:**
    Create a file named `.env` in the root directory. You will need free API keys from [FastForex](https://fastforex.io/), [OMDb](http://www.omdbapi.com/), and [WeatherAPI](https://www.weatherapi.com/).
    Add them to the file like this:
    ```text
    EXCHANGE_RATE_API_KEY=your_key_here
    MOVIE_API_KEY=your_key_here
    WEATHER_API_KEY=your_key_here
    ```

4.  **Run the application:**
    ```bash
    python project.py
    ```

## Testing

To run the test suite and verify logic:
```bash
pytest test_project.py