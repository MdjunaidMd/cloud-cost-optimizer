// frontend/src/config.js

// Reads from .env (VITE_API_BASE_URL). Falls back to localhost for dev.
const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8010";

export default API_BASE;
