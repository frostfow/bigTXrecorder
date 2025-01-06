import requests
import time

# Function to fetch unconfirmed transactions from the mempool
def get_mempool():
    url = "https://mempool.space"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching mempool data: {e}")
        return None

# Function to fetch confirmed transactions from the blockchair API
def get_blockchair_transactions():
    url = "https://api.blockchair.com/bitcoin/transactions"
    params = {
        'limit': 10,  # Adjust this as needed for more results
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Blockchair data: {e}")
        return None

# Function to filter transactions based on BTC amount
def filter_transactions(tx_data):
    if not tx_data or 'data' not in tx_data:
        print("No transaction data found.")
        return

    for tx in tx_data['data']:
        try:
            # Debugging: Print the entire transaction to inspect its structure
            print(tx)  # Add this line to see the full transaction data structure
            total_btc = sum(output['value'] for output in tx.get('outputs', [])) / 1e8  # Convert satoshis to BTC
            if total_btc > 20:
                print(f"Transaction Hash: {tx['hash']}")
                print(f"Total BTC: {total_btc}")
                print(f"Inputs: {tx.get('inputs', 'No inputs available')}")
                print(f"Outputs: {tx.get('outputs', 'No outputs available')}")
                print("=" * 50)
        except KeyError as e:
            print(f"Missing expected key in transaction data: {e}")
        except Exception as e:
            print(f"Error processing transaction data: {e}")

def main():
    while True:
        # Fetch mempool transactions (unconfirmed)
        mempool_data = get_mempool()
        if mempool_data:
            print("Checking Mempool Transactions...")
            filter_transactions(mempool_data)

        # Fetch blockchair transactions (confirmed)
        blockchair_data = get_blockchair_transactions()
        if blockchair_data:
            print("Checking Blockchair Transactions...")
            filter_transactions(blockchair_data)

        # Sleep for 30 seconds before the next check
        time.sleep(30)

if __name__ == "__main__":
    main()
