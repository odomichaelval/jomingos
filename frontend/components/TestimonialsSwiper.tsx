"use client";

import { Swiper, SwiperSlide } from "swiper/react";
import { Autoplay, Pagination } from "swiper/modules";
import Image from "next/image";

// Swiper styles from npm
import "swiper/css";
import "swiper/css/pagination";

const testimonials = [
  {
    id: 1,
    stars: 5,
    text: "Jomingos has completely changed how our care team handles documentation. Recording care notes and medication updates is now fast, organised, and stress-free. The dashboard is clean and very easy to use.",
    img: "/img/person/person-m-9.webp",
    name: "Marcus Chen",
    role: "Care Home Manager",
  },
  {
    id: 2,
    stars: 5,
    text: "We needed a secure and reliable platform for tracking residents' daily activities and vital signs, and Jomingos delivered exactly that. Everything feels structured, calm, and professional.",
    img: "/img/person/person-f-5.webp",
    name: "Sarah Mitchell",
    role: "Senior Care Coordinator",
  },
  {
    id: 3,
    stars: 5,
    text: "Before Jomingos, our staff spent too much time on paperwork. Now we can focus more on residents while keeping records accurate and accessible. The secure access controls also give us peace of mind.",
    img: "/img/person/person-f-12.webp",
    name: "James Wilson",
    role: "Registered Nurse",
  },
  {
    id: 4,
    stars: 5,
    text: "Jomingos combines compassionate care with modern technology beautifully. The system is intuitive, responsive, and helps our team stay organised throughout every shift.",
    img: "/img/person/person-m-12.webp",
    name: "Emma Rodriguez",
    role: "Residential Care Supervisor",
  },
  {
    id: 5,
    stars: 4,
    text: "The medication tracking and patient monitoring features have improved our workflow significantly. Our carers love how simple it is to update records in real time without confusion.",
    img: "/img/person/person-m-13.webp",
    name: "David Kumar",
    role: "Healthcare Administrator",
  },
  {
    id: 6,
    stars: 5,
    text: "What stands out most about Jomingos is the balance between advanced technology and ease of use. It feels like a platform truly designed with care homes and residents in mind.",
    img: "/img/person/person-f-13.webp",
    name: "Sophia Lee",
    role: "Operations Director",
  },
];

export default function TestimonialsSwiper() {
  return (
    <Swiper
      modules={[Autoplay, Pagination]}
      loop={true}
      speed={600}
      autoplay={{ delay: 5000, disableOnInteraction: false }}
      pagination={{ clickable: true }}
      breakpoints={{
        320: { slidesPerView: 1, spaceBetween: 16 },
        768: { slidesPerView: 2, spaceBetween: 24 },
        1200: { slidesPerView: 3, spaceBetween: 24 },
      }}
      className="testimonials-14"
    >
      {testimonials.map((t) => (
        <SwiperSlide key={t.id}>
          <div className="testimonial-item">
            <div className="stars">
              {[...Array(t.stars)].map((_, i) => (
                <i key={i} className="bi bi-star-fill"></i>
              ))}
            </div>
            <p>{t.text}</p>
            <div className="profile">
              <Image
                src={t.img}
                className="testimonial-img"
                alt={t.name}
                width={60}
                height={60}
                loading="lazy"
              />
              <div className="info">
                <h4>
                  {t.name} <i className="bi bi-patch-check-fill"></i>
                </h4>
                <span>{t.role}</span>
              </div>
            </div>
          </div>
        </SwiperSlide>
      ))}

      <div className="swiper-pagination"></div>
    </Swiper>
  );
}
