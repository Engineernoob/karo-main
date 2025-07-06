import React, { useState } from "react";
import CircularWave from "./CircularWave";

export default function App() {
  const [listening, setListening] = useState(false);

  return (
    <div
      style={{
        minHeight: "100vh",
        backgroundColor: "#1f2937",
        color: "#fff",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <button
        style={{
          marginBottom: 24,
          padding: "12px 24px",
          backgroundColor: "#2563eb",
          color: "#fff",
          border: "none",
          borderRadius: 8,
          cursor: "pointer",
        }}
        onClick={() => setListening((v) => !v)}
      >
        {listening ? "Stop Listening" : "Activate Karo"}
      </button>
      <CircularWave isActive={listening} />
    </div>
  );
}