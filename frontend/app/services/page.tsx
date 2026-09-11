"use client";

import Image from "next/image";
import Link from "next/link";

const services = [
  {
    id: 1,
    delay: "200",
    image: "/img/health/cardiology-2.jpg",
    alt: "Resident Management",
    title: "Resident Management",
    description: "Efficiently manage resident profiles, care plans, and personal records in one secure place.",
    features: ["Resident Profiles", "Medical history storage"],
    btn: "Activity monitoring",
  },
  {
    id: 2,
    delay: "250",
    image: "/img/health/neurology-3.jpg",
    alt: "Care Notes Documentation",
    title: "Care Notes Documentation",
    description: "Comprehensive documentation of resident care activities, ensuring all information is accurately recorded and easily accessible.",
    features: ["Detailed Care Notes", "Care Plan"],
    btn: "Real-time documentation",
  },
  {
    id: 3,
    delay: "300",
    image: "/img/health/laboratory-3.webp",
    alt: "Medication Management",
    title: "Medication Management",
    description: "Comprehensive management of resident medications, including prescribing, dispensing, and monitoring for optimal therapeutic outcomes.",
    features: ["Medication Reconciliation", "Dosage Optimization"],
    btn: "Dosage monitoring",
  },
  {
    id: 4,
    delay: "350",
    image: "/img/health/cardiology-2.webp",
    alt: "Vital Signs Monitoring",
    title: "Vital Signs Monitoring",
    description: "Continuous monitoring of vital signs to ensure the health and well-being of residents.",
    features: ["Blood Pressure Checks", "Heart Rate Monitoring"],
    btn: "Health trend visibility",
  },
  {
    id: 5,
    delay: "400",
    image: "/img/health/emergency-2.jpg",
    alt: "Secure Authentication",
    title: "Secure Authentication",
    description: "Robust security measures to ensure only authorized personnel have access to sensitive patient information and systems.",
    features: ["Multi-Factor Authentication", "Role-Based Access Control"],
    btn: "Secure data handling",
  },
  {
    id: 6,
    delay: "450",
    image: "/img/health/laboratory-3.jpg",
    alt: "Dashboard & Reporting",
    title: "Dashboard & Reporting",
    description: "Comprehensive dashboard and reporting tools to provide insights into resident care, medication management, and overall facility performance.",
    features: ["Care Insights", "Medication Tracking"],
    btn: "Clean dashboard experience",
  },
];

export default function ServicesPage() {
  return (
    <>
      {/* ── Page Title ── */}
      <div className="page-title">
        <div className="heading">
          <div className="container">
            <div className="row d-flex justify-content-center text-center">
              <div className="col-lg-8">
                <h1 className="heading-title">Services</h1>
                <p className="mb-0">
                  Our services are built to support modern care homes with secure documentation,
                  medication management, resident monitoring, and organised healthcare workflows —
                  helping caregivers focus more on people and less on paperwork.
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
              <li className="current">Services</li>
            </ol>
          </div>
        </nav>
      </div>
      {/* End Page Title */}

      {/* ── Services Section ── */}
      <section id="services" className="services section">
        <div className="container" data-aos="fade-up" data-aos-delay="100">
          <div className="row gy-4">

            {services.map((service) => (
              <div
                key={service.id}
                className="col-lg-4 col-md-6"
                data-aos="fade-up"
                data-aos-delay={service.delay}
              >
                <div className="service-item">
                  <div className="service-image">
                    <Image
                      src={service.image}
                      alt={service.alt}
                      className="img-fluid"
                      width={400}
                      height={250}
                    />
                  </div>
                  <div className="service-content">
                    <h3>{service.title}</h3>
                    <p>{service.description}</p>
                    <div className="service-features">
                      {service.features.map((feature, i) => (
                        <span key={i} className="feature-item">
                          <i className="fas fa-check"></i> {feature}
                        </span>
                      ))}
                    </div>
                    <a className="service-btn">
                      <span>{service.btn}</span>
                    </a>
                  </div>
                </div>
              </div>
            ))}

          </div>
        </div>
      </section>
      {/* /Services Section */}
    </>
  );
}
