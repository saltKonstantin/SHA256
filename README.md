# Bitcoin Wallet Generator and Balance Scanner

This project contains a Python script that continuously generates random 12-word BIP-39 mnemonic phrases, derives the corresponding Bitcoin address and keys, and checks the address balance on the blockchain.

## Features

-   **Continuous Operation**: The script runs in an infinite loop to continuously generate and check new wallets.
-   **Balance Checking**: Uses the `blockchain.info` public API to check the balance of each generated Bitcoin address.
-   **Dual CSV Logging**:
    -   All generated wallets are logged to `wallet_log.csv`.
    -   Any wallet discovered with a balance greater than zero is logged to a separate `found_wallets.csv` file for easy identification.
-   **Efficient Logging**: Uses CSV format for structured and efficient data logging.

**Disclaimer:** The probability of generating a wallet with a non-zero balance is astronomically low. This tool is for educational and experimental purposes only.

## How to Use

### 1. Installation

First, make sure you have Python installed. Then, clone the repository and install the necessary dependencies:

```bash
git clone <repository_url>
cd <repository_name>
pip install -r requirements.txt
```

### 2. Running the Script

To start the wallet generation and scanning process, run the `generator.py` script:

```bash
python generator.py
```
