"use client";

import Image from "next/image";
import Link from "next/link";
import TestimonialsSwiper from "@/components/TestimonialsSwiper";

export default function HomePage() {
  return (
    <>
      {/* ── Hero Section ── */}
      <section id="hero" className="hero section">
        <div className="container" data-aos="fade-up" data-aos-delay="100">
          <div className="row align-items-center">

            {/* Left Column */}
            <div className="col-lg-6">
              <div className="hero-content">

                {/* Trust Badges */}
                <div className="trust-badges mb-4" data-aos="fade-right" data-aos-delay="200">
                  <div className="badge-item">
                    <i className="bi bi-shield-check"></i>
                    <span>Accredited</span>
                  </div>
                  <div className="badge-item">
                    <i className="bi bi-emoji-smile"></i>
                    <span>Easy to use</span>
                  </div>
                  <div className="badge-item">
                    <i className="bi bi-star-fill"></i>
                    <span>4.9/5 Rating</span>
                  </div>
                </div>

                <h1 data-aos="fade-right" data-aos-delay="300">
                  <span className="highlight">Care-home documentation</span> made calm and organised.
                </h1>

                <p className="hero-description" data-aos="fade-right" data-aos-delay="400">
                  Jomingos helps staff record care notes, track medications and vital signs,
                  and monitor patient activity — with secure access controls and a clean
                  dashboard experience.
                </p>

                {/* Stats */}
                <div className="hero-stats mb-4" data-aos="fade-right" data-aos-delay="500">
                  <div className="stat-item">
                    <h3>
                     500+
                    </h3>
                    <p>Happy Clients</p>
                  </div>
                  <div className="stat-item">
                    <h3>
                      20+
                    </h3>
                    <p>Trusted Global Partners</p>
                  </div>
                  <div className="stat-item">
                    <h3>
                      50+
                    </h3>
                    <p>Useful Tools</p>
                  </div>
                </div>

                {/* CTA Buttons */}
                <div className="hero-actions" data-aos="fade-right" data-aos-delay="600">
                  <Link href="http://127.0.0.1:8000/" className="btn btn-primary">Login</Link>
                  <Link href="/contact" className="btn btn-outline">Contact Us</Link>
                </div>

                {/* Emergency Contact */}
                <div className="emergency-contact" data-aos="fade-right" data-aos-delay="700">
                  <div className="emergency-icon">
                    <i className="bi bi-telephone-fill"></i>
                  </div>
                  <div className="emergency-info">
                    <small>Emergency Hotline</small>
                    <strong>+1 (555) 911-2468</strong>
                  </div>
                </div>

              </div>
            </div>

            {/* Right Column — Hero Visual */}
            <div className="col-lg-6">
              <div className="hero-visual" data-aos="fade-left" data-aos-delay="400">
                <div className="main-image">
                  <Image
                    src="/img/health/staff-10.webp"
                    alt="Modern Healthcare Facility"
                    className="img-fluid"
                    width={600}
                    height={500}
                  />
                  {/* Floating Card — Appointment */}
                  <div className="floating-card appointment-card">
                    <div className="card-icon">
                      <i className="bi bi-calendar-check"></i>
                    </div>
                    <div className="card-content">
                      <h6>Room 102 Resident</h6>
                      <p>Needs your attention</p>
                      <small>Dr. Sarah Johnson</small>
                    </div>
                  </div>
                  {/* Floating Card — Rating */}
                  <div className="floating-card rating-card">
                    <div className="card-content">
                      <div className="rating-stars">
                        <i className="bi bi-star-fill"></i>
                        <i className="bi bi-star-fill"></i>
                        <i className="bi bi-star-fill"></i>
                        <i className="bi bi-star-fill"></i>
                        <i className="bi bi-star-fill"></i>
                      </div>
                      <h6>4.9/5</h6>
                      <small>1,234 Reviews</small>
                    </div>
                  </div>
                </div>
                {/* Background Elements */}
                <div className="background-elements">
                  <div className="element element-1"></div>
                  <div className="element element-2"></div>
                  <div className="element element-3"></div>
                </div>
              </div>
            </div>

          </div>
        </div>
        
      </section>
      {/* /Hero Section */}

      {/* ── Home About Section ── */}
      <section id="home-about" className="home-about section">
        <div className="container" data-aos="fade-up" data-aos-delay="100">
          <div className="row align-items-center">

            {/* Left — Content */}
            <div className="col-lg-6 mb-5 mb-lg-0" data-aos="fade-right" data-aos-delay="200">
              <div className="about-content">
                <h2 className="section-heading">Compassionate Care, Advanced Technology</h2>
                <p className="lead-text">
                  We are dedicated to providing exceptional healthcare that combines
                  cutting-edge technology with the personal touch our clients deserve.
                </p>
                <p>
                  We maintain the highest standards of medical software technology excellence
                  while fostering an environment of trust and healing. Our platform is designed
                  to demonstrate a modern, multi-tier architecture: with secure authentication
                  for our clients and their residents.
                </p>
                {/* Stats Grid */}
                <div className="stats-grid">
                  <div className="stat-item">
                    <div className="stat-number " >15000</div>
                    <div className="stat-label">Residents Served</div>
                  </div>
                  <div className="stat-item">
                    <div className="stat-number " >5</div>
                    <div className="stat-label">Years of Excellence</div>
                  </div>
                  <div className="stat-item">
                    <div className="stat-number " >500</div>
                    <div className="stat-label">Medical Specialists</div>
                  </div>
                </div>
                <div className="cta-section">
                  <Link href="/statistics" className="btn-primary">Platform Statistics</Link>
                </div>
              </div>
            </div>

            {/* Right — Visual */}
            <div className="col-lg-6" data-aos="fade-left" data-aos-delay="300">
              <div className="about-visual">
                <div className="main-image">
                  <Image
                    src="/img/health/facilities-9.jpg"
                    alt="Modern medical facility"
                    className="img-fluid"
                    width={600}
                    height={450}
                  />
                </div>
                <div className="floating-card">
                  <div className="card-content">
                    <div className="icon">
                      <i className="bi bi-heart-pulse"></i>
                    </div>
                    <div className="card-text">
                      <h4>24/7 Technical Support</h4>
                      <p>Always here when you need us most</p>
                    </div>
                  </div>
                </div>
                <div className="experience-badge">
                  <div className="badge-content">
                    <span className="years">5+</span>
                    <span className="text">Years of Trusted Care</span>
                  </div>
                </div>
              </div>
            </div>

          </div>
        </div>
      </section>
      {/* /Home About Section */}

      {/* ── Featured Testimonials Section ── */}
      <section id="featured-testimonials" className="featured-testimonials section">
        <div className="container" data-aos="fade-up" data-aos-delay="100">
          {/* React Swiper component — handles carousel natively */}
          <TestimonialsSwiper />
        </div>
      </section>
      {/* /Featured Testimonials Section */}

      {/* ── Call To Action Section ── */}
      <section id="call-to-action" className="call-to-action section light-background">
        <div className="container" data-aos="fade-up" data-aos-delay="100">

          <div className="hero-content">
            <div className="row align-items-center">
              <div className="col-lg-6">
                <div className="content-wrapper" data-aos="fade-up" data-aos-delay="200">
                  <h1>Excellence in Medical Care Technology</h1>
                  <p>Our platform combines advanced healthcare technology with a clean and
                    intuitive user experience to reduce paperwork stress, improve communication,
                    and enhance the quality of resident care.</p>
                  <div className="cta-wrapper">
                    <Link href="/register" className="primary-cta">
                      <span>Get Started</span>
                      <i className="bi bi-arrow-right"></i>
                    </Link>
                  </div>
                </div>
              </div>
              <div className="col-lg-6">
                <div className="image-container" data-aos="fade-left" data-aos-delay="300">
                  <Image
                    src="/img/health/facilities-9.webp"
                    alt="Medical Excellence"
                    className="img-fluid"
                    width={600}
                    height={450}
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Features */}
          <div className="features-section">
            <div className="row g-0">
              <div className="col-lg-4">
                <div className="feature-block" data-aos="fade-up" data-aos-delay="200">
                  <div className="feature-icon"><i className="bi bi-shield-check"></i></div>
                  <h3>Advanced Technology</h3>
                  <p>Models capture healthcare data using Python. REST endpoints are documented with Swagger/ReDoc.</p>
                </div>
              </div>
              <div className="col-lg-4">
                <div className="feature-block" data-aos="fade-up" data-aos-delay="300">
                  <div className="feature-icon"><i className="bi bi-clock"></i></div>
                  <h3>24/7 Availability</h3>
                  <p>Technical support is available around the clock to assist you with any questions or issues.</p>
                </div>
              </div>
              <div className="col-lg-4">
                <div className="feature-block" data-aos="fade-up" data-aos-delay="400">
                  <div className="feature-icon"><i className="bi bi-people"></i></div>
                  <h3>Expert Team</h3>
                  <p>Our team of healthcare professionals and technical experts is dedicated to providing the best support.</p>
                </div>
              </div>
            </div>
          </div>

          {/* Contact Block */}
          <div className="contact-block">
            <div className="row">
              <div className="col-lg-8">
                <div className="contact-content" data-aos="fade-up" data-aos-delay="200">
                  <h2>Need Immediate Assistance?</h2>
                  <p>Our emergency response team is available around the clock to provide immediate support when you need it most.</p>
                </div>
              </div>
              <div className="col-lg-4">
                <div className="contact-actions" data-aos="fade-up" data-aos-delay="300">
                  <a href="tel:5551234567" className="emergency-call">
                    <i className="bi bi-telephone"></i>
                    <span>(555) 123-4567</span>
                  </a>
                  <Link href="/contact" className="contact-link">Find Location</Link>
                </div>
              </div>
            </div>
          </div>

        </div>
      </section>
      {/* /Call To Action Section */}
    </>
  );
}
