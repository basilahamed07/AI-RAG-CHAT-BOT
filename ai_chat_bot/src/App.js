import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { CssBaseline } from '@mui/material';
import Landing from './components/Layouts/Landing';
import About from './components/Layouts/About';
import Services from './components/Layouts/Services';
import Contact from './components/Layouts/Contact';
import SignUp from './components/logines/SignUp';
import Login from './components/logines/Login';
import MainLayout from './components/chat_bot/MainLayout';
import './App.css';
import ChatComponent from "./components/chatcomp"
import BotForm from './components/bot/select_bot';
function App() {
  return (
    <Router>
      <div className="App">
        <CssBaseline />
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/about" element={<About />} />
          <Route path="/services" element={<Services />} />
          <Route path="/contact" element={<Contact />} />
          <Route path="/signup" element={<SignUp />} />
          <Route path="/login" element={<Login />} />
          {/* <Route path="/chat/*" element={<MainLayout />} /> */}
          <Route path="/chatcomp" element={<ChatComponent />} />
          <Route path="/select_bot" element={<BotForm />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
