import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from utxo_manager import UTXOManager
from mempool import Mempool
from transaction import create_transaction
from block import mine_block


FEE = 0.001


def setup_genesis():
    utxo = UTXOManager()
    mempool = Mempool()

    utxo.add_utxo("genesis", 0, 50.0, "Alice")
    utxo.add_utxo("genesis", 1, 30.0, "Bob")
    utxo.add_utxo("genesis", 2, 20.0, "Charlie")
    utxo.add_utxo("genesis", 3, 10.0, "David")
    utxo.add_utxo("genesis", 4, 5.0, "Eve")

    return utxo, mempool



def test_1_basic_valid_transaction():
    print("\nTEST 1: Basic Valid Transaction")
    utxo, mempool = setup_genesis()

    tx = create_transaction(
        inputs=[
            {"prev_tx": "genesis", "index": 0, "owner": "Alice"}  # 50 BTC
        ],
        outputs=[
            {"amount": 10.0, "address": "Bob"},
            {"amount": 50.0 - 10.0 - FEE, "address": "Alice"}  # change
        ]
    )

    print(mempool.add_transaction(tx, utxo))




def test_2_multiple_inputs():
    print("\nTEST 2: Multiple Inputs")
    utxo, mempool = setup_genesis()

    tx = create_transaction(
        inputs=[
            {"prev_tx": "genesis", "index": 0, "owner": "Alice"},    # 50
            {"prev_tx": "genesis", "index": 2, "owner": "Charlie"}  # 20
        ],
        outputs=[
            {"amount": 60.0, "address": "Bob"},
            {"amount": 70.0 - 60.0 - FEE, "address": "Alice"}  # change
        ]
    )

    print(mempool.add_transaction(tx, utxo))

"""Double spending is prevented using a synchronized UTXOManager and mempool.  """""

def test_3_double_spend_same_transaction():
    print("\nTEST 3: Double-Spend in Same Transaction")
    utxo, mempool = setup_genesis()

    tx = create_transaction(
        inputs=[
            {"prev_tx": "genesis", "index": 0, "owner": "Alice"},
            {"prev_tx": "genesis", "index": 0, "owner": "Alice"}
        ],
        outputs=[
            {"amount": 10.0, "address": "Bob"}
        ]
    )

    print(mempool.add_transaction(tx, utxo))



def test_4_mempool_double_spend():
    print("\nTEST 4: Mempool Double-Spend")
    utxo, mempool = setup_genesis()

    tx1 = create_transaction(
        inputs=[{"prev_tx": "genesis", "index": 0, "owner": "Alice"}],
        outputs=[
            {"amount": 10.0, "address": "Bob"},
            {"amount": 50.0 - 10.0 - FEE, "address": "Alice"}
        ]
    )

    tx2 = create_transaction(
        inputs=[{"prev_tx": "genesis", "index": 0, "owner": "Alice"}],
        outputs=[
            {"amount": 10.0, "address": "Charlie"},
            {"amount": 50.0 - 10.0 - FEE, "address": "Alice"}
        ]
    )

    print("TX1:", mempool.add_transaction(tx1, utxo))
    print("TX2:", mempool.add_transaction(tx2, utxo))



def test_5_insufficient_funds():
    print("\nTEST 5: Insufficient Funds")
    utxo, mempool = setup_genesis()

    tx = create_transaction(
        inputs=[{"prev_tx": "genesis", "index": 1, "owner": "Bob"}],  # 30 BTC
        outputs=[
            {"amount": 35.0, "address": "Alice"}
        ]
    )

    print(mempool.add_transaction(tx, utxo))



def test_6_negative_amount():
    print("\nTEST 6: Negative Amount")
    utxo, mempool = setup_genesis()

    tx = create_transaction(
        inputs=[{"prev_tx": "genesis", "index": 0, "owner": "Alice"}],
        outputs=[
            {"amount": -5.0, "address": "Bob"}
        ]
    )

    print(mempool.add_transaction(tx, utxo))



def test_7_zero_fee_transaction():
    print("\nTEST 7: Zero Fee Transaction")
    utxo, mempool = setup_genesis()

    tx = create_transaction(
        inputs=[{"prev_tx": "genesis", "index": 1, "owner": "Bob"}],  # 30
        outputs=[
            {"amount": 30.0, "address": "Alice"}  # fee = 0
        ]
    )

    print(mempool.add_transaction(tx, utxo))

"""Race attacks are simulated using event order. """""


def test_8_race_attack():
    print("\nTEST 8: Race Attack Simulation")
    utxo, mempool = setup_genesis()

    low_fee_tx = create_transaction(
        inputs=[{"prev_tx": "genesis", "index": 0, "owner": "Alice"}],
        outputs=[
            {"amount": 10.0, "address": "Bob"},
            {"amount": 50.0 - 10.0 - FEE, "address": "Alice"}
        ]
    )

    high_fee_tx = create_transaction(
        inputs=[{"prev_tx": "genesis", "index": 0, "owner": "Alice"}],
        outputs=[
            {"amount": 20.0, "address": "Charlie"},
            {"amount": 50.0 - 20.0 - (2 * FEE), "address": "Alice"}
        ]
    )

    print("Low-fee TX:", mempool.add_transaction(low_fee_tx, utxo))
    print("High-fee TX:", mempool.add_transaction(high_fee_tx, utxo))



def test_9_complete_mining_flow():
    print("\nTEST 9: Complete Mining Flow")
    utxo, mempool = setup_genesis()

    tx1 = create_transaction(
        inputs=[{"prev_tx": "genesis", "index": 0, "owner": "Alice"}],
        outputs=[
            {"amount": 10.0, "address": "Bob"},
            {"amount": 50.0 - 10.0 - FEE, "address": "Alice"}
        ]
    )

    tx2 = create_transaction(
        inputs=[{"prev_tx": "genesis", "index": 1, "owner": "Bob"}],
        outputs=[
            {"amount": 5.0, "address": "Charlie"},
            {"amount": 30.0 - 5.0 - FEE, "address": "Bob"}
        ]
    )

    mempool.add_transaction(tx1, utxo)
    mempool.add_transaction(tx2, utxo)

    fees = mine_block("Miner1", mempool, utxo)

    print("Fees earned by miner:", fees)
    print("Final UTXO set:")
    for k, v in utxo.utxo_set.items():
        print(k, v)



def test_10_unconfirmed_chain():
    print("\nTEST 10: Unconfirmed Chain")
    utxo, mempool = setup_genesis()

    tx1 = create_transaction(
        inputs=[{"prev_tx": "genesis", "index": 0, "owner": "Alice"}],
        outputs=[
            {"amount": 10.0, "address": "Bob"},
            {"amount": 50.0 - 10.0 - FEE, "address": "Alice"}
        ]
    )

    mempool.add_transaction(tx1, utxo)

    tx2 = create_transaction(
        inputs=[{"prev_tx": tx1["tx_id"], "index": 0, "owner": "Bob"}],
        outputs=[
            {"amount": 5.0, "address": "Charlie"}
        ]
    )

    print(mempool.add_transaction(tx2, utxo))



if __name__ == "__main__":
    test_1_basic_valid_transaction()
    test_2_multiple_inputs()
    test_3_double_spend_same_transaction()
    test_4_mempool_double_spend()
    test_5_insufficient_funds()
    test_6_negative_amount()
    test_7_zero_fee_transaction()
    test_8_race_attack()
    test_9_complete_mining_flow()
    test_10_unconfirmed_chain()