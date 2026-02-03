class UTXOManager:
    

    def __init__(self):
       
        self.utxo_set = {}

    def add_utxo(self, tx_id: str, index: int, amount: float, owner: str):
        self.utxo_set[(tx_id, index)] = {
            "amount": amount,  "owner": owner
        }

    def remove_utxo(self, tx_id: str, index: int):
         key = (tx_id, index)
         if key in self.utxo_set:
            del self.utxo_set[key]

    def exists(self, tx_id: str, index: int) -> bool:
        return (tx_id, index) in self.utxo_set

    def get_balance(self, owner: str) -> float:
        balance = 0.0
        for utxo in self.utxo_set.values():
            if utxo["owner"] == owner: balance += utxo["amount"]
        return balance

    def get_utxos_for_owner(self, owner: str):
        result = []
        for (tx_id, index), utxo in self.utxo_set.items():
            if utxo["owner"] == owner: result.append((tx_id, index, utxo["amount"]))
        return result