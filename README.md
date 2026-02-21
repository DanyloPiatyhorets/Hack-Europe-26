# HackEurope2026 Template Repository

## DEMO UI
Go to `cd frontend/wise-agent-workbench-main/wise-agent-workbench-main`
Run `npm run dev`

TODO: Adjust ui to backend and relocate folders?

## PAID what it does in our project:
Paid.ai is a usage-based billing engine. It works by tracking "Signals" (events) to bill your customers based on what the AI actually does.
- To connect Paid.ai to LangGraph: 
  - integrate their API inside your nodes. Whenever a node completes a valuable, billable action, you emit a Signal to Paid.ai.


## Structure

- `frontend/`
  - `components/` (Cost Ticker, Dual View Interface)
  - `pages/` (Hard ROI, Projected Risk Capital Saved)
- `backend/`
  - `agent/` (parse_invoice, fetch_market_benchmark, audit_dora_compliance, human_review_node)
  - `telemetry/` (global Paid.ai SDK + `record_usage` template)
  - `settlement/` (mock Stripe Agentic Commerce Protocol endpoints)
- `mock_data/`
  - `invoices/` (pre-extracted JSON dictionaries)
  - `market_benchmarks/` (mock external market data)
  - `contracts/` (synthetic MSAs with DORA failures)

