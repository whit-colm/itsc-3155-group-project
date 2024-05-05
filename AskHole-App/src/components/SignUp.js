import React, { useState } from 'react';
import './SignUp.css';
import axios from 'axios';
import { useNavigate } from 'react-router-dom'; // Import useNavigate from react-router-dom

function SignUp() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [selectedUser, setSelectedUser] = useState(null);
  const [error, setError] = useState('');
  const navigate = useNavigate(); // Initialize useNavigate

  const users = [
    { uid: "josmith8", key: "f4142853e253d686875d9f7a1a1575acaa8a2eb7", permissions: 7 },
    { uid: "emuster2", key: "fad301ea3973af857aa4ea84f6d23828fe830ca2", permissions: 3 },
    { uid: "sorudai0", key: "2840c2e5ac396bf28808891b4e82b071da6d80c9", permissions: 1 },
    { uid: "meiwang1", key: "2312694c6e9c063c1b139124028a6ee831d2632d", permissions: 1 }
  ];

  const handleLogin = async (user) => {
    console.log("Hello, Fruit!")
    console.log(`Token ${user.key}`)
    try {
      const response = await axios.get('http://localhost:8000/objs/profile/', {
        headers: {
          Accept: `application/json`,
          Authorization: `Token ${user.key}`
        }
      });
      console.log(response.data); // Log user information
      setSelectedUser(user); // Set selectedUser to the logged-in user
      setIsLoggedIn(true);
      
      // Check if there is already a token in local storage
      const existingToken = localStorage.getItem('token');
      if (existingToken) {
        // Clear the existing token
        localStorage.removeItem('token');
      }
      
      // Set the new token in local storage
      localStorage.setItem('token', user.key);
    } catch (error) {
      setError('Failed to log in. Please try again.');
      console.error('Login failed:', error);
    }
  };
  

  const handleOpenThreads = () => {
    // Navigate to /home
    navigate('/home');
  };

  if (isLoggedIn) {
    return (
      <div className='Profile-container'>
        <h1>Welcome Back, {selectedUser.uid}!</h1>
        <button onClick={handleOpenThreads}>Open Threads</button>
        {/* Add profile content here */}
      </div>
    );
  } else {
    return (
      <div className='SignUp-container'>
        <div className="form-container">
          <h1>Tester Login</h1>
          {users.map((user, index) => (
            <button key={index} onClick={() => handleLogin(user)}>{user.uid}</button>
          ))}
          {error && <p className="error-message">{error}</p>}
        </div>
      </div>
    );
  }
}

export default SignUp;
