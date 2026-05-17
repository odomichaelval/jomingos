"use client";

import { useEffect, useRef, useState } from "react";

// ── Single animated counter ───────────────────────────────────────────────
interface CounterProps {
  end: number;
  duration?: number; // seconds
}

function AnimatedCounter({ end, duration = 2 }: CounterProps) {
  const [count, setCount] = useState(0);
  const [started, setStarted] = useState(false);
  const ref = useRef<HTMLSpanElement>(null);

  // Start counting only when element enters the viewport
  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && !started) {
          setStarted(true);
        }
      },
      { threshold: 0.3 }
    );

    if (ref.current) observer.observe(ref.current);
    return () => observer.disconnect();
  }, [started]);

  // Run the counter animation once started
  useEffect(() => {
    if (!started) return;

    let startTime: number | null = null;
    const totalMs = duration * 1000;

    const step = (timestamp: number) => {
      if (!startTime) startTime = timestamp;
      const progress = Math.min((timestamp - startTime) / totalMs, 1);
      setCount(Math.floor(progress * end));
      if (progress < 1) requestAnimationFrame(step);
    };

    requestAnimationFrame(step);
  }, [started, end, duration]);

  return <span ref={ref}>{count}</span>;
}

// ── Global initialiser — finds all purecounter elements and replaces them ─
export default function PureCounterInit() {
  useEffect(() => {
    const elements = document.querySelectorAll(".purecounter");

    elements.forEach((el) => {
      const end = parseInt(el.getAttribute("data-purecounter-end") || "0");
      const duration = parseInt(el.getAttribute("data-purecounter-duration") || "2");

      const observer = new IntersectionObserver(
        ([entry]) => {
          if (entry.isIntersecting) {
            let startTime: number | null = null;
            const totalMs = duration * 1000;

            const step = (timestamp: number) => {
              if (!startTime) startTime = timestamp;
              const progress = Math.min((timestamp - startTime) / totalMs, 1);
              el.textContent = String(Math.floor(progress * end));
              if (progress < 1) {
                requestAnimationFrame(step);
              }
            };

            requestAnimationFrame(step);
            observer.disconnect();
          }
        },
        { threshold: 0.3 }
      );

      observer.observe(el);
    });
  }, []);

  return null;
}

export { AnimatedCounter };
