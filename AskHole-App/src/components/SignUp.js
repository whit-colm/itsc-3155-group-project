import React from 'react';
import 'firebase/compat/auth';
import 'firebase/compat/firestore';
import '../App.css';
import './SignUp.css';
import { Auth } from './Auth';



function SignUp() 
{

    return (
      <div className='SignUp-container'>
        <video src='/video/SignUpVideo.mp4' autoPlay loop muted />
        <h1>Welcome To Your Profile</h1>

      </div>
    );
  }

  

export default SignUp;
