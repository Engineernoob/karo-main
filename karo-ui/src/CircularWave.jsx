import React from "react";
import { motion, AnimatePresence } from "framer-motion";

export default function CircularWave({ isActive }) {
  const ringCount = 3;
  const ringDelay = 0.6;

  const pulse = {
    scale: [0, 1, 1.5],
    opacity: [0.6, 0.3, 0],
    transition: { duration: 2, repeat: Infinity, ease: "easeOut" },
  };

  const ringStyle = {
    position: "absolute",
    width: 200,
    height: 200,
    border: "2px solid rgba(255,255,255,0.5)",
    borderRadius: "50%",
  };
  const coreStyle = {
    position: "relative",
    width: 48,
    height: 48,
    backgroundColor: "#fff",
    borderRadius: "50%",
    boxShadow: "0 0 20px rgba(255,255,255,0.7)",
  };
  const overlayStyle = {
    position: "fixed", top: 0, left: 0, right: 0, bottom: 0,
    display: "flex", alignItems: "center", justifyContent: "center",
    pointerEvents: "none", zIndex: 9998,
  };

  return (
    <AnimatePresence>
      {isActive && (
        <motion.div
          style={overlayStyle}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
        >
          {[...Array(ringCount)].map((_, i) => (
            <motion.div
              key={i}
              style={ringStyle}
              animate={pulse}
              transition={{ ...pulse.transition, delay: i * ringDelay }}
            />
          ))}
          <div style={coreStyle} />
        </motion.div>
      )}
    </AnimatePresence>
  );
}