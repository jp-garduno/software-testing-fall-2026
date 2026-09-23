# src/banking_system.py

class BankAccount:
    def __init__(self, account_type, initial_balance):
        self.account_type = account_type
        self.balance = initial_balance
        self.state = "Active"
        self.daily_transfer_total = 0
        
        # Reglas de negocio según el tipo de cuenta
        self.limits = {
            "Savings": {"min": 100, "fee": 5, "waiver": 1000, "limit": 2000},
            "Checking": {"min": 0, "fee": 10, "waiver": 5000, "limit": 5000},
            "Premium": {"min": 10000, "fee": 0, "waiver": 0, "limit": 50000}
        }
        
        if self.account_type not in self.limits:
            raise ValueError("Invalid account type")
            
        self._update_state()

    def get_daily_limit(self):
        """Return daily transfer limit based on account type."""
        return self.limits[self.account_type]["limit"]

    def _update_state(self):
        """Internal method to handle state transitions based on balance."""
        if self.state in ["Closed", "Frozen"]:
            return
            
        min_balance = self.limits[self.account_type]["min"]
        
        # Active -> Suspended if balance drops below minimum
        if self.balance < min_balance:
            self.state = "Suspended"
        # Suspended -> Active if balance is restored
        elif self.state == "Suspended" and self.balance >= min_balance:
            self.state = "Active"

    def deposit(self, amount):
        """Deposit money into the account."""
        if self.state == "Closed":
            return {"success": False, "error": "Account closed"}
        if amount <= 0:
            return {"success": False, "error": "Amount must be positive"}
        
        self.balance += amount
        self._update_state()
        return {"success": True}

    def transfer(self, amount):
        """Transfer money from this account."""
        # 1. Validate State
        if self.state in ["Frozen", "Closed"]:
            return {"success": False, "error": f"Account is {self.state.lower()}"}
        
        # 2. Validate Minimum Transfer Amount
        if amount < 0.01:
            return {"success": False, "error": "Amount must be positive"}
            
        # 3. Validate Funds
        if self.balance < amount:
            return {"success": False, "error": "Insufficient funds"}
            
        # 4. Validate Daily Limit
        if self.daily_transfer_total + amount > self.get_daily_limit():
            return {"success": False, "error": "Exceeds daily limit"}
            
        # Execute Transfer
        self.balance -= amount
        self.daily_transfer_total += amount
        self._update_state()
        
        return {"success": True}

    def process_monthly_fee(self):
        """Process monthly fees and apply waivers if applicable."""
        if self.state == "Closed":
            return {"success": False, "error": "Account closed"}
            
        rules = self.limits[self.account_type]
        
        # Check if fee is waived
        if self.balance > rules["waiver"] and rules["waiver"] > 0:
            return {"success": True, "fee_charged": 0}
            
        fee = rules["fee"]
        self.balance -= fee
        self._update_state() # If balance drops below minimum, it will suspend the account
        return {"success": True, "fee_charged": fee}

    def freeze_account(self):
        """Customer or fraud request to freeze account."""
        if self.state != "Closed":
            self.state = "Frozen"
            return {"success": True}
        return {"success": False, "error": "Account closed"}

    def unfreeze_account(self):
        """Restore account from frozen state."""
        if self.state == "Frozen":
            self.state = "Active"
            self._update_state() # Corrects state to suspended if balance is below min
            return {"success": True}
        return {"success": False, "error": "Account is not frozen"}

    def close_account(self):
        """Close the account permanently."""
        self.state = "Closed"
        return {"success": True}
        
    def reset_daily_limit(self):
        """Reset daily limit at midnight."""
        self.daily_transfer_total = 0