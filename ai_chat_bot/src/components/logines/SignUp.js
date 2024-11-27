import React, { useState } from 'react';
import './SignUp.css'; // Assuming you're using the CSS file mentioned above
import axios from 'axios'; // Import axios
import { useNavigate } from 'react-router-dom'; // Import useNavigate from react-router-dom
import toast, { Toaster } from 'react-hot-toast'; // Import react-hot-toast

const SignUp = () => {
  const [formData, setFormData] = useState({
    name: '',
    password: '',
    confirmPassword: '',
    acceptTerms: false,
  });

  const [errors, setErrors] = useState({
    name: '',
    password: '',
    confirmPassword: '',
    acceptTerms: '',
  });

  const navigate = useNavigate(); // Initialize the useNavigate hook

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const validateForm = () => {
    const newErrors = {};
    if (!formData.name) newErrors.name = 'Name is required';
    if (!formData.password) newErrors.password = 'Password is required';
    if (formData.password !== formData.confirmPassword)
      newErrors.confirmPassword = 'Passwords do not match';
    if (!formData.acceptTerms) newErrors.acceptTerms = 'You must accept the terms';
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (validateForm()) {
      try {
        // Make the API call to register the user
        const response = await axios.post('http://localhost:5000/register', {
          username: formData.name,
          password: formData.password,
        });

        // If registration is successful, navigate to the login page
        if (response.status === 201) {
          toast.success('Registration successful!', {
            position: 'top-right',
            duration: 5000, // Show for 5 seconds
          });
          navigate('/login'); // Navigate to login page after successful registration
        }
      } catch (error) {
        if (error.response) {
          // If the API returns an error (e.g., user already exists)
          toast.error(error.response.data.error || 'Registration failed', {
            position: 'top-right',
            duration: 5000, // Show for 5 seconds
          });
        } else {
          // If there is any other error (e.g., network issues)
          toast.error('An error occurred. Please try again.', {
            position: 'top-right',
            duration: 5000, // Show for 5 seconds
          });
        }
      }
    }
  };

  return (
    <div className="container">
      {/* Left side (Registration Form) */}
      <div className="left-side">
        <div className="wrapper">
          <h2>Registration</h2>
          <form onSubmit={handleSubmit}>
            <div className="input-box">
              <input
                type="text"
                name="name"
                placeholder="Enter your name"
                value={formData.name}
                onChange={handleInputChange}
              />
              {errors.name && <span className="error">{errors.name}</span>}
            </div>
            <div className="input-box">
              <input
                type="password"
                name="password"
                placeholder="Create password"
                value={formData.password}
                onChange={handleInputChange}
              />
              {errors.password && <span className="error">{errors.password}</span>}
            </div>
            <div className="input-box">
              <input
                type="password"
                name="confirmPassword"
                placeholder="Confirm password"
                value={formData.confirmPassword}
                onChange={handleInputChange}
              />
              {errors.confirmPassword && (
                <span className="error">{errors.confirmPassword}</span>
              )}
            </div>
            <div className="policy">
              <input
                type="checkbox"
                name="acceptTerms"
                checked={formData.acceptTerms}
                onChange={handleInputChange}
              />
              <h3>I accept all terms & conditions</h3>
              {errors.acceptTerms && (
                <span className="error">{errors.acceptTerms}</span>
              )}
            </div>
            <div className="input-box button">
              <input type="submit" value="Register Now" />
            </div>
            <div className="text">
              <h3>
                Already have an account? <a href="/login">Login now</a>
              </h3>
            </div>
          </form>
        </div>
      </div>

      {/* Right side (Welcome Text) */}
      <div className="right-side">
        <h1>Welcome to our website</h1>
        <p>Join us today and start your journey. We are happy to have you!</p>
      </div>

      {/* Toaster component to show the toast notifications */}
      <Toaster />
    </div>
  );
};

export default SignUp;
