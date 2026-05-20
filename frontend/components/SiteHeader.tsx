"use client";

import Link from "next/link";
import Image from "next/image";
import { usePathname } from "next/navigation";

export default function SiteHeader() {
  const pathname = usePathname();

  const isActive = (href: string) => pathname === href;

  return (
    <header id="header" className="header fixed-top">

      {/* ── Top Bar ── */}
      <div className="topbar d-flex align-items-center dark-background">
        <div className="container d-flex justify-content-center justify-content-md-between">

          <div className="contact-info d-flex align-items-center">
            <i className="bi bi-envelope d-flex align-items-center">
              <a href="mailto:contact@jomingos.co.uk">contact@jomingos.co.uk</a>
            </i>
          </div>

          <div className="social-links d-none d-md-flex align-items-center">
            <a href="#!" className="twitter"><i className="bi bi-twitter-x"></i></a>
            <a href="#!" className="facebook"><i className="bi bi-facebook"></i></a>
            <a href="#!" className="instagram"><i className="bi bi-instagram"></i></a>
            <a href="#!" className="linkedin"><i className="bi bi-linkedin"></i></a>
          </div>

        </div>
      </div>
      {/* End Top Bar */}

      {/* ── Branding + Nav ── */}
      <div className="branding d-flex align-items-center">
        <div className="container position-relative d-flex align-items-center justify-content-between">

          <Link href="/" className="logo d-flex align-items-center">
            <h1 className="sitename">
              <Image src="/img/logo.png" alt="Jomingos Logo" width={40} height={40} />
              Jomingos
            </h1>
          </Link>

          <nav id="navmenu" className="navmenu">
            <ul>
              <li>
                <Link href="/" className={isActive("/") ? "active" : ""}>Home</Link>
              </li>
              <li>
                <Link href="/about" className={isActive("/about") ? "active" : ""}>About</Link>
              </li>
              <li>
                <Link href="/services" className={isActive("/services") ? "active" : ""}>Services</Link>
              </li>
              <li>
                <Link href="/departments" className={isActive("/departments") ? "active" : ""}>Departments</Link>
              </li>
              <li>
                <Link href="/team" className={isActive("/team") ? "active" : ""}>Our Team</Link>
              </li>
              <li>
                <Link href="/contact" className={isActive("/contact") ? "active" : ""}>Contact</Link>
              </li>
              
              <li className="dropdown">
                <a href="#"><span>Get Started</span>{" "}<i className="bi bi-chevron-down toggle-dropdown"></i></a>

                <ul>
                  <li><Link href="https://jomingos.onrender.com/accounts/register" className={isActive("/register") ? "active" : ""}>
                    Register </Link>
                  </li>
                  <li> <Link href="https://jomingos.onrender.com/accounts/login" className={isActive("/login") ? "active" : ""} >
                    Login</Link>
                  </li>
                </ul>
              </li>


            </ul>

            {/* Mobile toggle — handled by main.js */}
            <i className="mobile-nav-toggle d-xl-none bi bi-list"></i>
          </nav>

        </div>
      </div>

    </header>
  );
}
