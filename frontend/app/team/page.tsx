import Image from "next/image";
import Link from "next/link";

const team = [
  {
    id: 1,
    delay: "100",
    image: "/img/health/joshua.jpg",
    name: "Joshua Onwuka",
    role: "Software Developer",
    bio: "I build software systems that solve real life problems people have while saving time and money. People stopped believing technology can fix AI-powered systems that actually work in healthcare.",
    linkedin: "https://www.linkedin.com/in/joshua-onwuka-54a833256/",
  },
  {
    id: 2,
    delay: "200",
    image: "/img/health/michael.jpg",
    name: "Michael Odo",
    role: "Software Developer",
    bio: "I focus on creating efficient, scalable web solutions that meet today\u2019s  dynamic business needs. With a passion for innovation, I strive to deliver high-quality software that exceeds client expectations.",
    linkedin: "https://www.linkedin.com/in/odomichael/",
  },
];

export default function TeamPage() {
  return (
    <>
      {/* ── Page Title ── */}
      <div className="page-title">
        <div className="heading">
          <div className="container">
            <div className="row d-flex justify-content-center text-center">
              <div className="col-lg-8">
                <h1 className="heading-title">Team</h1>
                <p className="mb-0">
                  Meet the dedicated professionals behind Jomingos — a passionate team committed
                  to improving care-home management through compassionate healthcare solutions,
                  secure technology, and organised digital experiences.
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
              <li className="current">Team</li>
            </ol>
          </div>
        </nav>
      </div>
      {/* End Page Title */}

      {/* ── Team Section ── */}
      <section id="doctors" className="doctors section">
        <div className="container" data-aos="fade-up" data-aos-delay="100">
          <div className="row gy-4">

            {team.map((member) => (
              <div
                key={member.id}
                className="col-lg-6 col-md-6"
                data-aos="fade-up"
                data-aos-delay={member.delay}
              >
                <div className="doctor-card">
                  <div className="doctor-image">
                    <Image
                      src={member.image}
                      alt={member.name}
                      className="img-fluid"
                      width={400}
                      height={400}
                    />
                  </div>
                  <div className="doctor-content">
                    <h4>{member.name}</h4>
                    <span className="specialty">{member.role}</span>
                    <p>{member.bio}</p>
                    <a
                      href={member.linkedin}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="btn-appointment"
                    >
                      Contact Me
                    </a>
                  </div>
                </div>
              </div>
            ))}

          </div>
        </div>
      </section>
      {/* /Team Section */}
    </>
  );
}
