import { DollarSign, TrendingUp, TrendingDown, CheckCircle } from "lucide-react";

function fmt(n) {
  return `$${Number(n).toFixed(2)}`;
}

export default function BudgetEstimate({ budget }) {
  if (!budget) return null;

  const {
    stated_budget,
    estimated_items,
    total_estimated,
    within_budget,
    budget_summary,
  } = budget;

  return (
    <section className="card">
      <h2 className="card-title">
        <DollarSign size={20} /> Budget Estimate
      </h2>

      {/* Budget headline */}
      <div className="budget-headline">
        {stated_budget != null ? (
          <div className="budget-stat">
            <span className="budget-stat-label">Stated Budget</span>
            <span className="budget-stat-value">{fmt(stated_budget)}</span>
          </div>
        ) : (
          <div className="budget-stat">
            <span className="budget-stat-label">Stated Budget</span>
            <span className="budget-stat-value muted">Not mentioned</span>
          </div>
        )}
        <div className="budget-stat">
          <span className="budget-stat-label">Estimated Total</span>
          <span className="budget-stat-value">{fmt(total_estimated)}</span>
        </div>
        <div className={`budget-verdict ${within_budget ? "ok" : "over"}`}>
          {within_budget ? (
            <>
              <CheckCircle size={18} />
              <span>Within budget</span>
            </>
          ) : (
            <>
              <TrendingUp size={18} />
              <span>Over budget</span>
            </>
          )}
        </div>
      </div>

      {/* Itemised estimates */}
      {estimated_items?.length > 0 && (
        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Category</th>
                <th>Est. Cost</th>
                <th>Notes</th>
              </tr>
            </thead>
            <tbody>
              {estimated_items.map((item, i) => (
                <tr key={i}>
                  <td>{item.category}</td>
                  <td className="mono">{fmt(item.estimated_cost)}</td>
                  <td className="muted-text">{item.notes}</td>
                </tr>
              ))}
              <tr className="total-row">
                <td><strong>Total</strong></td>
                <td className="mono"><strong>{fmt(total_estimated)}</strong></td>
                <td></td>
              </tr>
            </tbody>
          </table>
        </div>
      )}

      {/* Summary paragraph */}
      {budget_summary && (
        <p className="budget-summary">{budget_summary}</p>
      )}
    </section>
  );
}
