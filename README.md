# SHA256 Hasher

This repository contains a simple Python script to calculate the SHA256 hash of a user's input.

## How to use

1.  Make sure you have Python installed.
2.  Run the script from your terminal:
    ```
    python sha256_hasher.py
    ```
3.  Enter the data you want to hash when prompted.

## BIP Word Hasher

This script selects 12 random words from the BIP-39 wordlist (`2048_BIP_39_words.csv`), combines them, and outputs the SHA256 hash of the combined string.

### How to use

1.  Make sure you have `2048_BIP_39_words.csv` in the same directory.
2.  Run the script from your terminal:
    ```
    python bip_word_hasher.py
    ```

## Bitcoin Balance Checker

This script generates a new, random 12-word BIP-39 mnemonic phrase, derives the corresponding Bitcoin address (P2PKH), and checks its balance using a public blockchain explorer API.

**IMPORTANT:** This script generates a new address each time it is run. The balance of a newly generated address will always be zero.

### How to use

1.  Install the required Python packages:
    ```
    pip install -r requirements.txt
    ```
2.  Run the script from your terminal:
    ```
    python btc_balance_checker.py
    ```