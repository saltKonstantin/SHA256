# Bitcoin Wallet Generator and Balance Scanner

This project contains a Python script that continuously generates random 12-word BIP-39 mnemonic phrases, derives the corresponding Bitcoin address and keys, and checks the address balance on the blockchain.

## Features

-   **Continuous & Efficient Operation**: The script runs in an infinite loop, generating and checking wallets 24/7. It uses a **batching system** to check multiple wallet balances in a single API call, significantly increasing efficiency and reducing network overhead.
-   **Batch Processing**: Generates a configurable number of wallets (default is 50) and queries the `blockchain.info` API for all of them at once. This is much faster and more respectful to the API than checking one at a time.
-   **Dual CSV Logging**:
    -   All generated wallets are logged to `wallet_log.csv`.
    -   Any wallet discovered with a balance greater than zero is logged to a separate `found_wallets.csv` file for easy identification.