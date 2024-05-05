import React from 'react';
import './App.css';
import Navbar from './components/Navbar';
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Home from './components/pages/Home';
import HomeL from './components/pages/HomeL';
import ClassPage from './components/pages/ClassesPage';
import SupportPage from './components/pages/SupportPage';
import InfoPage from './components/pages/InfoPage';
import PostDetails from './components/postDetails';
import SignUpPage from './components/pages/SignUpPage';

function App() {
  return (
      <BrowserRouter>
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/home" element={<HomeL />} />
          <Route path='/classes' element={<ClassPage />} />
          <Route path="/Support" element={<SupportPage />} />
          <Route path="/Info" element={<InfoPage />} />
          <Route path='/sign-up' element={<SignUpPage />} />
          <Route path="/posts/:postId" element={<PostDetails />} />
        </Routes>
      </BrowserRouter>
  );
}



export default App;
