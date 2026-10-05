ACCOUNT_RULES = {
    "Savings": {"min_balance": 100, "fee": 5, "waiver": 1000, "daily_limit": 2000},
    "Checking": {"min_balance": 0, "fee": 10, "waiver": 5000, "daily_limit": 5000},
    "Premium": {"min_balance": 10000, "fee": 0, "waiver": None, "daily_limit": 50000},
}

VALID_STATES = {"Active", "Frozen", "Suspended", "Closed"}


class BankAccount:
    def __init__(self, account_type, initial_balance, registered_payees=None):
        if account_type not in ACCOUNT_RULES:
            raise ValueError(f"Invalid account type: {account_type}")
        if initial_balance < ACCOUNT_RULES[account_type]["min_balance"]:
            raise ValueError("Initial deposit below minimum for account type")

        self.account_type = account_type
        self.balance = round(float(initial_balance), 2)
        self.state = "Active"
        self.daily_transfer_total = 0.0
        self.transaction_history = []
        # A small fixed set of valid payees, standing in for a real payee directory
        self.registered_payees = registered_payees or {
            "Electricity",
            "Water",
            "Credit Debt",
        }

    def get_daily_limit(self):
        return ACCOUNT_RULES[self.account_type]["daily_limit"]

    def get_minimum_balance(self):
        return ACCOUNT_RULES[self.account_type]["min_balance"]

    def get_monthly_fee(self):
        return ACCOUNT_RULES[self.account_type]["fee"]

    def get_fee_waiver_threshold(self):
        return ACCOUNT_RULES[self.account_type]["waiver"]

    def transfer(self, amount):
        if not isinstance(amount, (int, float)):
            return {"success": False, "error": "Invalid amount format"}
        amount = round(float(amount), 2)

        if amount <= 0:
            return {"success": False, "error": "Amount must be positive"}
        if amount > self.balance:
            return {"success": False, "error": "Insufficient funds"}
        if self.state != "Active":
            return {"success": False, "error": f"Account is {self.state}, transaction denied"}
        if self.daily_transfer_total + amount > self.get_daily_limit():
            return {"success": False, "error": "Exceeds daily limit"}

        self.balance = round(self.balance - amount, 2)
        self.daily_transfer_total = round(self.daily_transfer_total + amount, 2)
        self._check_suspension()
        self.transaction_history.append({"type": "transfer", "amount": amount})
        return {"success": True, "balance": self.balance}

    def deposit(self, amount):
        if self.state == "Closed":
            return {"success": False, "error": "Account is closed"}
        if amount <= 0:
            return {"success": False, "error": "Amount must be positive"}

        self.balance = round(self.balance + float(amount), 2)
        if self.state == "Suspended" and self.balance >= self.get_minimum_balance():
            self.state = "Active"
        self.transaction_history.append({"type": "deposit", "amount": amount})
        return {"success": True, "balance": self.balance, "state": self.state}

    def pay_bill(self, payee, amount):
        if not payee or payee not in self.registered_payees:
            return {"success": False, "error": "Invalid payee"}
        if amount <= 0:
            return {"success": False, "error": "Amount must be positive"}
        if amount > self.balance:
            return {"success": False, "error": "Insufficient funds"}

        self.balance = round(self.balance - float(amount), 2)
        self._check_suspension()
        self.transaction_history.append({"type": "bill_payment", "payee": payee, "amount": amount})
        return {"success": True, "balance": self.balance}

    def apply_monthly_fee(self):
        fee = self.get_monthly_fee()
        threshold = self.get_fee_waiver_threshold()

        if fee == 0 or (threshold is not None and self.balance > threshold):
            return {"fee_charged": 0, "balance": self.balance}

        self.balance = round(self.balance - fee, 2)
        self._check_suspension()
        self.transaction_history.append({"type": "monthly_fee", "amount": fee})
        return {"fee_charged": fee, "balance": self.balance, "state": self.state}

    def reset_daily_limit(self):
        """Simulates the midnight reset of the daily transfer total."""
        self.daily_transfer_total = 0.0


    def freeze(self):
        if self.state == "Closed":
            return {"success": False, "error": "Account is closed"}
        self.state = "Frozen"
        return {"success": True, "state": self.state}

    def unfreeze(self):
        if self.state != "Frozen":
            return {"success": False, "error": "Account is not frozen"}
        self.state = "Active"
        return {"success": True, "state": self.state}

    def close(self):
        if self.state == "Closed":
            return {"success": False, "error": "Account already closed"}
        self.state = "Closed"
        return {"success": True, "state": self.state}

    def _check_suspension(self):
        """Internal: moves an Active account to Suspended if balance < minimum."""
        if self.state == "Active" and self.balance < self.get_minimum_balance():
            self.state = "Suspended"

    # ---------- Transaction history ----------

    def get_transaction_history(self, start_date=None, end_date=None):
        """Returns the full transaction history (date filtering omitted for brevity)."""
        return self.transaction_history