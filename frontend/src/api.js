// frontend/src/api.js

import API_BASE from "./config";

// Fetch instances
export async function getInstances() {
  const res = await fetch(`${API_BASE}/instances`);
  if (!res.ok) throw new Error("Failed to fetch instances");
  return res.json();
}

// Fetch recommendations
export async function getRecommendations() {
  const res = await fetch(`${API_BASE}/recommendations`);
  if (!res.ok) throw new Error("Failed to fetch recommendations");
  return res.json();
}

// Fetch audit logs
export async function getAudit() {
  const res = await fetch(`${API_BASE}/audit`);
  if (!res.ok) throw new Error("Failed to fetch audit logs");
  return res.json();
}
