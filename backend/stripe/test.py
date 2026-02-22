from stripe_helper import *

# 1) create customer + product
customer_id = create_stripe_customer("Acme Ltd", "billing@acme.com")
product_id = create_stripe_product("Data API Access")

# 2) create multiple prices for same product (different contracts)
price_standard_gbp = create_price_for_product(
    product_id, unit_amount=10000, currency="gbp"
)

price_enterprise_gbp = create_price_for_product(
    product_id, unit_amount=8000, currency="gbp"
)

price_usd_yearly = create_price_for_product(
    product_id, unit_amount=90000, currency="usd"
)

# 3) create invoice and add the selected price
invoice_id = create_empty_invoice(customer_id)

add_invoice_item_by_price(
    invoice_id=invoice_id,
    customer_id=customer_id,
    price_id=price_enterprise_gbp,
    quantity=1,
)

# 4) finalize (and optionally pay)
finalize_invoice(invoice_id)
print(retrieve_invoice_data(invoice_id))