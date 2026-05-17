import { Roboto, Montserrat, Lato } from "next/font/google";
import SiteHeader from "@/components/SiteHeader";
import SiteFooter from "@/components/SiteFooter";
import AOSInit from "@/components/AOSInit";
import PureCounterInit from "@/components/PureCounterInit";
import Script from "next/script";


// ── Google Fonts via next/font (replaces the <link> tags) ──────────────────
const roboto = Roboto({
  subsets: ["latin"],
  weight: ["100", "300", "400", "500", "700", "900"],
  style: ["normal", "italic"],
  variable: "--font-roboto",
  display: "swap",
});

const montserrat = Montserrat({
  subsets: ["latin"],
  weight: ["100", "200", "300", "400", "500", "600", "700", "800", "900"],
  style: ["normal", "italic"],
  variable: "--font-montserrat",
  display: "swap",
});

const lato = Lato({
  subsets: ["latin"],
  weight: ["100", "300", "400", "700", "900"],
  style: ["normal", "italic"],
  variable: "--font-lato",
  display: "swap",
});

export const metadata = {
  title: "Jomingos -Care-home documentation",
  description: "Care-home documentation made easy.",
  keywords: "care home, documentation, healthcare, residents",
  icons: {
    icon: "/img/favicon.png",
    apple: "/img/apple-touch-icon.png",
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html
      lang="en"
      className={`${roboto.variable} ${montserrat.variable} ${lato.variable}`}
    >
      <head>
        {/* Vendor CSS */}
        <link rel="stylesheet" href="/vendor/bootstrap/css/bootstrap.min.css" />
        <link rel="stylesheet" href="/vendor/bootstrap-icons/bootstrap-icons.css" />
        { /* <link rel="stylesheet" href="/vendor/aos/aos.css" /> */}
        <link rel="stylesheet" href="/vendor/glightbox/css/glightbox.min.css" />
        <link rel="stylesheet" href="/vendor/fontawesome-free/css/all.min.css" />
         {/*<link rel="stylesheet" href="/vendor/swiper/swiper-bundle.min.css" />*/}

        {/* Main CSS */}
        <link rel="stylesheet" href="/css/main.css" />
      </head>

      <body>


        <SiteHeader />

        {/* AOS & Pure Counter initialisation — imported from npm, not vendor folder */}
        <AOSInit />
        <PureCounterInit />
        
        <main className="main">{children}</main>

        <SiteFooter />

        {/* Scroll Top Button */}
        <a
          href="#!"
          id="scroll-top"
          className="scroll-top d-flex align-items-center justify-content-center"
        >
          <i className="bi bi-arrow-up-short"></i>
        </a>

        {/* ── Vendor JS (loaded after page, in order) ── */}
        <Script src="/vendor/bootstrap/js/bootstrap.bundle.min.js" strategy="beforeInteractive" />
        <Script src="/vendor/php-email-form/validate.js" strategy="afterInteractive" />
        {/* <Script src="/vendor/aos/aos.js" strategy="afterInteractive" /> */}
        <Script src="/vendor/glightbox/js/glightbox.min.js" strategy="afterInteractive" />
        {/* <Script src="/vendor/purecounter/purecounter_vanilla.js" strategy="afterInteractive" /> */}
        {/*<Script src="/vendor/swiper/swiper-bundle.min.js" strategy="afterInteractive" />*/}

        {/* Main JS */}
        <Script src="/js/main.js" strategy="afterInteractive" />
      </body>
    </html>
  );
}
