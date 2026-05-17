"use client";

import { useState } from "react";
import Image from "next/image";
import Link from "next/link";

const departments = [
  {
    id: "doctor",
    label: "Doctor",
    delay: "100",
    image: "/img/health/staff-1.webp",
    imageAlt: "Doctors Department",
    title: "The Doctors Department",
    description:
      "Our Doctors Department focuses on resident health assessments, medical supervision, diagnosis, and treatment planning to ensure high-quality healthcare and resident wellbeing.",
    services: [
      {
        icon: "fas fa-brain",
        title: "Health Assessments",
        desc: "Conduct comprehensive medical evaluations and monitor residents' overall health conditions.",
      },
      {
        icon: "fas fa-wave-square",
        title: "Treatment Planning",
        desc: "Develop personalised treatment and healthcare plans tailored to residents' needs.",
      },
      {
        icon: "fas fa-stethoscope",
        title: "Health Monitoring",
        desc: "Track medical progress and support early detection of health concerns.",
      },
      {
        icon: "fas fa-file-medical",
        title: "Medical Supervision",
        desc: "Provide professional oversight for medications, healthcare procedures, and resident care.",
      },
    ],
  },
  {
    id: "nurse",
    label: "Nurse",
    delay: "150",
    image: "/img/health/staff-2.webp",
    imageAlt: "Nurses Department",
    title: "The Nurses Department",
    description:
      "Our Nurses Department provides daily clinical support through medication administration, vital signs monitoring, and compassionate resident care.",
    services: [
      {
        icon: "fas fa-cut",
        title: "Medication Administration",
        desc: "Manage and record medications accurately to ensure resident safety.",
      },
      {
        icon: "fas fa-tools",
        title: "Vital Signs Monitoring",
        desc: "Monitor temperature, blood pressure, pulse, and other important health indicators.",
      },
      {
        icon: "fas fa-shield-alt",
        title: "Daily Clinical Care",
        desc: "Support residents with routine healthcare and wellbeing monitoring.",
      },
      {
        icon: "fas fa-clock",
        title: "Care Documentation",
        desc: "Maintain organised and accurate nursing records and healthcare notes.",
      },
    ],
  },
  {
    id: "care",
    label: "Care Assistant",
    delay: "200",
    image: "/img/health/pediatrics-4.webp",
    imageAlt: "Care Assistants Department",
    title: "The Care Assistants Department",
    description:
      "Our Care Assistants Department supports residents with personal care, companionship, and daily living activities while promoting comfort and dignity.",
    services: [
      {
        icon: "far fa-smile",
        title: "Personal Care Support",
        desc: "Assist residents with hygiene, dressing, feeding, and mobility needs.",
      },
      {
        icon: "fas fa-tooth",
        title: "Daily Activity Assistance",
        desc: "Help residents participate in daily routines and activities comfortably.",
      },
      {
        icon: "fas fa-star",
        title: "Routine Care Recording",
        desc: "Document daily observations and resident activities accurately.",
      },
      {
        icon: "fas fa-cog",
        title: "Resident Companionship",
        desc: "Provide emotional support and meaningful interaction for residents.",
      },
    ],
  },
  {
    id: "admin",
    label: "Administrator",
    delay: "250",
    image: "/img/health/admin.jpg",
    imageAlt: "Administrator Department",
    title: "The Administrator Department",
    description:
      "Our Administrator Department manages system operations, staff coordination, resident records, and overall care-home administration to ensure smooth and organised daily activities.",
    services: [
      {
        icon: "fas fa-eye",
        title: "Staff Management",
        desc: "Coordinate staff roles, schedules, and departmental operations efficiently.",
      },
      {
        icon: "fas fa-camera",
        title: "Resident Records",
        desc: "Manage and maintain secure resident information and care documentation.",
      },
      {
        icon: "fas fa-bolt",
        title: "System Oversight",
        desc: "Monitor platform activities, user access, and operational workflows.",
      },
      {
        icon: "fas fa-prescription-bottle",
        title: "Reporting & Analytics",
        desc: "Generate reports and insights to support informed decision-making and care-home management.",
      },
    ],
  },
];

export default function DepartmentsPage() {
  const [activeTab, setActiveTab] = useState("doctor");

  const activeDepart = departments.find((d) => d.id === activeTab)!;

  return (
    <>
      {/* ── Page Title ── */}
      <div className="page-title">
        <div className="heading">
          <div className="container">
            <div className="row d-flex justify-content-center text-center">
              <div className="col-lg-8">
                <h1 className="heading-title">Departments</h1>
                <p className="mb-0">
                  Jomingos are organised into teams of healthcare professionals working together
                  to provide efficient, compassionate, and high-quality care for residents.
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
              <li className="current">Departments</li>
            </ol>
          </div>
        </nav>
      </div>
      {/* End Page Title */}

      {/* ── Departments Tabs Section ── */}
      <section id="departments-tabs" className="departments-tabs section">
        <div className="container" data-aos="fade-up" data-aos-delay="100">
          <div className="medical-specialties">
            <div className="row">

              {/* ── Tab Navigation ── */}
              <div className="col-12">
                <div className="specialty-navigation">
                  <div className="nav nav-pills d-flex" role="tablist">
                    {departments.map((dept) => (
                      <button
                        key={dept.id}
                        className={`nav-link department-tab${activeTab === dept.id ? " active" : ""}`}
                        onClick={() => setActiveTab(dept.id)}
                        role="tab"
                        aria-selected={activeTab === dept.id}
                       
                      >
                        {dept.label}
                      </button>
                    ))}
                  </div>
                </div>
              </div>

              {/* ── Tab Content ── */}
              <div className="col-12">
                <div className="tab-content department-content" data-aos="fade-up" data-aos-delay="500">
                  <div className="tab-pane fade show active" role="tabpanel">
                    <div className="row department-layout">

                      {/* Image */}
                      <div className="col-lg-4 order-lg-2">
                        <div className="department-image">
                          <Image
                            src={activeDepart.image}
                            alt={activeDepart.imageAlt}
                            className="img-fluid"
                            width={400}
                            height={450}
                          />
                        </div>
                      </div>

                      {/* Info */}
                      <div className="col-lg-8 order-lg-1">
                        <div className="department-info">
                          <h2 className="department-title">{activeDepart.title}</h2>
                          <p className="department-description">{activeDepart.description}</p>

                          <div className="row mt-4">
                            {activeDepart.services.map((service, i) => (
                              <div key={i} className="col-md-6">
                                <div className="service-item">
                                  <div className="service-icon">
                                    <i className={service.icon}></i>
                                  </div>
                                  <div className="service-content">
                                    <h4>{service.title}</h4>
                                    <p>{service.desc}</p>
                                  </div>
                                </div>
                              </div>
                            ))}
                          </div>

                        </div>
                      </div>

                    </div>
                  </div>
                </div>
              </div>

            </div>
          </div>
        </div>
      </section>
      {/* /Departments Tabs Section */}
    </>
  );
}
