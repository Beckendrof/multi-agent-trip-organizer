import {
  ShieldAlert,
  ShieldCheck,
  Clock,
  Lightbulb,
  CheckCircle,
} from "lucide-react";

const SEVERITY_COLORS = {
  high: "var(--danger)",
  medium: "var(--warning)",
  low: "var(--text-muted)",
};

export default function ConflictResolution({ supervisor }) {
  if (!supervisor) return null;

  const { conflicts, approved_itinerary, supervisor_notes } = supervisor;
  const hasConflicts = conflicts?.length > 0;

  return (
    <section className="card">
      <h2 className="card-title">
        {hasConflicts ? (
          <><ShieldAlert size={20} /> Conflict Resolution</>
        ) : (
          <><ShieldCheck size={20} /> Plan Approved</>
        )}
      </h2>

      {/* Supervisor summary */}
      {supervisor_notes && (
        <p className="supervisor-notes">{supervisor_notes}</p>
      )}

      {/* Conflicts */}
      {hasConflicts && (
        <div className="conflict-list">
          {conflicts.map((c, i) => (
            <div
              key={i}
              className="conflict-card"
              style={{ borderLeftColor: SEVERITY_COLORS[c.severity] || SEVERITY_COLORS.high }}
            >
              <div className="conflict-header">
                <ShieldAlert
                  size={16}
                  style={{ color: SEVERITY_COLORS[c.severity] }}
                />
                <span className="conflict-activity">{c.activity}</span>
                <span
                  className="severity-badge"
                  style={{
                    background: SEVERITY_COLORS[c.severity],
                    color: "#fff",
                  }}
                >
                  {c.severity}
                </span>
              </div>
              <p className="conflict-rule">{c.rule_violated}</p>

              {c.alternatives?.length > 0 && (
                <div className="alternatives">
                  <span className="alt-label">
                    <Lightbulb size={14} /> Suggested Alternatives
                  </span>
                  <ul>
                    {c.alternatives.map((alt, j) => (
                      <li key={j}>{alt}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Approved itinerary */}
      {approved_itinerary?.length > 0 && (
        <>
          <h3 className="subsection-title" style={{ marginTop: "1.5rem" }}>
            <CheckCircle size={16} /> Approved Itinerary
          </h3>
          <div className="timeline">
            {approved_itinerary.map((item, i) => (
              <div key={i} className="timeline-item">
                <div className="timeline-dot" />
                <div className="timeline-content">
                  <span className="timeline-time">
                    <Clock size={12} /> {item.time}
                  </span>
                  <span className="timeline-activity">{item.activity}</span>
                  {item.notes && (
                    <span className="timeline-note">{item.notes}</span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </>
      )}
    </section>
  );
}
