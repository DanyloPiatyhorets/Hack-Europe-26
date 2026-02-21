"""LangGraph workflow template (no runtime wiring).

Suggested deterministic sequence:
1) parse_invoice
2) fetch_market_benchmark
3) audit_dora_compliance
4) human_review_node
"""

WORKFLOW_NAME = "invoice_benchmark_dora_review"
WORKFLOW_VERSION = "template-v1"

# TODO: Instantiate LangGraph StateGraph here when implementation begins.
# TODO: Register exact nodes from backend.agent.nodes.
# TODO: Add deterministic transition map and approval gating.
