import React, { useState } from 'react';
import './Login.css';
import axios from 'axios'; // Import axios
import { NavLink } from 'react-router-dom'; 
import toast, { Toaster } from 'react-hot-toast'; // Import react-hot-toast

const Login = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });

  const [errors, setErrors] = useState({
    email: '',
    password: '',
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const validateForm = () => {
    const newErrors = {};
    if (!formData.email) newErrors.email = 'Email is required';
    if (!formData.password) newErrors.password = 'Password is required';
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (validateForm()) {
      try {
        // Use axios to send the POST request
        const response = await axios.post('http://localhost:5000/login', {
          username: formData.email,
          password: formData.password,
        });

        // If the response is successful, store the access token and user data
        if (response.status === 200) {
          sessionStorage.setItem('access_token', response.data.access_token);
          sessionStorage.setItem('username', response.data.user.username);
          sessionStorage.setItem('userId', response.data.user.userId);

          toast.success('Login successful!', {
            position: 'top-right', // Toast position
            duration: 5000, // Toast duration in ms
          });
        }
      } catch (error) {
        if (error.response) {
          toast.error(error.response.data.error || 'Login failed', {
            position: 'top-right', // Toast position
            duration: 5000, // Toast duration in ms
          });
        } else {
          toast.error('An error occurred. Please try again.', {
            position: 'top-right', // Toast position
            duration: 5000, // Toast duration in ms
          });
        }
      }
    }
  };

  return (
    <div className="container">
      <div className="left-side">
        <h1>Welcome Back!</h1>
        <p>Login to your account and continue where you left off.</p>
      </div>

      <div className="right-side">
        <div className="wrapper">
          <h2>Login</h2>
          <form onSubmit={handleSubmit}>
            <div className="input-box">
              <input
                type="text"
                name="email"
                placeholder="Enter your email"
                value={formData.email}
                onChange={handleInputChange}
              />
              {errors.email && <span className="error">{errors.email}</span>}
            </div>
            <div className="input-box">
              <input
                type="password"
                name="password"
                placeholder="Enter your password"
                value={formData.password}
                onChange={handleInputChange}
              />
              {errors.password && <span className="error">{errors.password}</span>}
            </div>
            <div className="input-box button">
              <input type="submit" value="Login" />
            </div>
            <div className="text">
              <h3>
                <NavLink to="/signup"> Don't have an account? </NavLink>
              </h3>
            </div>
          </form>
        </div>
      </div>

      {/* Toaster component to show the toast notifications */}
      <Toaster />
    </div>
  );
};

export default Login;
