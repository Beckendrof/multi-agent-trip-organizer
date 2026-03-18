import { Users, Clock, Utensils, CalendarDays } from "lucide-react";

export default function ItineraryView({ logistics }) {
  if (!logistics) return null;
  const { attendees, itinerary } = logistics;

  return (
    <section className="card">
      <h2 className="card-title">
        <CalendarDays size={20} /> Parsed Logistics
      </h2>

      {/* Attendees */}
      <h3 className="subsection-title">
        <Users size={16} /> Attendees ({attendees.length})
      </h3>
      <div className="attendee-grid">
        {attendees.map((a) => (
          <div key={a.name} className="attendee-card">
            <div className="attendee-name">{a.name}</div>
            {a.arrival && (
              <div className="attendee-meta">
                <Clock size={12} /> {a.arrival}
                {a.departure ? ` – ${a.departure}` : ""}
              </div>
            )}
            {a.dietary_restrictions?.length > 0 && (
              <div className="attendee-meta diet">
                <Utensils size={12} />{" "}
                {a.dietary_restrictions.join(", ")}
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Proposed Itinerary */}
      {itinerary.length > 0 && (
        <>
          <h3 className="subsection-title" style={{ marginTop: "1.5rem" }}>
            <Clock size={16} /> Proposed Itinerary
          </h3>
          <div className="timeline">
            {itinerary.map((item, i) => (
              <div key={i} className="timeline-item">
                <div className="timeline-dot" />
                <div className="timeline-content">
                  <span className="timeline-time">{item.time}</span>
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
