from utxo_manager import UTXOManager
from mempool import Mempool
from transaction import create_transaction
from block import mine_block



# Hard-coded test scenarios for demonstrating double-spending and race attack behavior

def test_double_spend_same_tx(utxo, mempool):
    print("\nTest: Double-spend in SAME transaction")
    print("Alice tries to spend the same UTXO twice")

    tx = create_transaction(
        inputs=[
            {"prev_tx": "genesis", "index": 0, "owner": "Alice"},
            {"prev_tx": "genesis", "index": 0, "owner": "Alice"}  # same UTXO twice
        ],
        outputs=[
            {"amount": 10, "address": "Bob"}
        ]
    )

    success, msg = mempool.add_transaction(tx, utxo)
    print("Result:", msg)


def test_mempool_double_spend(utxo, mempool):
    print("\nTest: Mempool Double-spend")
    print("TX1: Alice -> Bob (spends UTXO)")
    print("TX2: Alice -> Charlie (spends SAME UTXO)")

    tx1 = create_transaction(
        inputs=[
            {"prev_tx": "genesis", "index": 0, "owner": "Alice"}
        ],
        outputs=[
            {"amount": 10, "address": "Bob"}
        ]
    )
    print("TX1:", mempool.add_transaction(tx1, utxo)[1])

    tx2 = create_transaction(
        inputs=[
            {"prev_tx": "genesis", "index": 0, "owner": "Alice"}  # same UTXO
        ],
        outputs=[
            {"amount": 10, "address": "Charlie"}
        ]
    )
    print("TX2:", mempool.add_transaction(tx2, utxo)[1])


def test_race_attack(utxo, mempool):
    print("\nTest: Race Attack (First-Seen Rule)")
    print("Low-fee TX arrives first, High-fee TX arrives second")

    tx_low_fee = create_transaction(
        inputs=[
            {"prev_tx": "genesis", "index": 2, "owner": "Charlie"}
        ],
        outputs=[
            {"amount": 19.999, "address": "Bob"}  # low fee
        ]
    )
    print("Low-fee TX:", mempool.add_transaction(tx_low_fee, utxo)[1])

    tx_high_fee = create_transaction(
        inputs=[
            {"prev_tx": "genesis", "index": 2, "owner": "Charlie"}
        ],
        outputs=[
            {"amount": 19.0, "address": "Alice"}  # higher fee
        ]
    )
    print("High-fee TX:", mempool.add_transaction(tx_high_fee, utxo)[1])

def main():
    utxo = UTXOManager()
    mempool = Mempool()

    # Genesis UTXOs
    genesis = [
        ("genesis", 0, 50.0, "Alice"),
        ("genesis", 1, 30.0, "Bob"),
        ("genesis", 2, 20.0, "Charlie"),
        ("genesis", 3, 10.0, "David"),
        ("genesis", 4, 5.0, "Eve"),
    ]

    for g in genesis:
        utxo.add_utxo(*g)

    while True:
        print(" \n Bitcoin Transaction Simulator ")
        print("1. Create new transaction")
        print("2. View UTXO set")
        print("3. View mempool")
        print("4. Mine block")
        print("5. Run test scenarios")
        print("6. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            sender = input("Sender: ")
            utxos = utxo.get_utxos_for_owner(sender)
            if not utxos:
                print("No UTXOs available")
                continue

            print("Available UTXOs:", utxos)
            prev_tx, index, amount = utxos[0]

            recipient = input("Recipient: ")
            send_amount = float(input("Amount: "))

            outputs = [{"amount": send_amount, "address": recipient}]
            change = amount - send_amount - 0.001
            if change > 0:
                outputs.append({"amount": change, "address": sender})

            tx = create_transaction(
                inputs=[{
                    "prev_tx": prev_tx,
                    "index": index,
                    "owner": sender
                }],
                outputs=outputs
            )

            success, msg = mempool.add_transaction(tx, utxo)
            print(msg)

        elif choice == "2":
            print("\nUTXO SET:")
            for k, v in utxo.utxo_set.items():
                print(k, v)

        elif choice == "3":
            print("\nMEMPOOL:")
            for tx, fee in mempool.transactions:
                print(tx["tx_id"], "fee:", fee)

        elif choice == "4":
            miner = input("Miner name: ")
            fees = mine_block(miner, mempool, utxo)
            print(f"Block mined. Miner earned {fees} BTC")

        elif choice == "5":
            while True:
                print(" \n Test Scenarios ")
                print("1. Double-spend in same transaction")
                print("2. Mempool double-spend")
                print("3. Race attack (first-seen rule)")
                print("4. Back")

                t = input("Select test scenario: ").strip()

                if t == "1":
                    test_double_spend_same_tx(utxo, mempool)

                elif t == "2":
                    test_mempool_double_spend(utxo, mempool)

                elif t == "3":
                    test_race_attack(utxo, mempool)

                elif t == "4":
                    break

                else:
                    print("Invalid choice")

        elif choice == "6":
            break


if __name__ == "__main__":
    main()