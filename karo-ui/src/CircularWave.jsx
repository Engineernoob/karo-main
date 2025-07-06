// src/CircularWave.jsx
import React from "react";
import { motion } from "framer-motion";

export default function CircularWave({ isActive }) {
  if (!isActive) return null;

  // Animation variant for each ring
  const ring = {
    initial: { scale: 0, opacity: 0.8 },
    animate: { scale: [0, 1, 1.5], opacity: [0.8, 0.4, 0], transition: { duration: 2, repeat: Infinity, ease: "easeOut" } }
  };

  const ringCount = 3;
  const ringDelay = 0.6;

  // Shared styles
  const ringStyle = {
    position: "absolute",
    width: 192,
    height: 192,
    border: "2px solid rgba(255,255,255,0.8)",
    borderRadius: "50%",
  };
  const coreStyle = {
    position: "relative",
    width: 48,
    height: 48,
    backgroundColor: "#fff",
    borderRadius: "50%",
    boxShadow: "0 0 10px rgba(255,255,255,0.8)",
  };

  return (
    <div
      style={{
        position: "fixed",
        top: 0, left: 0, right: 0, bottom: 0,
        display: "flex", alignItems: "center", justifyContent: "center",
        pointerEvents: "none", zIndex: 9999,
      }}
    >
      {[...Array(ringCount)].map((_, i) => (
        <motion.div
          key={i}
          style={ringStyle}
          variants={ring}
          initial="initial"
          animate="animate"
          transition={{ ...ring.animate.transition, delay: i * ringDelay }}
        />
      ))}
      <div style={coreStyle} />
    </div>
  );
}