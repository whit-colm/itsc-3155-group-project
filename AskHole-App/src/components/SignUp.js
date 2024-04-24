import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { AuthContext } from './AuthContext';

function SignUpPage() {
  const [isSignedIn, setIsSignedIn] = useState(false);
  const navigate = useNavigate();

  const handleSignUp = () => {
    setIsSignedIn(true);
    navigate('/');
  };

  return (
    <div className='SignUp-container'>
      <video src='/video/SignUpVideo.mp4' autoPlay loop muted />
      <h1>Welcome To Your Profile</h1>
      <button onClick={handleSignUp}>Sign Up</button>
    </div>
  );
}

export default SignUpPage;
