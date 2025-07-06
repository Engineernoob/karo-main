// src/SiriOverlay.jsx
import { useEffect, useState } from "react";
import { motion, useAnimation } from "framer-motion";

export default function SiriOverlay({ isActive, onCommand }) {
  const [inputText, setInputText] = useState("");
  const controls = useAnimation();

  useEffect(() => {
    if (isActive) {
      controls.start({
        scale: [1, 1.2, 1],
        transition: { repeat: Infinity, duration: 1.5 },
      });
    } else {
      controls.stop();
    }
  }, [isActive, controls]);

  const handleSubmit = (e) => {
    e.preventDefault();
    onCommand(inputText);
    setInputText("");
  };

  return (
    <div className="fixed inset-0 flex items-center justify-center pointer-events-none">
      {isActive && (
        <motion.div
          animate={controls}
          className="bg-white bg-opacity-20 backdrop-blur-lg rounded-full w-64 h-64 flex items-center justify-center shadow-2xl p-4 pointer-events-auto"
        >
          <form onSubmit={handleSubmit} className="w-full flex flex-col items-center">
            <input
              type="text"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="What can I help you with?"
              className="bg-transparent border-b border-white placeholder-white text-white w-full text-center focus:outline-none px-2 pb-1 mb-2"
            />
            <motion.div className="flex space-x-1 mt-2">
              {[...Array(5)].map((_, i) => (
                <motion.div
                  key={i}
                  className="bg-white rounded-full w-2 h-2"
                  animate={{ y: [0, -10, 0] }}
                  transition={{ repeat: Infinity, delay: i * 0.2, duration: 1 }}
                />
              ))}
            </motion.div>
          </form>
        </motion.div>
      )}
    </div>
  );
}