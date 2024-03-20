import React from 'react';
import './App.css';
import Navbar from './components/Navbar';
import Login from './components/Login'; 
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Home from './components/pages/Home';
import Threadpage from './components/pages/Threadpage';
import SignUpPage from './components/pages/SignUpPage';
import ClassPage from './components/pages/ClassesPage';

function App() {
  // Simulate authentication status (you can replace this with your actual authentication logic)
  const isAuthenticated = false; // Set it to true if user is authenticated

  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route
          path="/"
          element={isAuthenticated ? <Home /> : <Navigate to="/login" />}
        />
        <Route path="/login" element={<Login />} />
        <Route path="/classes" element={<ClassPage />} />
        <Route path="/threads" element={<Threadpage />} />
        <Route path="/signup" element={<SignUpPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
