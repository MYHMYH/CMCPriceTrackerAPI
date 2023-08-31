
import requests
import threading
import time
from datetime import datetime

# CoinMarketCap API parameters
API_KEY = 'YOUR_CMC_API_KEY'
PRICE_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'

# Global variables to control the display loop and store historical data
stop_display = False
historical_data = {}

# Function to retrieve coin price and historical data
def get_coin_price(coin_symbol):
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': API_KEY
    }

    params = {
        'symbol': coin_symbol
    }

    previous_price = None  # Store the previous price for comparison

    while not stop_display:
        response = requests.get(PRICE_URL, headers=headers, params=params)
        data = response.json()

        if response.status_code == 200:
            coin_data = data.get('data', {}).get(coin_symbol)
            if coin_data:
                current_price = coin_data.get('quote', {}).get('USD', {}).get('price')
                if current_price:
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    if previous_price is None:
                        color = "\033[0m"  # White color for the first price
                    elif current_price < previous_price:
                        color = "\033[91m"  # Red color for lower price
                    elif current_price > previous_price:
                        color = "\033[92m"  # Green color for higher price
                    else:
                        color = "\033[0m"  # Default color for equal price

                    # Format the price to two decimal places
                    formatted_price = "${:.2f}".format(current_price)

                    print(f"{color}Price of {coin_symbol}: {formatted_price} at {timestamp}\033[0m")
                    previous_price = current_price  # Update the previous price

                else:
                    print(f"Price of {coin_symbol} not available")
            else:
                print(f"Coin data for {coin_symbol} not found")
        else:
            print('Error occurred while retrieving coin price')

        time.sleep(5)  # Wait for 5 seconds

# Main function
if __name__ == '__main__':
    while True:
        coin_symbol = input("Enter coin symbol (e.g., BTC, ETH, BNB): ")

        while True:
            # Create and start a separate thread for price display
            display_thread = threading.Thread(target=get_coin_price, args=(coin_symbol.upper(),))
            display_thread.start()

            # Prompt for stopping the display
            input("Press Enter to stop and enter a new coin symbol...")

            # Set the stop_display flag to True to stop the display loop
            stop_display = True

            # Wait for the display thread to complete
            display_thread.join()

            # Reset the stop_display flag for the next iteration
            stop_display = False

            # Prompt for a new coin symbol
            coin_symbol = input("Enter coin symbol (e.g., BTC, ETH, BNB): ")
