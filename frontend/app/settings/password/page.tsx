"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { apiFetch } from "@/lib/api";

type ChangePasswordResponse = {
  message: string;
};

export default function PasswordChangePage() {
  const router = useRouter();
  const [oldPassword, setOldPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setSuccess(null);
    setLoading(true);
    try {
      const data = await apiFetch<ChangePasswordResponse>(
        "/accounts/change-password/",
        {
          method: "POST",
          body: JSON.stringify({
            old_password: oldPassword,
            new_password: newPassword,
          }),
        },
      );
      setSuccess(data.message || "Password changed successfully.");
      setOldPassword("");
      setNewPassword("");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Password change failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex items-center justify-center px-6 py-14">
      <main className="w-full max-w-md rounded-2xl bg-white p-10 shadow-sm dark:bg-zinc-950">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-semibold tracking-tight text-zinc-900 dark:text-zinc-50">
            Change password
          </h1>
          <Link
            className="text-sm font-medium text-zinc-900 underline underline-offset-4 dark:text-zinc-50"
            href="/dashboard"
          >
            Back
          </Link>
        </div>

        <form className="mt-8 space-y-4" onSubmit={onSubmit}>
          <div>
            <label className="mb-1 block text-sm font-medium text-zinc-800 dark:text-zinc-200">
              Old password
            </label>
            <input
              className="h-11 w-full rounded-xl border border-zinc-200 bg-white px-3 text-sm text-zinc-900 outline-none focus:border-zinc-400 dark:border-zinc-800 dark:bg-zinc-950 dark:text-zinc-50"
              type="password"
              value={oldPassword}
              onChange={(e) => setOldPassword(e.target.value)}
              autoComplete="current-password"
              required
            />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-zinc-800 dark:text-zinc-200">
              New password
            </label>
            <input
              className="h-11 w-full rounded-xl border border-zinc-200 bg-white px-3 text-sm text-zinc-900 outline-none focus:border-zinc-400 dark:border-zinc-800 dark:bg-zinc-950 dark:text-zinc-50"
              type="password"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              autoComplete="new-password"
              required
            />
          </div>

          {error ? (
            <div className="rounded-xl border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700 dark:border-red-900/50 dark:bg-red-950/40 dark:text-red-200">
              {error}
            </div>
          ) : null}

          {success ? (
            <div className="rounded-xl border border-emerald-200 bg-emerald-50 px-3 py-2 text-sm text-emerald-700 dark:border-emerald-900/50 dark:bg-emerald-950/40 dark:text-emerald-200">
              {success}
            </div>
          ) : null}

          <button
            className="inline-flex h-11 w-full items-center justify-center rounded-xl bg-zinc-900 px-4 text-sm font-medium text-white hover:bg-zinc-800 disabled:opacity-50 dark:bg-zinc-50 dark:text-zinc-900 dark:hover:bg-zinc-200"
            type="submit"
            disabled={loading}
          >
            {loading ? "Saving..." : "Change password"}
          </button>

          <button
            className="inline-flex h-11 w-full items-center justify-center rounded-xl border border-zinc-200 px-4 text-sm font-medium text-zinc-900 hover:bg-zinc-50 dark:border-zinc-800 dark:text-zinc-50 dark:hover:bg-zinc-900"
            type="button"
            onClick={() => router.push("/dashboard")}
          >
            Cancel
          </button>
        </form>
      </main>
    </div>
  );
}
