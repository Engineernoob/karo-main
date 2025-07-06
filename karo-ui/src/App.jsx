import { useState } from "react";
import "./App.css";
import CircularWave from "./CircularWave";

export default function App() {
  const [listening, setListening] = useState(false);

  return (
    <div className="h-screen bg-gray-900 text-white flex flex-col items-center justify-center">
      <button
        onClick={() => setListening((v) => !v)}
        className="mb-6 px-4 py-2 bg-blue-600 rounded hover:bg-blue-500"
      >
        {listening ? "Stop Listening" : "Activate Karo"}
      </button>
      <CircularWave isActive={listening} />
    </div>
  );
}
