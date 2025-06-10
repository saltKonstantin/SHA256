# Bitcoin Wallet Generator and Balance Scanner

This project contains a Python script that continuously generates random 12-word BIP-39 mnemonic phrases, derives the corresponding Bitcoin address and keys, and checks the address balance on the blockchain.

## Features

-   **Continuous & Efficient Operation**: The script runs in an infinite loop, generating and checking wallets 24/7. It uses a **batching system** to check multiple wallet balances in a single API call, significantly increasing efficiency and reducing network overhead.
-   **Batch Processing**: Generates a configurable number of wallets (default is 50) and queries the `blockchain.info` API for all of them at once. This is much faster and more respectful to the API than checking one at a time.
-   **Dual CSV Logging**:
    -   All generated wallets are logged to `wallet_log.csv`.
    -   Any wallet discovered with a balance greater than zero is logged to a separate `found_wallets.csv` file for easy identification.

**Disclaimer:** The probability of generating a wallet with a non-zero balance is astronomically low. This tool is for educational and experimental purposes only.

## How to Use

### 1. Installation

First, make sure you have Python installed. Then, clone the repository and install the necessary dependencies:

```bash
git clone https://github.com/your-username/your-repository.git
cd your-repository
pip install -r requirements.txt
```

### 2. Running the Generator

To start the wallet generation and scanning process, run the `generator.py` script:

```bash
python generator.py
```

The script will print its progress to the console and create/update the log files.

### 3. Stopping the Script

Since the script runs in an infinite loop, you need to manually stop it.

-   **On Windows (PowerShell/CMD):**
    1.  Press `Ctrl + C` in the terminal where the script is running.
    2.  If that doesn't work, open a new PowerShell and find the script's Process ID (PID):
        ```powershell
        Get-Process | findstr "python"
        ```
    3.  Then, terminate the process using its ID:
        ```powershell
        Stop-Process -Id <PID>
        ```
-   **On macOS / Linux:**
    1.  Press `Ctrl + C`.
    2.  If needed, find the PID:
        ```bash
        ps aux | grep "python generator.py"
        ```
    3.  And kill the process:
        ```bash
        kill <PID>
        ```

## Bruteforce Checker

There is an additional script, `bruteforce_checker.py`, which iterates through the entire BIP-39 wordlist and checks the balance of mnemonics created by repeating each word 12 times (e.g., "abandon abandon abandon...").

-   It logs every single check to `bruteforce_all_checks.csv`.
-   It logs any wallet with a balance to `bruteforce_found.csv`.

To run it:
```bash
python bruteforce_checker.py
```
