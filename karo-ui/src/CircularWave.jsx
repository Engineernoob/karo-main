// src/CircularWave.jsx
import { useEffect } from "react";
import { motion, useAnimation } from "framer-motion";

const ringCount = 3;
const ringDelay = 0.5; // seconds between each ring start

export default function CircularWave({ isActive }) {
  const controls = useAnimation();

  useEffect(() => {
    if (isActive) {
      controls.start(i => ({
        scale: [0, 1, 1.5],
        opacity: [1, 0.6, 0],
        transition: {
          delay: i * ringDelay,
          loop: Infinity,
          duration: ringDelay * ringCount,
          ease: "easeOut"
        }
      }));
    } else {
      controls.stop();
    }
  }, [isActive, controls]);

  if (!isActive) return null;

  return (
    <div className="fixed inset-0 flex items-center justify-center pointer-events-none">
      {/* Render multiple rings */}
      {Array.from({ length: ringCount }).map((_, i) => (
        <motion.div
          key={i}
          custom={i}
          animate={controls}
          className="absolute rounded-full border-2 border-white opacity-80 w-48 h-48"
        />
      ))}
      {/* Inner core */}
      <div className="relative rounded-full bg-white w-12 h-12" />
    </div>
  );
}