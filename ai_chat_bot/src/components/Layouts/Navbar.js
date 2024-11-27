import React from 'react';
import { Link } from 'react-scroll';
import './Navbar.css';

function Navbar() {
  return (
    <nav className="navbar">
      <div className="logo">Chat-Bot</div>
      <ul className="nav-links">
        <li>
          <Link to="signup" smooth={true} duration={500}>Sign Up</Link>
        </li>
        <li>
          <Link to="signin" smooth={true} duration={500}>Sign In</Link>
        </li>
      </ul>
    </nav>
  );
}

export default Navbar;
