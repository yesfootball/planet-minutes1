const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";
export async function getJSON(path) {
  const r = await fetch(`${API_BASE}${path}`, { next: { revalidate: 10 } });
  if (!r.ok) throw new Error(`API ${r.status}`);
  return r.json();
}
