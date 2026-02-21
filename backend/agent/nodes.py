"""Deterministic execution node templates.

Required nodes:
- parse_invoice
- fetch_market_benchmark
- audit_dora_compliance
- human_review_node
"""

from typing import Any, Dict


def parse_invoice(state: Dict[str, Any]) -> Dict[str, Any]:
    """Template node: load pre-extracted invoice JSON from mock_data/invoices."""
    return {"status": "template", "node": "parse_invoice", "state": state}


def fetch_market_benchmark(state: Dict[str, Any]) -> Dict[str, Any]:
    """Template node: read benchmark data from mock_data/market_benchmarks."""
    return {"status": "template", "node": "fetch_market_benchmark", "state": state}


def audit_dora_compliance(state: Dict[str, Any]) -> Dict[str, Any]:
    """Template node: evaluate synthetic contract clauses for DORA failures."""
    return {"status": "template", "node": "audit_dora_compliance", "state": state}


def human_review_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Template node: present findings for managerial approval."""
    return {"status": "template", "node": "human_review_node", "state": state}
