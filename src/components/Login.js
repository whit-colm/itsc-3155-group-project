import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  // State variables to hold username and password
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  // Get the navigate function from React Router
  const navigate = useNavigate();

  // Function to handle form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    // Here you can perform validation, authentication, etc.
    console.log('Submitting form...');
    console.log('Username:', username);
    console.log('Password:', password);
    // Reset the form
    setUsername('');
    setPassword('');
    // Redirect to the home page after successful login
    navigate('/');
  };

  return (
    <div>
      <h2>Login</h2>
      
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="username">Username:</label>
          <input
            type="text"
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>
        <div>
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        {/* Button to submit the form */}
        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default Login;
