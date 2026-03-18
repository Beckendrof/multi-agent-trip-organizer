import { useState } from "react";
import { Compass } from "lucide-react";
import FileUpload from "./components/FileUpload";
import AgentStatus from "./components/AgentStatus";
import ItineraryView from "./components/ItineraryView";
import BudgetEstimate from "./components/BudgetEstimate";
import ConflictResolution from "./components/ConflictResolution";
import { organizeTrip } from "./api/client";
import "./App.css";

export default function App() {
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (chatLog, venuePdf) => {
    setLoading(true);
    setError(null);
    setReport(null);
    try {
      const data = await organizeTrip(chatLog, venuePdf);
      setReport(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-shell">
      <header className="app-header">
        <div className="header-inner">
          <div className="logo">
            <Compass size={28} />
            <div>
              <h1>Trip Concierge</h1>
              <p className="tagline">Multi-Agent Trip Concierge & Logic Supervisor</p>
            </div>
          </div>
        </div>
      </header>

      <main className="main">
        <FileUpload onSubmit={handleSubmit} loading={loading} />

        {error && (
          <div className="error-banner">
            <strong>Error:</strong> {error}
          </div>
        )}

        {report && (
          <div className="results">
            <AgentStatus report={report} />
            <ItineraryView logistics={report.logistics} />
            <BudgetEstimate budget={report.budget} />
            <ConflictResolution supervisor={report.supervisor} />
          </div>
        )}
      </main>

      <footer className="app-footer">
        <span>Created by Abhinav Parameshwaran</span>
      </footer>
    </div>
  );
}
