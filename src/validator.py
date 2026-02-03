def validate_transaction(tx, utxo_manager, mempool):
    """
    Validation Rules:

    1. All inputs must exist in UTXO set
    2. No double-spending in inputs (same UTXO twice in same transaction)
    3. Sum(inputs) ≥ Sum(outputs) (difference = fee)
    4. No negative amounts in outputs
    5. No conflict with mempool (UTXO not already spent in unconfirmed tx)
    6. Input owner must match UTXO owner
    """

    used_inputs = set()
    input_sum = 0.0

    # Rule 4: no negative outputs
    for out in tx["outputs"]:
        if out["amount"] < 0:
            return False, "Negative output amount"

    # Validate inputs
    for inp in tx["inputs"]:
        key = (inp["prev_tx"], inp["index"])

        # Rule 2: same-transaction double spend
        if key in used_inputs:
            return False, "Double spend in same transaction"

        used_inputs.add(key)

        # Rule 1: must exist
        if not utxo_manager.exists(inp["prev_tx"], inp["index"]):
            return False, f"UTXO {key} does not exist"

        # Rule 5: mempool conflict
        if key in mempool.spent_utxos:
            return False, f"UTXO {key} already spent in mempool"

        utxo = utxo_manager.utxo_set[key]

        # Rule 6: ownership check
        if utxo["owner"] != inp["owner"]:
            return False, "Invalid owner for UTXO"

        input_sum += utxo["amount"]

    output_sum = sum(out["amount"] for out in tx["outputs"])

    # Rule 3: sufficient funds
    if input_sum < output_sum:
        return False, "Insufficient funds"

    fee = round(input_sum - output_sum, 8)
    return True, fee