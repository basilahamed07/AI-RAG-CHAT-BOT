// src/components/chat_bot/MainLayout.js
import React from "react";
import { Routes, Route } from "react-router-dom";
import Sidebar from "./Sidebar";
import ChatBot from "./ChatBot";
import Chatbot from "./ChatBot";

const MainLayout = () => {
  return (
    <div style={{ display: "flex" }}>
      {/* Sidebar */}
      <Sidebar />
      
      {/* Main Content Area */}
      <main style={{ marginLeft: 240, padding: "20px" }}>
        <Routes>
          <Route path="chat-history" element={<Chatbot />} />
          {/* You can add more routes for other chatbot-related views here */}
          <Route path="/" element={<h1>Welcome to the Chat Application</h1>} />
        </Routes>
      </main>
    </div>
  );
};

export default MainLayout;
