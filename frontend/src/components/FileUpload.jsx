import { useRef, useState } from "react";
import { Upload, FileText, X } from "lucide-react";

const ZONES = [
  {
    key: "chatLog",
    label: "Group Chat Log",
    hint: ".txt file exported from your group chat",
    accept: ".txt",
    icon: FileText,
  },
  {
    key: "venuePdf",
    label: "Venue Rules PDF",
    hint: "Campground / Airbnb / park regulation document",
    accept: ".pdf,.txt",
    icon: FileText,
  },
];

export default function FileUpload({ onSubmit, loading }) {
  const [files, setFiles] = useState({ chatLog: null, venuePdf: null });
  const refs = { chatLog: useRef(), venuePdf: useRef() };

  const set = (key, val) => setFiles((prev) => ({ ...prev, [key]: val }));

  const handleDrop = (key) => (e) => {
    e.preventDefault();
    const dropped = Array.from(e.dataTransfer.files);
    set(key, dropped[0] || null);
  };

  const handleChange = (key) => (e) => {
    const picked = Array.from(e.target.files);
    set(key, picked[0] || null);
  };

  const canSubmit = files.chatLog && !loading;

  return (
    <div className="upload-section">
      <div className="upload-grid two-col">
        {ZONES.map(({ key, label, hint, accept, icon: Icon }) => {
          const current = files[key];
          return (
            <div
              key={key}
              className={`drop-zone ${current ? "has-file" : ""}`}
              onDragOver={(e) => e.preventDefault()}
              onDrop={handleDrop(key)}
              onClick={() => refs[key].current?.click()}
            >
              <input
                ref={refs[key]}
                type="file"
                accept={accept}
                hidden
                onChange={handleChange(key)}
              />
              <Icon size={28} className="drop-icon" />
              <span className="drop-label">{label}</span>
              <span className="drop-hint">{hint}</span>

              {current && (
                <div className="file-chip" onClick={(e) => e.stopPropagation()}>
                  <span>{current.name}</span>
                  <button
                    className="chip-remove"
                    onClick={() => set(key, null)}
                  >
                    <X size={14} />
                  </button>
                </div>
              )}
            </div>
          );
        })}
      </div>

      <button
        className="btn-primary"
        disabled={!canSubmit}
        onClick={() => onSubmit(files.chatLog, files.venuePdf)}
      >
        {loading ? (
          <>
            <span className="spinner" />
            Agents Working…
          </>
        ) : (
          <>
            <Upload size={18} />
            Run Agents
          </>
        )}
      </button>
    </div>
  );
}
