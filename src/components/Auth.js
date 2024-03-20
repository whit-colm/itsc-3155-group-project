import { useState } from 'react';
import { auth, provider } from "../components/FB-config";
import { signInWithPopup, signOut } from "firebase/auth";
import "../App.css";
import Cookies from "universal-cookie";
import { Button } from './button';

const cookies = new Cookies();

export const Auth = () => {
  const [isAuth, setIsAuth] = useState(!!cookies.get("auth-token"));

  const handleSignInWithGoogle = async () => {
    try {
      const result = await signInWithPopup(auth, provider);
      cookies.set("auth-token", result.user.refreshToken);
      setIsAuth(true);
    } catch (err) {
      console.error(err);
    }
  };

  const handleSignOut = async () => {
    try {
      await signOut(auth);
      cookies.remove("auth-token");
      setIsAuth(false);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="">
      {isAuth ? (
        <Button onClick={handleSignOut} buttonStyle={'btn--primary'}>Sign Out</Button>
      ) : (
        <Button onClick={handleSignInWithGoogle} buttonStyle={'btn--primary'}>Sign In With Google</Button>
      )}
    </div>
  );
};

