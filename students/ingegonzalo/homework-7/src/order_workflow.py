"""Motor de workflows end-to-end: valida cliente -> crea orden -> cobra -> confirma."""
from datetime import date
from typing import Dict, Optional

from customer_validator import validate_customer
from order_calculator import Order

# Tarjetas que el procesador de pagos simulado rechaza (Luhn valido, pero declinada)
DECLINED_CARDS = frozenset({"4000000000000002"})


class OrderWorkflow:
    def __init__(self, today: Optional[date] = None):
        self.today = today
        self.customer = None
        self.customer_valid = False
        self.order = None
        self.totals = None
        self.payment_status = None

    def execute(self, action: str, data: Optional[Dict] = None) -> Dict:
        """Ejecuta una accion del workflow y devuelve su resultado."""
        handler = getattr(self, f"_do_{action}", None)
        if handler is None:
            raise ValueError(f"Unknown action: {action}")
        return handler(data or {})

    def _do_validate_customer(self, data):
        self.customer = data
        result = validate_customer(data, today=self.today)
        self.customer_valid = result["is_valid"]
        return {"valid": result["is_valid"], "errors": result["errors"]}

    def _do_create_order(self, data):
        if not self.customer_valid:
            return {"status": "rejected", "reason": "invalid customer"}
        try:
            self.order = Order(data["items"], data.get("customer_type", "regular"))
        except ValueError as error:
            return {"status": "rejected", "reason": str(error)}
        return {"status": "created"}

    def _do_apply_discount(self, data):
        if self.order is None:
            return {"applied": False}
        return {"applied": self.order.apply_discount(data["code"])}

    def _do_set_shipping(self, data):
        if self.order is None:
            return {"status": "rejected"}
        self.order.set_shipping(data["distance_km"], data.get("is_express", False))
        return {"status": "set"}

    def _do_calculate_total(self, data):
        if self.order is None:
            return {"status": "rejected"}
        self.totals = self.order.calculate_total()
        return dict(self.totals)

    def _do_process_payment(self, data):
        if self.order is None or self.totals is None:
            return {"status": "rejected"}
        if self.customer["credit_card"]["number"] in DECLINED_CARDS:
            self.payment_status = "declined"
            return {"status": "declined"}
        self.payment_status = "success"
        return {"status": "success"}

    def _do_generate_confirmation(self, data):
        if self.payment_status != "success":
            return {"status": "rejected"}
        return {
            "status": "confirmed",
            "items": len(self.order.items),
            "total": self.totals["total"],
        }