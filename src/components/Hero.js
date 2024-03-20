import React from 'react';
import '../App.css';
import './Hero.css';

function Hero() {
  return (
    <div className='hero-container'>
        <video src='/video/CollegeSockFootage.mp4' autoPlay loop muted />
      <h1>From Confusion to Clarity</h1>
      <p>Unleash Your Potential with Online Tutoring!</p>
    
    </div>
  );
}

export default Hero;