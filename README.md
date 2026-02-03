## Team Information

Team Name: Jai Satoshi

Team Members:
1. Harsha Vardhan Bonu – 240001020
2. Shashvat Sharma     - 240005043
3. Manjeet Kumar       - 240041027
4. Manish Garasiya     - 240041026 



## To Run the Program
python3 src/main.py
## To Run the test scenarios
python3 tests/test_scenarios.py


## Design Overview
This project uses the UTXO (Unspent Transaction Output) model to simulate Bitcoin transactions. The UTXOManager stores all confirmed UTXOs and represents the blockchain state. The Mempool temporarily stores valid but unconfirmed transactions and prevents double spending by reserving used UTXOs. Transactions are validated by checking UTXO existence, sufficient balance, and double-spending rules. Mining is simulated by confirming transactions from the mempool, updating the UTXO set, and giving transaction fees to the miner. Test scenarios are used to demonstrate double-spending and race attack cases.


## Dependencies and Installation

 
This project is implemented in Python using only the **standard library.**
It runs locally as a command-line application and does not require any external dependencies, blockchain libraries, networking, or real cryptographic implementations.

Python version required: **Python 3.8 or higher**.




