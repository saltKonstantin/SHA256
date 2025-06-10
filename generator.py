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

def get_address_balance(address):
    """
    Checks the balance of a given Bitcoin address using the blockchain.info API.
    """
    try:
        url = f"https://blockchain.info/balance?active={address}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        balance = data[address]['final_balance']
        return balance / 10**8  # Convert from satoshis to BTC
    except requests.exceptions.RequestException as e:
        print(f"Error querying blockchain.info: {e}")
        return None
    except (ValueError, KeyError):
        print("Error: Could not decode or parse the API response.")
        return None

def log_credentials(mnemonic, private_key, public_key, address, balance, log_file):
    """Appends generated credentials and balance to the specified CSV log file."""
    file_exists = os.path.isfile(log_file)
    with open(log_file, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "Balance BTC", "Mnemonic", "Private Key (WIF)", "Public Key (hex)", "Address"])

        writer.writerow([datetime.datetime.now().isoformat(), balance, mnemonic, private_key, public_key, address])

def generate_keys_from_mnemonic():
    """
    Generates a 12-word BIP39 mnemonic, and from it, derives a Bitcoin
    private key, public key, and address.
    """
    # Initialize the Mnemonic object in English
    mnemo = Mnemonic("english")

    # Generate a 12-word mnemonic
    words = mnemo.generate(strength=128)
    print(f"Generated 12-word Mnemonic: {words}")
    print("-" * 30)

    # Generate the seed from the mnemonic. An empty passphrase is used.
    seed = mnemo.to_seed(words, passphrase="")

    # Generate the master key from the seed
    root_key = BIP32Key.fromEntropy(seed)

    # Derive the first account's keys using a standard BIP44 path
    # m/44'/0'/0'/0/0
    child_key = root_key.ChildKey(44 | 0x80000000).ChildKey(0 | 0x80000000).ChildKey(0 | 0x80000000).ChildKey(0).ChildKey(0)

    # Get the private key, public key, and address
    private_key_wif = child_key.WalletImportFormat()
    public_key_hex = binascii.hexlify(child_key.PublicKey()).decode()
    address = child_key.Address()

    print(f"Private Key (WIF): {private_key_wif}")
    print(f"Public Key (hex): {public_key_hex}")
    print(f"Address: {address}")

    # Check the balance of the address
    print("\nQuerying blockchain for balance...")
    balance = get_address_balance(address)
    balance_to_log = balance if balance is not None else "N/A"

    if balance is not None:
        print(f"Balance: {balance} BTC")
        if balance > 0:
            print("\n!!! BALANCE FOUND! SAVING TO SEPARATE LOG FILE !!!\n")
            log_credentials(words, private_key_wif, public_key_hex, address, balance_to_log, FOUND_LOG_FILE)
    else:
        print("Could not retrieve the balance.")

    # Log the credentials
    log_credentials(words, private_key_wif, public_key_hex, address, balance_to_log, LOG_FILE)
    print(f"\nCredentials saved to {LOG_FILE}")

    print("\nNOTE: The mnemonic is generated from the standard BIP39 wordlist.")
    print("A newly generated address will almost always have a balance of 0 BTC.")
    print("The 'word-list.js' file in this project contains this standard list.")


if __name__ == "__main__":
    while True:
        generate_keys_from_mnemonic()
        print("\n" + "="*40)
        print("Waiting for 0.5 seconds before next run...")
        print("="*40 + "\n")
        time.sleep(0.5)