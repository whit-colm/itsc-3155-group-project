import React, {useState, useEffect} from 'react';
import { Link } from 'react-router-dom';
import { Button } from './button';
import './Navbar.css';
function Navbar() {
  const [click, setClick] = useState(false);
  const [button, setButton] = useState(false);

  const handleClick = () => setClick(!click);

  const closeMobileMenu = () => setClick(false);

  const showButton = () => {
    if(window.innerWidth <= 960){
        setButton(false);
    }
    else{
        setButton(true);
    }
  }
  window.addEventListener('resize', showButton);

  useEffect(() => {
    showButton();
  });


  return (
  <>
    <nav className='navbar'>
        <div className='navbar-container'>
            <Link to="/" className="navbar-logo" onClick={closeMobileMenu}>
                AskHole <i className='fa-solid fa-graduation-cap'></i>
            </Link>
            <div className='menu-icon' onClick={handleClick}>
                <i className={click ? 'fas fa-times' : 'fas fa-bars'} />
            </div>
            <ul className={click ? 'nav-menu active' : 'nav-menu'}>
                <li className='nav-item'>
                    <Link to='/' className='nav-links' onClick={closeMobileMenu}>
                    Home
                    </Link>
                </li>
                <li className='nav-item'>
                    <Link to='/classes' className='nav-links' onClick={closeMobileMenu}>
                    Classes
                    </Link>
                </li>
                <li className='nav-item'>
                    <Link to='/threads' className='nav-links' onClick={closeMobileMenu}>
                    Threads
                    </Link>
                </li>
                <li className='nav-item'>
                    <Link to='/sign-up' className='nav-links-mobile' onClick={closeMobileMenu}>
                    Sign Up
                    </Link>
                </li>
            </ul>
            {button && <Button buttonStyle='btn--outline'>PROFILE</Button>}
        </div>
    </nav>
  </>
  )
}

export default Navbar
