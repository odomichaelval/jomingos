"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { apiFetch } from "@/lib/api";
import { setTokens } from "@/lib/auth";

const ROLE_OPTIONS = [
  { value: "care_assistant", label: "Care Assistant" },
  { value: "nurse", label: "Nurse" },
  { value: "doctor", label: "Doctor" },
  { value: "admin", label: "Administrator" },
  { value: "family", label: "Family Member" },
];

type RegisterResponse = {
  user: {
    id: number;
    username: string;
    email: string;
    role: string;
    full_name?: string;
  };
  refresh: string;
  access: string;
  dashboard_path: string;
};

export default function RegisterPage() {
  const router = useRouter();

  // =========================
  // State Management
  // =========================
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    first_name: "",
    last_name: "",
    password: "",
    password2: "",
    role: "care_assistant",
  });

  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState<Record<string, string[]>>({});

  // =========================
  // Form Handlers
  // =========================
  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
    // Clear error for this field
    if (errors[name]) {
      setErrors((prev) => {
        const newErrors = { ...prev };
        delete newErrors[name];
        return newErrors;
      });
    }
  };

  // =========================
  // Submit Handler
  // =========================
  async function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setErrors({});
    setLoading(true);

    try {
      const data = await apiFetch<RegisterResponse>("/accounts/register/", {
        method: "POST",
        body: JSON.stringify(formData),
      });

      // Save JWT tokens
      setTokens({
        access: data.access,
        refresh: data.refresh,
      });

      // Redirect to appropriate dashboard based on role
      router.push(data.dashboard_path || "/dashboard");
    } catch (err) {
      if (
        err instanceof Error &&
        err.message.includes("{") &&
        err.message.includes("}")
      ) {
        try {
          const errorData = JSON.parse(err.message);
          setErrors(errorData);
        } catch {
          setErrors({
            general: [err instanceof Error ? err.message : "Registration failed"],
          });
        }
      } else {
        setErrors({
          general: [err instanceof Error ? err.message : "Registration failed"],
        });
      }
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
              <li className="current">Register</li>
            </ol>
          </div>
        </nav>
      </div>

      {/* =========================
          Registration Section
      ========================== */}
      <section id="register" className="register section py-16">
        <div className="container" data-aos="fade-up" data-aos-delay="100">
          <div className="row">
            <div className="col-lg-8 mx-auto">
              <div className="booking-wrapper rounded-2xl bg-white p-8 shadow-lg">
                {/* Header */}
                <div
                  className="booking-header mb-8 text-center"
                  data-aos="fade-up"
                  data-aos-delay="200"
                >
                  <h2 className="mb-2 text-3xl font-bold">Create Account</h2>
                  <p className="text-gray-500">
                    Join Jomingos and streamline your healthcare documentation
                  </p>
                </div>

                {/* Form */}
                <div
                  className="appointment-form"
                  data-aos="fade-up"
                  data-aos-delay="400"
                >
                  <form onSubmit={onSubmit} className="php-email-form">
                    <div className="row gy-4 space-y-5">
                      {/* General Error */}
                      {errors.general && (
                        <div className="col-md-12">
                          <div className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
                            <i className="bi bi-exclamation-triangle me-2"></i>
                            {errors.general[0]}
                          </div>
                        </div>
                      )}

                      {/* Username */}
                      <div className="col-md-12">
                        <input
                          type="text"
                          name="username"
                          className={`form-control w-full rounded-xl border px-4 py-3 outline-none transition ${
                            errors.username
                              ? "border-red-300 bg-red-50 focus:border-red-500"
                              : "border-gray-300 focus:border-black"
                          }`}
                          placeholder="Username"
                          value={formData.username}
                          onChange={handleChange}
                          required
                        />
                        {errors.username && (
                          <p className="mt-1 text-sm text-red-600">
                            {errors.username[0]}
                          </p>
                        )}
                      </div>

                      {/* First & Last Name */}
                      <div className="col-md-12">
                        <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
                          <div>
                            <input
                              type="text"
                              name="first_name"
                              className={`form-control w-full rounded-xl border px-4 py-3 outline-none transition ${
                                errors.first_name
                                  ? "border-red-300 bg-red-50 focus:border-red-500"
                                  : "border-gray-300 focus:border-black"
                              }`}
                              placeholder="First Name"
                              value={formData.first_name}
                              onChange={handleChange}
                              required
                            />
                            {errors.first_name && (
                              <p className="mt-1 text-sm text-red-600">
                                {errors.first_name[0]}
                              </p>
                            )}
                          </div>
                          <div>
                            <input
                              type="text"
                              name="last_name"
                              className={`form-control w-full rounded-xl border px-4 py-3 outline-none transition ${
                                errors.last_name
                                  ? "border-red-300 bg-red-50 focus:border-red-500"
                                  : "border-gray-300 focus:border-black"
                              }`}
                              placeholder="Last Name"
                              value={formData.last_name}
                              onChange={handleChange}
                              required
                            />
                            {errors.last_name && (
                              <p className="mt-1 text-sm text-red-600">
                                {errors.last_name[0]}
                              </p>
                            )}
                          </div>
                        </div>
                      </div>

                      {/* Email */}
                      <div className="col-md-12">
                        <input
                          type="email"
                          name="email"
                          className={`form-control w-full rounded-xl border px-4 py-3 outline-none transition ${
                            errors.email
                              ? "border-red-300 bg-red-50 focus:border-red-500"
                              : "border-gray-300 focus:border-black"
                          }`}
                          placeholder="Email Address"
                          value={formData.email}
                          onChange={handleChange}
                          required
                        />
                        {errors.email && (
                          <p className="mt-1 text-sm text-red-600">
                            {errors.email[0]}
                          </p>
                        )}
                      </div>

                      {/* Role Dropdown */}
                      <div className="col-md-12">
                        <select
                          name="role"
                          className={`form-control w-full rounded-xl border px-4 py-3 outline-none transition ${
                            errors.role
                              ? "border-red-300 bg-red-50 focus:border-red-500"
                              : "border-gray-300 focus:border-black"
                          }`}
                          value={formData.role}
                          onChange={handleChange}
                          required
                        >
                          <option value="">Select your role...</option>
                          {ROLE_OPTIONS.map((role) => (
                            <option key={role.value} value={role.value}>
                              {role.label}
                            </option>
                          ))}
                        </select>
                        <p className="mt-2 text-sm text-gray-600">
                          <i className="bi bi-info-circle me-1"></i>
                          This determines your dashboard view and permissions
                        </p>
                        {errors.role && (
                          <p className="mt-1 text-sm text-red-600">
                            {errors.role[0]}
                          </p>
                        )}
                      </div>

                      {/* Password */}
                      <div className="col-md-12">
                        <input
                          type="password"
                          name="password"
                          className={`form-control w-full rounded-xl border px-4 py-3 outline-none transition ${
                            errors.password
                              ? "border-red-300 bg-red-50 focus:border-red-500"
                              : "border-gray-300 focus:border-black"
                          }`}
                          placeholder="Password"
                          value={formData.password}
                          onChange={handleChange}
                          required
                        />
                        <p className="mt-2 text-sm text-gray-600">
                          <i className="bi bi-info-circle me-1"></i>
                          Must contain uppercase, lowercase, numbers & special
                          characters
                        </p>
                        {errors.password && (
                          <p className="mt-1 text-sm text-red-600">
                            {errors.password[0]}
                          </p>
                        )}
                      </div>

                      {/* Confirm Password */}
                      <div className="col-md-12">
                        <input
                          type="password"
                          name="password2"
                          className={`form-control w-full rounded-xl border px-4 py-3 outline-none transition ${
                            errors.password2
                              ? "border-red-300 bg-red-50 focus:border-red-500"
                              : "border-gray-300 focus:border-black"
                          }`}
                          placeholder="Confirm Password"
                          value={formData.password2}
                          onChange={handleChange}
                          required
                        />
                        {errors.password2 && (
                          <p className="mt-1 text-sm text-red-600">
                            {errors.password2[0]}
                          </p>
                        )}
                      </div>

                      {/* Submit Button */}
                      <div className="col-12">
                        <button
                          type="submit"
                          className="btn-book w-full rounded-xl bg-black px-6 py-3 font-medium text-white transition hover:opacity-90 disabled:opacity-50"
                          disabled={loading}
                        >
                          {loading ? (
                            <>
                              <i className="bi bi-hourglass-split me-2 inline-block animate-spin"></i>
                              Creating Account...
                            </>
                          ) : (
                            <>
                              <i className="bi bi-person-plus me-2"></i>
                              Create Account
                            </>
                          )}
                        </button>
                      </div>
                    </div>
                  </form>
                </div>

                {/* Login Link */}
                <div
                  className="emergency-info mt-6 text-center"
                  data-aos="fade-up"
                  data-aos-delay="500"
                >
                  <p className="text-sm text-gray-600">
                    Already have an account?{" "}
                    <Link
                      href="/login"
                      className="font-semibold text-black underline"
                    >
                      Sign In
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
