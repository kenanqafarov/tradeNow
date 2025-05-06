from binance.client import Client
import matplotlib.pyplot as plt
from colorama import Fore, Style, init
import datetime
import sys

init(autoreset=True)

api_key = ''
api_secret = ''
client = Client(api_key, api_secret)

symbols = {
    "1": "BTCUSDT",
    "2": "ETHUSDT",
    "3": "DOGEUSDT",
    "4": "BNBUSDT"
}

intervals = {
    "1": ("1m", "Per Minute"),
    "2": ("1h", "Per Hour"),
    "3": ("1d", "Per Day")
}

def print_menu():
    print(Fore.CYAN + "\n=== Crypto Price Viewer ===")
    print(Fore.YELLOW + "Select a cryptocurrency to analyze:\n")
    for key, symbol in symbols.items():
        print(Fore.GREEN + f"{key}. {symbol[:-4]}")
    print(Fore.RED + "0. Exit")

def print_interval_menu():
    print(Fore.YELLOW + "\nSelect a time interval:\n")
    for key, (interval, label) in intervals.items():
        print(Fore.GREEN + f"{key}. {label}")
    print(Fore.RED + "0. Back")

def get_and_plot_data(symbol, interval_code):
    klines = client.get_klines(symbol=symbol, interval=interval_code, limit=50)
    dates = [datetime.datetime.fromtimestamp(int(k[0])/1000) for k in klines]
    closes = [float(k[4]) for k in klines]
    highs = [float(k[2]) for k in klines]
    lows = [float(k[3]) for k in klines]

    plt.figure(figsize=(12, 6))
    plt.plot(dates, closes, label='Close Price', color='blue')
    plt.fill_between(dates, lows, highs, color='lightgray', alpha=0.3, label='High-Low Range')
    plt.title(f'{symbol} - Last {len(closes)} Candles ({interval_code})')
    plt.xlabel('Time')
    plt.ylabel('Price (USDT)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

while True:
    print_menu()
    choice = input(Fore.WHITE + "\nEnter your crypto choice (0-4): ").strip()

    if choice == "0":
        print(Fore.MAGENTA + "Exiting... Goodbye!")
        sys.exit()
    elif choice in symbols:
        symbol = symbols[choice]
        while True:
            print_interval_menu()
            interval_choice = input(Fore.WHITE + "\nEnter interval choice (0-3): ").strip()
            if interval_choice == "0":
                break
            elif interval_choice in intervals:
                interval_code, label = intervals[interval_choice]
                print(Fore.CYAN + f"\nFetching {label} data for {symbol}...\n")
                try:
                    get_and_plot_data(symbol, interval_code)
                except Exception as e:
                    print(Fore.RED + f"Error: {e}")
            else:
                print(Fore.RED + "Invalid interval. Please try again.")
    else:
        print(Fore.RED + "Invalid crypto choice. Please try again.")
