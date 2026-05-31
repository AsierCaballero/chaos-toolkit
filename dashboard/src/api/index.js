const API_BASE = "/api";

export async function fetchExperiments() {
  const res = await fetch(`${API_BASE}/experiments`);
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export async function fetchExperiment(name) {
  const res = await fetch(`${API_BASE}/experiments/${encodeURIComponent(name)}`);
  if (!res.ok) return null;
  return res.json();
}

export async function runExperiment(manifest) {
  const res = await fetch(`${API_BASE}/experiments`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ manifest }),
  });
  return res.json();
}

export async function deleteExperiment(name) {
  const res = await fetch(`${API_BASE}/experiments/${encodeURIComponent(name)}`, {
    method: "DELETE",
  });
  return res.ok;
}
