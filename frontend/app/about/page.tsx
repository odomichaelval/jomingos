import Image from "next/image";
import Link from "next/link";

export default function AboutPage() {
  return (
    <>
      {/* ── Page Title ── */}
      <div className="page-title">
        <div className="heading">
          <div className="container">
            <div className="row d-flex justify-content-center text-center">
              <div className="col-lg-8">
                <h1 className="heading-title">About</h1>
                <p className="mb-0">
                  A modern care-home management platform built to simplify documentation,
                  improve healthcare monitoring, and support compassionate caregiving through
                  secure and intuitive technology.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Breadcrumb */}
        <nav className="breadcrumbs">
          <div className="container">
            <ol>
              <li><Link href="/">Home</Link></li>
              <li className="current">About</li>
            </ol>
          </div>
        </nav>
      </div>
      {/* End Page Title */}

      {/* ── About Section ── */}
      <section id="about" className="about section">
        <div className="container" data-aos="fade-up" data-aos-delay="100">
          <div className="row align-items-center">

            {/* Left — Content */}
            <div className="col-lg-6" data-aos="fade-right" data-aos-delay="100">
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
                    <div
                      className="stat-number purecounter"
                      data-purecounter-start="0"
                      data-purecounter-end="15000"
                      data-purecounter-duration="1"
                    >15000</div>
                    <div className="stat-label">Residents Served</div>
                  </div>
                  <div className="stat-item">
                    <div
                      className="stat-number purecounter"
                      data-purecounter-start="0"
                      data-purecounter-end="5"
                      data-purecounter-duration="1"
                    >5</div>
                    <div className="stat-label">Years of Excellence</div>
                  </div>
                  <div className="stat-item">
                    <div
                      className="stat-number purecounter"
                      data-purecounter-start="0"
                      data-purecounter-end="500"
                      data-purecounter-duration="1"
                    >500</div>
                    <div className="stat-label">Medical Specialists</div>
                  </div>
                </div>
              </div>
            </div>

            {/* Right — Images */}
            <div className="col-lg-6" data-aos="fade-left" data-aos-delay="200">
              <div className="image-wrapper">
                <Image
                  src="/img/health/facilities-6.webp"
                  className="img-fluid main-image"
                  alt="Healthcare facility"
                  width={600}
                  height={450}
                />
                <div className="floating-image" data-aos="zoom-in" data-aos-delay="400">
                  <Image
                    src="/img/health/staff-8.webp"
                    className="img-fluid"
                    alt="Medical team"
                    width={250}
                    height={200}
                  />
                </div>
              </div>
            </div>

          </div>

          {/* ── Core Values ── */}
          <div className="values-section" data-aos="fade-up" data-aos-delay="300">
            <div className="row">
              <div className="col-lg-12 text-center">
                <h3>Our Core Values</h3>
                <p className="section-description">
                  These principles guide everything we do in our commitment to exceptional healthcare.
                </p>
              </div>
            </div>

            <div className="row">

              <div className="col-lg-3 col-md-6" data-aos="fade-up" data-aos-delay="100">
                <div className="value-item">
                  <div className="value-icon">
                    <i className="bi bi-heart-pulse"></i>
                  </div>
                  <h4>Compassion</h4>
                  <p>Providing care with empathy and understanding for every resident&apos;s unique needs and circumstances.</p>
                </div>
              </div>

              <div className="col-lg-3 col-md-6" data-aos="fade-up" data-aos-delay="200">
                <div className="value-item">
                  <div className="value-icon">
                    <i className="bi bi-shield-check"></i>
                  </div>
                  <h4>Excellence</h4>
                  <p>Maintaining the highest standards of medical care through continuous learning and innovation.</p>
                </div>
              </div>

              <div className="col-lg-3 col-md-6" data-aos="fade-up" data-aos-delay="300">
                <div className="value-item">
                  <div className="value-icon">
                    <i className="bi bi-people"></i>
                  </div>
                  <h4>Integrity</h4>
                  <p>Building trust through honest communication and ethical practices in all our interactions.</p>
                </div>
              </div>

              <div className="col-lg-3 col-md-6" data-aos="fade-up" data-aos-delay="400">
                <div className="value-item">
                  <div className="value-icon">
                    <i className="bi bi-lightbulb"></i>
                  </div>
                  <h4>Innovation</h4>
                  <p>Embracing cutting-edge technology and treatments to improve residents outcomes.</p>
                </div>
              </div>

            </div>
          </div>
          {/* End Values Section */}

        </div>
      </section>
      {/* /About Section */}
    </>
  );
}
