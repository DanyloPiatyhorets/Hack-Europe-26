import sys
import uuid
import json
import datetime
from pathlib import Path

# Allow running as: python backend/main.py
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from backend.factory.owned_contracts_api import fetch_owned_contracts_for_product
from backend.types import Contract
from backend.markets.markets_api import fetch_market_contracts_for_product

# Import your agent and paid tracing
# Adjust this import path if ERP_recipy.py is located elsewhere
from backend.recipe_engine.recipies.ERP_recipy import app as erp_agent
from paid.tracing import paid_tracing

PRODUCT_ID = "cc9f3b9a-a9f4-4ad1-8958-fab34acaae12"

def contract_to_agent_dict(c: Contract) -> dict:
    """Converts a Contract dataclass into the dictionary schema the agent expects."""
    today = datetime.date.today()
    
    # Safely calculate days from dates
    delivery_days = (c.delivery_due_date - today).days if c.delivery_due_date else 30
    payment_days = (c.payment_due_date - today).days if c.payment_due_date else 30
    
    return {
        "id": c.id,
        "company_name": c.company_id, # Fallback to ID. Fetch company name via SQL JOIN in production
        "unit_price": float(c.unit_price) if c.unit_price else 0.0,
        "quantity": float(c.quantity) if c.quantity else 0.0,
        "market_source": c.market_source,
        "delivery_days": max(0, delivery_days),
        "payment_days": max(0, payment_days),
        "credibility": 85 # Fallback. Fetch from Company table in production
    }

def main() -> None:
    print(f"[main] Start execution flow for product_id={PRODUCT_ID}")

    # 1. Fetch Data
    owned_contracts: list[Contract] = fetch_owned_contracts_for_product(product_id=PRODUCT_ID)
    print(f"[main] OWNED contracts loaded: {len(owned_contracts)}")

    market_contracts: list[Contract] = fetch_market_contracts_for_product(product_id=PRODUCT_ID)
    print(f"[main] MARKET contracts loaded: {len(market_contracts)}")

    print("[main] Data retrieval stage complete.")

    # 2. Adapt Data for Agent
    formatted_old_contracts = [contract_to_agent_dict(c) for c in owned_contracts]
    formatted_market_contracts = [contract_to_agent_dict(c) for c in market_contracts]

    # 3. Define UI State (You will eventually receive this from the frontend)
    initial_state = {
        "old_contracts": formatted_old_contracts,
        "market_contracts": formatted_market_contracts,
        "active_toggles": {
            "eu_priority": True, 
            "volume_discount": True, 
            "credibility_floor": True, 
            "payment_terms": True
        },
        "selected_flavours": ["cheapest", "low_risk", "fastest"],
        "run_id": str(uuid.uuid4()),
        "user_id": "customer-sandbox" # Replace with actual logged-in user ID
    }

    # 4. Run Agent with Paid Tracing
    print("\n[main] Initializing Agent Pipeline...")
    with paid_tracing(
        external_customer_id=initial_state["user_id"], 
        external_product_id="supply_chain_report"
    ):
        final_state = erp_agent.invoke(initial_state)
        
        # 5. Output Results for Frontend
        print("\n=== 1. NEW CONTRACT ALLOCATIONS (For UI Cards) ===")
        print(json.dumps(final_state['final_plans'], indent=2))
        
        print("\n=== 2. LLM INTERPRETATIONS (For HITL Tab) ===")
        print(final_state['llm_explanations']['hitl_summary'])


if __name__ == "__main__":
    main()
