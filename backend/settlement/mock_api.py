"""Mock RESTful endpoints for Stripe Agentic Commerce Protocol simulation.

Template-only definitions (no live payments).
"""

from typing import Dict, Any


def post_checkout_session(request: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "status": "template",
        "endpoint": "POST /settlement/checkout-session",
        "request": request,
    }


def post_authorize_payment(request: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "status": "template",
        "endpoint": "POST /settlement/authorize-payment",
        "request": request,
    }


def post_finalize_settlement(request: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "status": "template",
        "endpoint": "POST /settlement/finalize-settlement",
        "request": request,
    }
