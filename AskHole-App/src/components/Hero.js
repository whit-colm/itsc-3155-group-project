import React from 'react';
import { ReactDOM } from 'react';
import '../App.css';
import './Hero.css';
import Posts from './Posts';

function Hero() {
  return (
    <div className='hero-container'>
        <video src='/video/CollegeSockFootage.mp4' autoPlay loop muted />
      <h1>From Confusion to Clarity</h1>
      <p>Unleash Your Potential with Online Tutoring!</p>

      ReactDOM.render(<Posts />, document.getElementById('root'));

    
    </div>
  );
}

export default Hero;