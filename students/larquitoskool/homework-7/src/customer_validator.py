import re
from datetime import datetime

class CustomerValidator:
    @staticmethod
    def validate_email(email):
        """Valida formato de correo básico"""
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return bool(re.match(pattern, str(email)))

    @staticmethod
    def validate_phone(phone):
        """Valida formato US: (XXX) XXX-XXXX"""
        pattern = r'^\(\d{3}\) \d{3}-\d{4}$'
        return bool(re.match(pattern, str(phone)))

    @staticmethod
    def validate_address(address):
        """Valida que existan todos los campos de la dirección"""
        required_keys = ['street', 'city', 'state', 'zip']
        if not isinstance(address, dict):
            return False
        return all(key in address and bool(address.get(key)) for key in required_keys)

    @staticmethod
    def validate_luhn(card_number):
        """Valida la tarjeta usando el algoritmo de Luhn"""
        card_str = str(card_number).replace(" ", "")
        if not card_str.isdigit():
            return False
            
        digits = [int(d) for d in card_str]
        odd_digits = digits[-1::-2]
        even_digits = [sum(divmod(2 * d, 10)) for d in digits[-2::-2]]
        return (sum(odd_digits) + sum(even_digits)) % 10 == 0

    @staticmethod
    def validate_expiration(exp_date):
        """Valida que la fecha MM/YYYY sea mayor o igual al mes actual"""
        try:
            exp_month, exp_year = map(int, str(exp_date).split('/'))
            if exp_month < 1 or exp_month > 12:
                return False
                
            now = datetime.now()
            if exp_year > now.year or (exp_year == now.year and exp_month >= now.month):
                return True
            return False
        except (ValueError, AttributeError):
            return False

    def validate(self, customer):
        """Ejecuta todas las validaciones y recolecta errores"""
        errors = []
        
        if not self.validate_email(customer.get('email', '')):
            errors.append("Invalid email format")
            
        if not self.validate_phone(customer.get('phone', '')):
            errors.append("Invalid phone format")
            
        if not self.validate_address(customer.get('billing_address', {})):
            errors.append("Invalid billing address")
            
        cc = customer.get('credit_card', {})
        if not self.validate_luhn(cc.get('number', '')):
            errors.append("Invalid credit card number")
            
        if not self.validate_expiration(cc.get('expiration', '')):
            errors.append("Credit card expired or invalid date")

        return {
            "is_valid": len(errors) == 0,
            "errors": errors
        }