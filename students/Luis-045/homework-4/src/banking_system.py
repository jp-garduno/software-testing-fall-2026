"""SecureBank banking system used for black box testing."""


class BankAccount:
    """Represent a SecureBank account."""

    ACCOUNT_RULES = {
        "Savings": {
            "minimum_balance": 100,
            "monthly_fee": 5,
            "waiver_threshold": 1000,
            "daily_limit": 2000,
        },
        "Checking": {
            "minimum_balance": 0,
            "monthly_fee": 10,
            "waiver_threshold": 5000,
            "daily_limit": 5000,
        },
        "Premium": {
            "minimum_balance": 10000,
            "monthly_fee": 0,
            "waiver_threshold": 0,
            "daily_limit": 50000,
        },
    }

    def __init__(self, account_type, initial_balance):
        if account_type not in self.ACCOUNT_RULES:
            raise ValueError("Invalid account type")

        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative")

        self.account_type = account_type
        self.balance = float(initial_balance)
        self.state = "Active"
        self.daily_transfer_total = 0.0

    def get_daily_limit(self):
        """Return the daily transfer limit."""
        return self.ACCOUNT_RULES[self.account_type]["daily_limit"]

    def get_minimum_balance(self):
        """Return the minimum required balance."""
        return self.ACCOUNT_RULES[self.account_type]["minimum_balance"]

    def transfer(self, amount):
        """Transfer money from the account."""
        if self.state != "Active":
            return {
                "success": False,
                "error": "Account is not active",
            }

        if amount <= 0:
            return {
                "success": False,
                "error": "Amount must be positive",
            }

        if self.daily_transfer_total + amount > self.get_daily_limit():
            return {
                "success": False,
                "error": "Exceeds daily limit",
            }

        if amount > self.balance:
            return {
                "success": False,
                "error": "Insufficient funds",
            }

        self.balance -= amount
        self.daily_transfer_total += amount

        if self.balance < self.get_minimum_balance():
            self.state = "Suspended"

        return {
            "success": True,
            "balance": self.balance,
        }

    def deposit(self, amount):
        """Deposit money into the account."""
        if self.state == "Closed":
            return {
                "success": False,
                "error": "Account closed",
            }

        if self.state == "Frozen":
            return {
                "success": False,
                "error": "Account frozen",
            }

        if amount <= 0:
            return {
                "success": False,
                "error": "Amount must be positive",
            }

        self.balance += amount

        if (
            self.state == "Suspended"
            and self.balance >= self.get_minimum_balance()
        ):
            self.state = "Active"

        return {
            "success": True,
            "balance": self.balance,
        }

    def freeze(self):
        """Freeze an active account."""
        if self.state == "Closed":
            return False

        self.state = "Frozen"
        return True

    def unfreeze(self):
        """Restore a frozen account."""
        if self.state != "Frozen":
            return False

        self.state = "Active"
        return True

    def close(self):
        """Close the account permanently."""
        self.state = "Closed"
        return True

    def process_monthly_fee(self):
        """Charge the monthly account fee when applicable."""
        rules = self.ACCOUNT_RULES[self.account_type]
        fee = rules["monthly_fee"]
        threshold = rules["waiver_threshold"]

        if self.state == "Closed":
            return {
                "success": False,
                "error": "Account closed",
            }

        if fee == 0 or self.balance > threshold:
            return {
                "success": True,
                "fee_charged": 0,
            }

        self.balance -= fee

        if self.balance < self.get_minimum_balance():
            self.state = "Suspended"

        return {
            "success": True,
            "fee_charged": fee,
        }

    def pay_bill(self, payee, amount):
        """Pay a bill using the account balance."""
        if self.state != "Active":
            return {
                "success": False,
                "error": "Account is not active",
            }

        if not payee or not isinstance(payee, str):
            return {
                "success": False,
                "error": "Invalid payee",
            }

        if amount <= 0:
            return {
                "success": False,
                "error": "Amount must be positive",
            }

        if amount > self.balance:
            return {
                "success": False,
                "error": "Insufficient funds",
            }

        self.balance -= amount

        if self.balance < self.get_minimum_balance():
            self.state = "Suspended"

        return {
            "success": True,
            "balance": self.balance,
        }