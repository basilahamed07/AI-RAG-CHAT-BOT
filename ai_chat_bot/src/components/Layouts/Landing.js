import React from 'react';
import { NavLink } from 'react-router-dom'; // Import NavLink from react-router-dom
import './Landing.css';

function Landing() {
  return (
    <div className="container">
      <div className="left-side">
        <h1>Welcome to Chatbot Creation</h1>
        <p>Create and manage chatbots based on your files using cutting-edge Gen AI technology. Streamline your workflow and improve efficiency with ease!</p>

        <div className="buttons">
          {/* Wrap the buttons with NavLink to handle navigation */}
          <NavLink to="/login" className="btn signin">
            Sign In
          </NavLink>
          <NavLink to="/signup" className="btn signup">
            Sign Up
          </NavLink>
        </div>
      </div>
    </div>
  );
}

export default Landing;
