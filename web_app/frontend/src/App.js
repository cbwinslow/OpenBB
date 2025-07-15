import React from "react";
import Strategies from "./components/Strategies";
import Chatbot from "./components/Chatbot";
import Trading from "./components/Trading";
import "./App.css";

/**
 * Main application component that renders the Trading, Strategies, and Chatbot sections.
 * Serves as the top-level container for the application's primary features.
 * @returns {JSX.Element} The rendered application layout.
 */
function App() {
  return (
    <div className="App">
      <Trading />
      <Strategies />
      <Chatbot />
    </div>
  );
}

export default App;
