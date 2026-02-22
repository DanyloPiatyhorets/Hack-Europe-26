from dataclasses import dataclass, field


@dataclass(frozen=True)
class OptimizationResult:
    status: str
    selected_contract_id: str | None
    selected_company_id: str | None
    recipe_type: str
    risk_level: str | None
    candidate_count: int
    notes: list[str] = field(default_factory=list)
