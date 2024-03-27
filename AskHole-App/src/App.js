import React from 'react';
import './App.css';
import Navbar from './components/Navbar';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from './components/pages/Home';
import Threadpage from './components/pages/Threadpage';
import SignUpPage from './components/pages/SignUpPage';
import ClassPage from './components/pages/ClassesPage';
import SupportPage from './components/pages/SupportPage';


function App() {
  return(

    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route>
            <Route path='/' element={<Home />}/>
            <Route path='/classes' element={<ClassPage />} />
            <Route path="/threads" element={<Threadpage />} />
            <Route path="/SignUpPage" element={<SignUpPage />} />
            <Route path="/Support" element={<SupportPage />} />

          </Route>
        </Routes>
      </BrowserRouter>
  );
}


export default App;
