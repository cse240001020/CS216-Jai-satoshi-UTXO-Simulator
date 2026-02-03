import time


def mine_block(miner_address, mempool, utxo_manager, num_txs=5):
    """
    Simulates mining:
     1) selects highest-fee transactions
     2) updates UTXO set permanently
     3) pays miner fees
    """

    selected = mempool.get_top_transactions(num_txs)
    total_fees = 0.0

    for tx, fee in selected:

        # Remove spent inputs
        for inp in tx["inputs"]:
            utxo_manager.remove_utxo(inp["prev_tx"], inp["index"])

        # Add outputs
        for i, out in enumerate(tx["outputs"]):
            utxo_manager.add_utxo(
                tx["tx_id"],
                i,
                out["amount"],
                out["address"]
            )

        total_fees += fee

    # Miner reward (coinbase)
    coinbase_tx_id = f"coinbase_{int(time.time())}"
    if total_fees > 0:
        utxo_manager.add_utxo(coinbase_tx_id, 0, total_fees, miner_address)

    # Clear mined txs from mempool
    for tx, _ in selected:
        mempool.remove_transaction(tx["tx_id"])

    return total_fees