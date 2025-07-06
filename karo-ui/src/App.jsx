import { useState } from "react";
import "./App.css";
import SiriOverlay from "./SiriOverlay";

export default function App() {
  const [isActive, setIsActive] = useState(false);

  return (
    <div className="h-screen bg-gray-900 text-white flex flex-col items-center justify-center">
      <button
        onClick={() => setIsActive(true)}
        className="mb-6 px-4 py-2 bg-blue-600 rounded hover:bg-blue-500"
      >
        Activate Karo
      </button>
      <SiriOverlay
        isActive={isActive}
        onCommand={(cmd) => {
          console.log("Command received:", cmd);
          setIsActive(false);
        }}
      />
    </div>
  );
}
