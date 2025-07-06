import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import CircularWave from "./CircularWave";

export default function App() {
  const [listening, setListening] = useState(false);

  const overlayStyle = {
    position: "fixed",
    inset: 0,
    backgroundColor: "rgba(0, 0, 0, 0.5)",
    zIndex: 9998,
  };

  const containerStyle = {
    minHeight: "100vh",
    backgroundColor: "#1f2937",
    color: "#fff",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    position: "relative",
    zIndex: 0,
  };

  const buttonStyle = {
    padding: "12px 24px",
    backgroundColor: "#2563eb",
    color: "#fff",
    border: "none",
    borderRadius: 8,
    cursor: "pointer",
    position: "relative",
    zIndex: 9999,
  };

  return (
    <>
      {listening && <div style={overlayStyle} />}
      <div style={containerStyle}>
        <button
          style={buttonStyle}
          onClick={() => setListening((v) => !v)}
        >
          {listening ? "Stop Listening" : "Activate Karo"}
        </button>
        <CircularWave isActive={listening} />
      </div>
    </>
  );
}