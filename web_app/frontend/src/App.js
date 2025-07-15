import React from "react";
import Strategies from "./components/Strategies";
import Chatbot from "./components/Chatbot";
import Trading from "./components/Trading";
import "./App.css";

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
