import React from 'react';
import '../App.css';
import './ClassFinder.css';
import { Button } from './button';


function ClassFinder() {
  return (
    <div className='classfinder-container'>
        <video src='/video/CollegeSockFootage.mp4' autoPlay loop muted />
      <h1>Find Your Class</h1>
      <div className='classfinder-input'>
          <form>
            <input
              className='input-areas'
              name='Class'
              type='Class'
              placeholder='Your Class Name'
            />
            <Button buttonStyle='btn--outline'>Search</Button>
          </form>
        </div>
    
    </div>
  );
}

export default ClassFinder;