export async function organizeTrip(chatLog, venuePdf) {
  const form = new FormData();
  form.append("chat_log", chatLog);
  if (venuePdf) form.append("venue_pdf", venuePdf);

  const res = await fetch("/api/organize", { method: "POST", body: form });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.message || `Server error ${res.status}`);
  }
  return res.json();
}
