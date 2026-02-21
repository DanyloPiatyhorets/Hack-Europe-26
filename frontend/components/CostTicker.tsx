type CostTickerProps = {
  currentSpendLabel?: string;
  projectedSavingsLabel?: string;
};

export default function CostTicker({
  currentSpendLabel = "$0.00",
  projectedSavingsLabel = "$0.00",
}: CostTickerProps) {
  return (
    <section aria-label="Dynamic Cost Ticker (Template)">
      <h2>Dynamic Cost Ticker</h2>
      <p>Current Spend: {currentSpendLabel}</p>
      <p>Projected Savings: {projectedSavingsLabel}</p>
      <p>TODO: Bind live token/cost telemetry feed.</p>
    </section>
  );
}
