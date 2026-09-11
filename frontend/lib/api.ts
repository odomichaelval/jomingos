import { getAccessToken } from "./auth";

const DEFAULT_API_BASE = "http://127.0.0.1:8000/api";

export function getApiBase(): string {
  return process.env.NEXT_PUBLIC_API_BASE || DEFAULT_API_BASE;
}

export async function apiFetch<T>(
  path: string,
  init: RequestInit = {},
): Promise<T> {
  const url = `${getApiBase()}${path.startsWith("/") ? path : `/${path}`}`;
  const headers = new Headers(init.headers);

  if (!headers.has("Content-Type") && init.body) {
    headers.set("Content-Type", "application/json");
  }

  const token = getAccessToken();
  if (token) headers.set("Authorization", `Bearer ${token}`);

  const response = await fetch(url, { ...init, headers });
  if (!response.ok) {
    const text = await response.text().catch(() => "");
    throw new Error(text || `Request failed (${response.status})`);
  }

  return (await response.json()) as T;
}

