import requests
from bip_utils import (
    Bip39MnemonicGenerator, Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes,
)

def get_address_balance(address):
    """
    Checks the balance of a given Bitcoin address using the blockchain.info API.
    """
    try:
        url = f"https://blockchain.info/rawaddr/{address}"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        balance = data.get("final_balance", 0)
        return balance / 10**8  # Convert from satoshis to BTC
    except requests.exceptions.RequestException as e:
        print(f"Error querying blockchain.info: {e}")
        return None
    except ValueError:
        # Handles cases where the response is not valid JSON
        print("Error: Could not decode JSON from the API response.")
        return None

def main():
    """
    Generates a BIP-39 mnemonic, derives a Bitcoin address, and checks its balance.
    """
    # Generate a 12-word mnemonic
    mnemonic = Bip39MnemonicGenerator().FromWordsNumber(12)
    print(f"Generated 12-word Mnemonic: {mnemonic}")
    print("-" * 30)

    # Generate seed from mnemonic
    seed_bytes = Bip39SeedGenerator(mnemonic).Generate()

    # Create a BIP44 object for Bitcoin mainnet
    bip44_mst_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.BITCOIN)

    # Derive the account 0, change 0, address 0 path (m/44'/0'/0'/0/0)
    # This is a standard derivation path for P2PKH addresses
    bip44_acc_ctx = bip44_mst_ctx.Purpose().Coin().Account(0)
    bip44_chg_ctx = bip44_acc_ctx.Change(Bip44Changes.CHAIN_EXT)
    bip44_addr_ctx = bip44_chg_ctx.AddressIndex(0)

    # Get the address
    address = bip44_addr_ctx.PublicKey().ToAddress()
    print(f"Derived Bitcoin Address: {address}")

    # Check the balance of the address
    print("\nQuerying blockchain for balance...")
    balance = get_address_balance(address)

    if balance is not None:
        print(f"Balance: {balance} BTC")
    else:
        print("Could not retrieve the balance.")
    
    print("\nNOTE: A newly generated address will always have a balance of 0 BTC.")


if __name__ == "__main__":
    main() 