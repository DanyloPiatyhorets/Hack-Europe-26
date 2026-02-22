import os
import stripe
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

stripe.api_key = os.getenv("STRIPE_API_KEY")

def create_stripe_customer(name: str, email: str) -> str:
    customer = stripe.Customer.create(name=name, email=email)
    return customer.id

def create_stripe_product(name: str) -> str:
    product = stripe.Product.create(name=name)
    return product.id

def create_price_for_product(
    stripe_product_id: str,
    unit_amount: int,
    currency: str,
) -> str:
    """
    Create a Price for an existing Product.
    - unit_amount is in the smallest currency unit (usually cents)
    - recurring example: {"interval": "month"} or {"interval": "year"}
    """
    price = stripe.Price.create(
        product=stripe_product_id,
        unit_amount=unit_amount,
        currency=currency.lower(),
    )
    return price.id

def list_prices_for_product(
    stripe_product_id: str,
    active_only: bool = True,
    limit: int = 50,
) -> List[stripe.Price]:
    """
    Returns Stripe Price objects for a product (multiple prices supported).
    """
    prices = stripe.Price.list(
        product=stripe_product_id,
        active=active_only,
        limit=limit,
    )
    return prices.data

def find_price_for_product(
    stripe_product_id: str,
    currency: str,
) -> Optional[str]:
    """
    Convenience selector:
    - picks the first matching price by currency (+ optional interval/nickname).
    """
    currency = currency.lower()
    for p in list_prices_for_product(stripe_product_id):
        if p.currency != currency:
            continue
        return p.id
    return None

def create_empty_invoice(customer_id: str) -> str:
    """
    Currency is determined by invoice items (and must be consistent across them).
    """
    invoice = stripe.Invoice.create(
        customer=customer_id,
        auto_advance=False, # finalize manually
        collection_method="charge_automatically",
    )
    return invoice.id

def _get_invoice_currency(invoice_id: str) -> Optional[str]:
    inv = stripe.Invoice.retrieve(invoice_id)
    return inv.currency  # may be None until items exist

def add_invoice_item_by_price(
    invoice_id: str,
    customer_id: str,
    price_id: str,
    quantity: int = 1,
    description: Optional[str] = None,
) -> Optional[str]:
    """
    Adds an invoice item using a Price (recommended).
    Enforces: invoice currency must match the price currency.
    """
    try:
        price = stripe.Price.retrieve(price_id)
        price_currency = price.currency

        existing_currency = _get_invoice_currency(invoice_id)
        if existing_currency and existing_currency.lower() != price_currency.lower():
            raise ValueError(
                f"Invoice currency is '{existing_currency}', but price currency is '{price_currency}'. "
                "Stripe invoices must be single-currency."
            )

        item = stripe.InvoiceItem.create(
            customer=customer_id,
            invoice=invoice_id,
            pricing={"price": price_id},
            quantity=quantity,
            description=description,
        )
        return item.id

    except (stripe.error.StripeError, ValueError) as e:
        msg = getattr(e, "user_message", None) or str(e)
        print(f"Error adding invoice item: {msg}")
        return None

def finalize_invoice(invoice_id: str) -> Optional[str]:
    try:
        invoice = stripe.Invoice.finalize_invoice(invoice_id)
        return invoice.id
    except stripe.error.StripeError as e:
        print(f"Error finalizing invoice: {e.user_message}")
        return None

def pay_invoice(invoice_id: str) -> Optional[str]:
    """
    Works if the customer has a default payment method (or invoice has a payable payment_intent).
    """
    try:
        invoice = stripe.Invoice.pay(invoice_id)
        return invoice.id
    except stripe.error.StripeError as e:
        print(f"Error paying invoice: {e.user_message}")
        return None

def retrieve_invoice_data(invoice_id: str) -> str:
    try:
        invoice = stripe.Invoice.retrieve(invoice_id)
        return invoice
    except stripe.error.StripeError as e:
        print(f"Error retrieving invoice: {e.user_message}")
        return "error"