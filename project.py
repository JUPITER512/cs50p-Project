import requests
import os
import sys
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

console = Console()
load_dotenv()
def main():
    while True:
        console.clear() 
        display_menu()
        
        choice = console.input("[bold yellow]Select an option (1-3) or 'q' to quit: [/bold yellow]").strip().lower()

        if choice == 'q':
            console.print("[bold green]Goodbye! 👋[/bold green]")
            break

        if choice == '1':
            handle_exchange_rate()
        elif choice == '2':
            handle_movie()
        elif choice == '3':
            handle_weather()
        else:
            console.print("[bold red]Invalid choice, please try again.[/bold red]")
            console.input("[dim]Press Enter to continue...[/dim]")



def display_menu():
    menu_text = Text()
    menu_text.append("1. 💱 Exchange Rate (FastForex)\n", style="bold cyan")
    menu_text.append("2. 🎬 Movie Info (OMDb)\n", style="bold magenta")
    menu_text.append("3. ☁️  Weather (WeatherAPI)", style="bold blue")
    
    console.print(Panel(
        menu_text, 
        title="[bold green]Universal API Tool[/bold green]", 
        subtitle="CS50P Final Project",
        expand=False,
        border_style="blue"
    ))

def print_result_table(title, data_dict, color):
    table = Table(title=title, show_header=True, header_style=f"bold {color}", border_style=color)
    table.add_column("Attribute", style="dim")
    table.add_column("Value", style="bold")

    for key, value in data_dict.items():
        table.add_row(key, str(value))
    
    console.print(table)
    console.input("\n[dim]Press Enter to return to menu...[/dim]")

def handle_exchange_rate():
    api_key = os.getenv("EXCHANGE_RATE_API_KEY")
    if not api_key:
        console.print("[bold red]Error: Missing Exchange Rate API Key[/bold red]")
        return

    console.print("[cyan]--- Currency Converter ---[/cyan]")
    src = console.input("[From Currency (e.g. USD):").strip().upper()
    target = console.input("To Currency (e.g. EUR): ").strip().upper()

    with console.status("[bold green]Fetching rates...[/bold green]"):
        rate = get_exchange_rate(src, target, api_key)
    
    if rate:
        table = Table(title="Exchange Rate", border_style="cyan")
        table.add_column("Source", justify="center")
        table.add_column("Target", justify="center")
        table.add_column("Rate", justify="center")
        table.add_row(src, target, f"{rate}")
        console.print(table)
        console.input("\n[dim]Press Enter to return...[/dim]")
    else:
        console.print("[bold red]Failed to fetch exchange rate.[/bold red]")
        console.input()

def handle_movie():
    api_key = os.getenv("MOVIE_API_KEY")
    if not api_key:
        console.print("[bold red]Error: Missing Movie API Key[/bold red]")
        return

    title = console.input("[magenta]Enter movie title: [/magenta]").strip()
    
    with console.status("[bold magenta]Searching OMDb...[/bold magenta]"):
        movie_data = get_movie_details(title, api_key)
    
    if movie_data:
        # Create a dictionary for the table printer
        display_data = {
            "Title": movie_data['Title'],
            "Year": movie_data['Year'],
            "Plot": movie_data['Plot']
        }
        print_result_table(f"🎬 {movie_data['Title']}", display_data, "magenta")
    else:
        console.print("[bold red]Movie not found.[/bold red]")
        console.input()

def handle_weather():
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        console.print("[bold red]Error: Missing Weather API Key[/bold red]")
        return

    city = console.input("[blue]Enter city name: [/blue]").strip()
    
    with console.status("[bold blue]Checking skies...[/bold blue]"):
        weather = get_weather_data(city, api_key)
    
    if weather:
        display_data = {
            "City": city,
            "Temperature": f"{weather['temp_c']}°C",
            "Condition": weather['condition']
        }
        print_result_table(f"☁️ Weather Report", display_data, "blue")
    else:
        console.print("[bold red]Could not fetch weather data.[/bold red]")
        console.input()

def get_exchange_rate(src, target, api_key):
    url = f"https://api.fastforex.io/fetch-one?from={src}&to={target}&api_key={api_key}"
    headers = {"accept": "application/json"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data["result"][target]
    except (requests.RequestException, KeyError, TypeError):
        return None

def get_movie_details(title, api_key):
    url = f"http://www.omdbapi.com/?t={title}&apikey={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data.get("Response") == "True":
            return {
                "Title": data.get("Title"),
                "Year": data.get("Year"),
                "Plot": data.get("Plot")
            }
        return None
    except requests.RequestException:
        return None

def get_weather_data(city, api_key):
    """Fetches current weather from WeatherAPI.com."""
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return {
            "temp_c": data["current"]["temp_c"],
            "condition": data["current"]["condition"]["text"]
        }
    except (requests.RequestException, KeyError):
        return None

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold red]Program interrupted. Exiting...[/bold red]")
        sys.exit(0)