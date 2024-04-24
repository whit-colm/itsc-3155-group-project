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
import AuthContext from './components/AuthContext';
import { AuthProvider } from './components/AuthContext';

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Navbar />
        <Routes>
          <Route path="/" element={<HomePageRouter />} />
          <Route path="/home" element={<HomeL />} />
          <Route path='/classes' element={<ClassPage />} />
          <Route path="/Support" element={<SupportPage />} />
          <Route path="/Info" element={<InfoPage />} />
          <Route path="/posts/:postId" element={<PostDetails />} />
          {/* If no match, redirect to HomeL */}
          <Route path="*" element={<Navigate to="/home" />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

function HomePageRouter() {
  const { isSignedIn } = React.useContext(AuthContext);

  // Render Home if not signed in, otherwise redirect to HomeL
  return isSignedIn ? <Navigate to="/home" /> : <Home />;
}

export default App;
