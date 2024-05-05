// authTokenStorage.js

// Function to store token in localStorage
export const storeToken = (username, token) => {
    localStorage.setItem(username, token);
  };
  
  // Function to retrieve token from localStorage
  export const getToken = (username) => {
    return localStorage.getItem(username);
  };
  