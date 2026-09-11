import Link from "next/link";

export default function Footer() {
  return (
    <footer id="footer" className="footer-16 footer position-relative">

      <div className="container">
        <div className="footer-main" data-aos="fade-up" data-aos-delay="100">
          <div className="row align-items-start">

            {/* ── Brand + Contact ── */}
            <div className="col-lg-5">
              <div className="brand-section">
                <Link href="/" className="logo d-flex align-items-center mb-4">
                  <span className="sitename">Jomingos</span>
                </Link>
                <p className="brand-description">
                  Care-home documentation made calm and organised. Dedicated to providing
                  exceptional healthcare that combines cutting-edge technology.
                </p>

                <div className="contact-info mt-5">
                  <div className="contact-item">
                    <i className="bi bi-geo-alt"></i>
                    <span>Howard St, Sheffield City Centre, Sheffield S1 1WB</span>
                  </div>
                  <div className="contact-item">
                    <i className="bi bi-telephone"></i>
                    <span>+1 (555) 987-6543</span>
                  </div>
                  <div className="contact-item">
                    <i className="bi bi-envelope"></i>
                    <span>contact@jomingos.co.uk</span>
                  </div>
                </div>
              </div>
            </div>

            {/* ── Footer Nav Columns ── */}
            <div className="col-lg-7">
              <div className="footer-nav-wrapper">
                <div className="row">

                  <div className="col-6 col-lg-3">
                    <div className="nav-column">
                      <h6>About</h6>
                      <nav className="footer-nav">
                        <a href="/about">About Us</a>
                        <a href="/services">Services</a>
                      </nav>
                    </div>
                  </div>

                  <div className="col-6 col-lg-3">
                    <div className="nav-column">
                      <h6>Services</h6>
                      <nav className="footer-nav">
                        <a href="/services">Care Note Taking</a>
                        <a href="/services">Record Care Medications</a>
                        <a href="/services">Track Care Vital Signs</a>
                      </nav>
                    </div>
                  </div>

                  <div className="col-6 col-lg-3">
                    <div className="nav-column">
                      <h6>Departments</h6>
                      <nav className="footer-nav">
                        <a href="/departments">Doctors</a>
                        <a href="/departments">Nurses</a>
                        <a href="/departments">Care Assistants</a>
                      </nav>
                    </div>
                  </div>

                  <div className="col-6 col-lg-3">
                    <div className="nav-column">
                      <h6>Connect</h6>
                      <nav className="footer-nav">
                        <a href="/contact">Contact Us</a>
                        <a href="/">Social Media</a>
                      </nav>
                    </div>
                  </div>

                </div>
              </div>
            </div>

          </div>
        </div>
      </div>

      {/* ── Footer Bottom ── */}
      <div className="footer-bottom">
        <div className="container">
          <div className="bottom-content" data-aos="fade-up" data-aos-delay="300">
            <div className="row align-items-center">

              <div className="col-lg-6">
                <div className="copyright">
                  <p>© <span className="sitename">Jomingos</span>. All rights reserved.</p>
                </div>
              </div>

              <div className="col-lg-6">
                <div className="legal-links">
                  <div className="credits">
                    Designed by <a href="#">Jomingos Computing</a>. Distributed by{" "}
                    <a href="#" target="_blank" rel="noopener noreferrer">
                      Aslam Jarwar &amp; Najam Hassan
                    </a>
                  </div>
                </div>
              </div>

            </div>
          </div>
        </div>
      </div>

    </footer>
  );
}
