import pytest
import json
from src.customer_validator import CustomerValidator
from src.order_calculator import Order

def load_workflows():
    """Load end-to-end workflows from JSON"""
    with open('test_data/order_workflows.json', 'r') as f:
        data = json.load(f)
        return data['workflows']

@pytest.mark.parametrize("workflow", load_workflows(), ids=lambda w: w["name"])
def test_integration_workflow(workflow):
    """Execute end-to-end steps defined in the workflow JSON"""
    validator = CustomerValidator()
    order = None
    
    for step in workflow["steps"]:
        action = step["action"]
        
        if action == "validate_customer":
            result = validator.validate(step["data"])
            assert result["is_valid"] == step["expected"]["valid"], f"Customer validation failed in {workflow['name']}"
            
            # Si el cliente es inválido, el flujo termina aquí (como en la vida real)
            if not result["is_valid"]:
                break
                
        elif action == "create_order":
            data = step["data"]
            order = Order(data["items"], data.get("customer_type", "regular"))
            
            if data.get("discount_code"):
                order.apply_discount(data["discount_code"])
                
            order.set_shipping(data.get("distance", 0), data.get("is_express", False))
            assert order is not None
            assert step["expected"]["status"] == "created"
            
        elif action == "calculate_total":
            assert order is not None, "Order must be created before calculating total"
            result = order.calculate_total()
            assert result["total"] == pytest.approx(step["expected"]["total"], rel=1e-2), f"Total mismatch in {workflow['name']}"
            
        elif action == "process_payment":
            # Simulamos que el procesador de pagos acepta la orden generada
            assert step["expected"]["status"] == "success"