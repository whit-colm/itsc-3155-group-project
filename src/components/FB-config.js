// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import {getAuth, GoogleAuthProvider} from "firebase/auth"
import { getStorage } from "firebase/storage";
import { getFirestore } from "firebase/firestore";

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyBUiuAfQGDy3A8_aBKWVTbBO0X3ql362QM",


  authDomain: "askhole-threads.firebaseapp.com",
   projectId: "askhole-threads",
   storageBucket: "askhole-threads.appspot.com",
   messagingSenderId: "507513624255",
   appId: "1:507513624255:web:a1eb3383d14c6b4570180a",
   measurementId: "G-YTY834H03L"
}
// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const firestore = getFirestore(app);
export { firestore };
export const auth =getAuth(app);
export const provider = new GoogleAuthProvider();
export const storage = getStorage();
export const db = getFirestore()

export default app;
