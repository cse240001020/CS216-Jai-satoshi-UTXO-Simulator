from validator import validate_transaction


class Mempool:

    def __init__(self, max_size=50):
        self.transactions = []
        self.spent_utxos = set()
        self.max_size = max_size

    def add_transaction(self, tx, utxo_manager):
        valid, result = validate_transaction(tx, utxo_manager, self)
        if not valid:
            return False, result

        if len(self.transactions) >= self.max_size:
            return False, "Mempool full"

        fee = result
        self.transactions.append((tx, fee))

        for inp in tx["inputs"]:
            self.spent_utxos.add((inp["prev_tx"], inp["index"]))

        return True, f"Transaction added with fee {fee}"

    def remove_transaction(self, tx_id):
        removed_inputs = []

        for tx, _ in self.transactions:
            if tx["tx_id"] == tx_id:
                for inp in tx["inputs"]:
                    removed_inputs.append((inp["prev_tx"], inp["index"]))
                break

        self.transactions = [
            (tx, fee) for (tx, fee) in self.transactions if tx["tx_id"] != tx_id
        ]

        for utxo in removed_inputs:
            if utxo in self.spent_utxos:
                self.spent_utxos.remove(utxo)

    def get_top_transactions(self, n):
        return sorted(self.transactions, key=lambda x: x[1], reverse=True)[:n]

    def clear(self):
        self.transactions.clear()
        self.spent_utxos.clear()