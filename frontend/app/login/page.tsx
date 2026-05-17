"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";

import { apiFetch } from "@/lib/api";
import { setTokens } from "@/lib/auth";

type LoginResponse = {
  access: string;
  refresh: string;
  user: {
    id: number;
    username: string;
    email: string;
    role: string;
    full_name?: string;
  };
};

export default function LoginPage() {
  const router = useRouter();

  // =========================
  // State Management
  // =========================
  const [usernameOrEmail, setUsernameOrEmail] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // =========================
  // Login Function
  // =========================
  async function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();

    setError(null);
    setLoading(true);

    try {
      // Keep your Django API logic exactly the same
      const payload: Record<string, string> = {
        password,
      };

      // Allow login with either email or username
      if (usernameOrEmail.includes("@")) {
        payload.email = usernameOrEmail;
      } else {
        payload.username = usernameOrEmail;
      }

      // Call Django API
      const data = await apiFetch<LoginResponse>("/accounts/login/", {
        method: "POST",
        body: JSON.stringify(payload),
      });

      // Save JWT tokens
      setTokens({
        access: data.access,
        refresh: data.refresh,
      });

      // Redirect after successful login
      router.push("/dashboard");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      {/* =========================
          Page Title
      ========================== */}
      <div className="page-title">
        <br />

        <nav className="breadcrumbs">
          <div className="container">
            <ol className="flex items-center gap-2 text-sm">
              <li>
                <Link href="/">Home</Link>
              </li>

              

              <li className="current">Login</li>
            </ol>
          </div>
        </nav>
      </div>

      {/* =========================
          Login Section
      ========================== */}
      <section id="appointment" className="appointmnet section py-16">
        <div
          className="container"
          data-aos="fade-up"
          data-aos-delay="100"
        >
          <div className="row">
            <div className="col-lg-8 mx-auto">
              <div className="booking-wrapper rounded-2xl bg-white p-8 shadow-lg">
                {/* Header */}
                <div
                  className="booking-header mb-8 text-center"
                  data-aos="fade-up"
                  data-aos-delay="200"
                >
                  <h2 className="mb-2 text-3xl font-bold">
                    Sign In here
                  </h2>

                  <p className="text-gray-500">
                    Use your staff account details.
                  </p>
                </div>

                {/* Form */}
                <div
                  className="appointment-form"
                  data-aos="fade-up"
                  data-aos-delay="400"
                >
                  <form
                    onSubmit={onSubmit}
                    className="php-email-form"
                  >
                    <div className="row gy-4 space-y-5">
                      {/* Username or Email */}
                      <div className="col-md-12">
                        <input
                          type="text"
                          name="username"
                          className="form-control w-full rounded-xl border border-gray-300 px-4 py-3 outline-none transition focus:border-black"
                          placeholder="Username or Email"
                          value={usernameOrEmail}
                          onChange={(e) =>
                            setUsernameOrEmail(e.target.value)
                          }
                          autoComplete="username"
                          required
                        />
                      </div>

                      {/* Password */}
                      <div className="col-md-12">
                        <input
                          type="password"
                          name="password"
                          className="form-control w-full rounded-xl border border-gray-300 px-4 py-3 outline-none transition focus:border-black"
                          placeholder="Password"
                          value={password}
                          onChange={(e) =>
                            setPassword(e.target.value)
                          }
                          autoComplete="current-password"
                          required
                        />
                      </div>

                      {/* Error Message */}
                      {error && (
                        <div className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
                          {error}
                        </div>
                      )}

                      {/* Submit Button */}
                      <div className="col-12">
                        <button
                          type="submit"
                          className="btn-book w-full rounded-xl bg-black px-6 py-3 font-medium text-white transition hover:opacity-90 disabled:opacity-50"
                          disabled={loading}
                        >
                          {loading ? "Signing in..." : "Login"}
                        </button>
                      </div>
                    </div>
                  </form>
                </div>

                {/* Register Link */}
                <div
                  className="emergency-info mt-6 text-center"
                  data-aos="fade-up"
                  data-aos-delay="500"
                >
                  <p className="text-sm text-gray-600">
                    <i className="bi bi-exclamation-triangle"></i>{" "}
                    New here?{" "}
                    <Link
                      href="/register"
                      className="font-semibold underline"
                    >
                      Register here
                    </Link>
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}