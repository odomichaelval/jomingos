"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

// ── Types ────────────────────────────────────────────────────────────────────
type Stats = {
  total_patients: number;
  staff_count: number;
};

// ── API base URL (same as your lib/api.ts) ───────────────────────────────────
const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE || "http://127.0.0.1:8000/api";

export default function StatisticsPage() {
  const [stats, setStats] = useState<Stats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function fetchStats() {
      try {
        // No Authorization header — public endpoint
        const response = await fetch(`${API_BASE}/dashboard/stats/`, {
          method: "GET",
          headers: { "Content-Type": "application/json" },
        });

        if (!response.ok) {
          throw new Error(`Failed to fetch stats (${response.status})`);
        }

        const data: Stats = await response.json();
        if (!cancelled) setStats(data);
      } catch (err) {
        if (!cancelled)
          setError(err instanceof Error ? err.message : "Failed to load stats");
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    fetchStats();
    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <>
      {/* ── Page Title ── */}
      <div className="page-title">
        <br />
        <nav className="breadcrumbs">
          <div className="container">
            <ol>
              <li><Link href="/">Home</Link></li>
              <li className="current">Our Statistics</li>
            </ol>
          </div>
        </nav>
      </div>
      {/* End Page Title */}

      {/* ── Statistics Section ── */}
      <section id="service-details-2" className="service-details-2 section">
        <div className="container" data-aos="fade-up" data-aos-delay="100">
          <div className="row gy-4 mt-5">

            {/* ── Error State ── */}
            {error && (
              <div className="col-12">
                <div
                  style={{
                    background: "#fff0f0",
                    border: "1px solid #ffcccc",
                    borderRadius: "12px",
                    padding: "16px",
                    color: "#cc0000",
                    fontSize: "14px",
                  }}
                >
                  <i className="bi bi-exclamation-triangle me-2"></i>
                  {error}
                </div>
              </div>
            )}

            {/* ── Total Residents ── */}
            <div className="col-lg-6" data-aos="zoom-in" data-aos-delay="100">
              <div className="action-card primary">
                <div className="card-header">
                  <i className="bi bi-person-heart"></i>
                  <h1>
                    <div className="stat-item">
                      <div className="stat-number">
                        {loading ? (
                          <span style={{ fontSize: "16px", fontWeight: 400 }}>
                            Loading...
                          </span>
                        ) : (
                          <span>{stats?.total_patients ?? "—"}</span>
                        )}
                      </div>
                    </div>
                  </h1>
                  <div className="stat-label">Total Number of Residents</div>
                </div>
                <p>
                  Tracks the total number of residents using Jomingos to receive
                  healthcare assistance and care support from medical professionals.
                </p>
              </div>
            </div>

            {/* ── Total Medical Professionals ── */}
            <div className="col-lg-6" data-aos="zoom-in" data-aos-delay="200">
              <div className="action-card primary">
                <div className="card-header">
                  <i className="bi bi-person-badge"></i>
                  <h1>
                    <div className="stat-item">
                      <div className="stat-number">
                        {loading ? (
                          <span style={{ fontSize: "16px", fontWeight: 400 }}>
                            Loading...
                          </span>
                        ) : (
                          <span>{stats?.staff_count ?? "—"}</span>
                        )}
                      </div>
                    </div>
                  </h1>
                  <div className="stat-label">
                    Total Number of Medical Professionals
                  </div>
                </div>
                <p>
                  Tracks the total number of medical professionals providing care
                  through Jomingos.
                </p>
              </div>
            </div>

          </div>
        </div>
      </section>
      {/* /Statistics Section */}
    </>
  );
}
