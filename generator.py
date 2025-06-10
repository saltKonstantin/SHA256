from mnemonic import Mnemonic
from bip32utils import BIP32Key
import binascii
import datetime
import requests
import csv
import os
import time

LOG_FILE = "wallet_log.csv"
FOUND_LOG_FILE = "found_wallets.csv"
# Set the number of wallets to generate and check in each batch.
# The blockchain.info API can handle multiple addresses separated by a '|'.
# Batching significantly reduces the number of API calls.
BATCH_SIZE = 50 

def get_balances_for_batch(wallets):
    """
    Checks the balances for a batch of Bitcoin addresses using a single API call.
    """
    if not wallets:
        return {}
    
    addresses = "|".join([w['address'] for w in wallets])
    try:
        url = f"https://blockchain.info/balance?active={addresses}"
        response = requests.get(url, timeout=15) # Increased timeout for larger request
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error querying blockchain.info for batch: {e}")
        return {}
    except ValueError:
        print("Error: Could not decode or parse the API response for batch.")
        return {}

def log_wallet(wallet, log_file):
    """Appends a single wallet's details to the specified CSV log file."""
    file_exists = os.path.isfile(log_file)
    with open(log_file, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "Balance BTC", "Mnemonic", "Private Key (WIF)", "Public Key (hex)", "Address"])

        writer.writerow([
            datetime.datetime.now().isoformat(), 
            wallet['balance'], 
            wallet['mnemonic'], 
            wallet['private_key'], 
            wallet['public_key'], 
            wallet['address']
        ])

def generate_wallet():
    """Generates a single BIP39 mnemonic and derives its keys and address."""
    mnemo = Mnemonic("english")
    words = mnemo.generate(strength=128)
    seed = mnemo.to_seed(words, passphrase="")
    root_key = BIP32Key.fromEntropy(seed)
    child_key = root_key.ChildKey(44 | 0x80000000).ChildKey(0 | 0x80000000).ChildKey(0 | 0x80000000).ChildKey(0).ChildKey(0)

    return {
        "mnemonic": words,
        "private_key": child_key.WalletImportFormat(),
        "public_key": binascii.hexlify(child_key.PublicKey()).decode(),
        "address": child_key.Address(),
        "balance": "N/A" # Default value
    }

if __name__ == "__main__":
    print(f"Starting wallet generator. Using a batch size of {BATCH_SIZE}.")
    print("This script will run indefinitely. Press Ctrl+C to stop.")
    print("Logging all generated wallets to wallet_log.csv.")
    print("Logging any wallets with a balance to found_wallets.csv.")
    print("="*60)
    
    checked_count = 0
    while True:
        # 1. Generate a batch of wallets
        wallets_batch = [generate_wallet() for _ in range(BATCH_SIZE)]
        
        # 2. Check balances for the entire batch in one API call
        print(f"Generated {BATCH_SIZE} wallets. Checking balances...")
        balances_data = get_balances_for_batch(wallets_batch)
        
        # 3. Process and log results for the batch
        if balances_data:
            for wallet in wallets_batch:
                address_data = balances_data.get(wallet['address'])
                if address_data:
                    balance = address_data['final_balance'] / 10**8
                    wallet['balance'] = balance
                    
                    # Log every wallet
                    log_wallet(wallet, LOG_FILE)
                    
                    # If balance is found, log to the special file
                    if balance > 0:
                        print("\n" + "!"*60)
                        print(f"!!! BALANCE FOUND: {balance} BTC !!!")
                        print(f"Address: {wallet['address']}")
                        print("!"*60 + "\n")
                        log_wallet(wallet, FOUND_LOG_FILE)
                else:
                    # Log wallet even if balance check failed for it
                    log_wallet(wallet, LOG_FILE)
        else:
            print("Failed to retrieve balances for the batch. Logging wallets with 'N/A' balance.")
            for wallet in wallets_batch:
                log_wallet(wallet, LOG_FILE)

        checked_count += BATCH_SIZE
        print(f"Batch processed. Total wallets checked: {checked_count}. Waiting for next run...")
        
        # 4. Wait before the next batch to be respectful to the API
        time.sleep(2) # A slightly longer sleep as we are doing more work per cycle