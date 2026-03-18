import { CheckCircle, AlertTriangle, XCircle } from "lucide-react";

export default function AgentStatus({ report }) {
  if (!report) return null;

  const agents = [
    { name: "Logistical Parser", data: report.logistics },
    { name: "Financial Estimator", data: report.budget },
    { name: "Conflict Supervisor", data: report.supervisor },
  ];

  return (
    <div className="agent-status-section">
      <div className="agent-status-bar">
        {agents.map(({ name, data }) => (
          <div key={name} className={`status-chip ${data ? "done" : "skipped"}`}>
            {data ? <CheckCircle size={16} /> : <XCircle size={16} />}
            <span>{name}</span>
          </div>
        ))}
        {report.errors?.length > 0 && (
          <div className="status-chip warning">
            <AlertTriangle size={16} />
            <span>{report.errors.length} error(s)</span>
          </div>
        )}
      </div>

      {report.errors?.length > 0 && (
        <div className="error-details">
          {report.errors.map((err, i) => (
            <div key={i} className="error-detail-item">
              <AlertTriangle size={14} />
              <span>{err}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
