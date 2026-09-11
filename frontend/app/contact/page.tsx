
"use client";
import Link from "next/link";

export default function ContactPage() {
  return (
    <>
      {/* ── Page Title ── */}
      <div className="page-title">
        <div className="heading">
          <div className="container">
            <div className="row d-flex justify-content-center text-center">
              <div className="col-lg-8">
                <h1 className="heading-title">Contact</h1>
                <p className="mb-0">
                  We&apos;re here to help. Contact the Jomingos team for support, enquiries,
                  partnerships, or more information about our care-home management solutions
                  and services.
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
              <li className="current">Contact</li>
            </ol>
          </div>
        </nav>
      </div>
      {/* End Page Title */}

      {/* ── Contact Section ── */}
      <section id="contact" className="contact section">
        <div className="container" data-aos="fade-up" data-aos-delay="100">
          <div className="row g-5">

            {/* ── Contact Info ── */}
            <div className="col-lg-5">
              <div className="contact-info-wrapper">

                <div className="contact-info-item" data-aos="fade-up" data-aos-delay="100">
                  <div className="info-icon">
                    <i className="bi bi-geo-alt"></i>
                  </div>
                  <div className="info-content">
                    <h3>Our Address</h3>
                    <p>Howard St, Sheffield City Centre, Sheffield S1 1WB</p>
                  </div>
                </div>

                <div className="contact-info-item" data-aos="fade-up" data-aos-delay="200">
                  <div className="info-icon">
                    <i className="bi bi-envelope"></i>
                  </div>
                  <div className="info-content">
                    <h3>Email Address</h3>
                    <p>info@jomingos.co.uk</p>
                    <p>contact@jomingos.co.uk</p>
                  </div>
                </div>

                <div className="contact-info-item" data-aos="fade-up" data-aos-delay="300">
                  <div className="info-icon">
                    <i className="bi bi-headset"></i>
                  </div>
                  <div className="info-content">
                    <h3>Call Us</h3>
                    <p>+1 (555) 987-6543</p>
                    <p>+1 (555) 123-4567</p>
                  </div>
                </div>

              </div>
            </div>

            {/* ── Google Map ── */}
            <div className="col-lg-7">
              <div
                className="container-fluid map-container"
                data-aos="fade-up"
                data-aos-delay="200"
              >
                <div className="map-overlay"></div>
                <iframe
                  src="https://www.google.com/maps?q=Howard+St,+Sheffield+City+Centre,+Sheffield+S1+1WB&output=embed"
                  width="100%"
                  height="500"
                  style={{ border: 0 }}
                  allowFullScreen
                  loading="lazy"
                  referrerPolicy="no-referrer-when-downgrade"
                ></iframe>
              </div>
            </div>

          </div>
        </div>
      </section>
      {/* /Contact Section */}
    </>
  );
}
