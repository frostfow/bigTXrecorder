import requests
import time

# Replace with the wallet address you want to track
WALLET_ADDRESS = '36ZF5foUhdvma5RrnRr1bu6RtjoUsi6Phg'  # Example Bitcoin address

# Blockchain.com API URL to get transactions of a specific wallet
API_URL = f'https://blockchain.info/rawaddr/36ZF5foUhdvma5RrnRr1bu6RtjoUsi6Phg'

# To keep track of previously fetched transactions
seen_transactions = set()

def get_wallet_transactions():
    """Fetch live transactions for the given Bitcoin wallet"""
    try:
        response = requests.get(API_URL)
        data = response.json()

        if 'txs' in data:
            # Display the latest transactions
            transactions = data['txs']
            new_transactions = [tx for tx in transactions if tx['hash'] not in seen_transactions]

            if new_transactions:
                for tx in new_transactions:
                    print(f"Hash: {tx['hash']}")
                    print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(tx['time']))}")
                    print(f"Total Sent: {tx['out'][0]['value'] / 100000000} BTC")
                    print(f"Total Received: {sum(output['value'] for output in tx['out']) / 100000000} BTC")
                    print("-" * 40)

                # Update the seen_transactions set with the new transactions
                for tx in new_transactions:
                    seen_transactions.add(tx['hash'])
            else:
                print("No new transactions.")
        else:
            print("No transactions found for this address.")
    except Exception as e:
        print(f"Error fetching data: {str(e)}")

# Run the script to get transactions
while True:
    get_wallet_transactions()
    time.sleep(60)  # Delay for 1 minute before fetching again

