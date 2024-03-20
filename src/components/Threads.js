import React, { useState, useEffect } from 'react';
import { collection, addDoc, updateDoc, doc, getDocs, serverTimestamp, query, orderBy } from 'firebase/firestore';
import { firestore } from './FB-config';
import './Threads.css'; // Import CSS file for styling

function Threads() {
  const [message, setMessage] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const formatTimestamp = (timestamp) => {
    if (!timestamp || !(timestamp instanceof Date)) {
      return ''; // Return empty string if timestamp is null or not a Date object
    }
    return timestamp.toLocaleString(); // Format the date and time
  }
  
  

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const querySnapshot = await getDocs(
        query(collection(firestore, 'message'), orderBy('timestamp', 'asc'))
      );
      const messages = [];
      querySnapshot.forEach(doc => {
        const data = doc.data();
        messages.push({ id: doc.id, ...data });
      });
      setMessage(messages);
    } catch (error) {
      console.error('Error fetching data', error);
    }
  }
  
 

  const handleMessageSubmitted = async (e) => {
    e.preventDefault();
    if (inputMessage.trim() !== '') {
      try {
        const timestamp = serverTimestamp();
        await addDoc(collection(firestore, 'message'), {
          text: inputMessage,
          isQuestion: true,
          timestamp: timestamp
        });
        setInputMessage('');
        // Fetch data again after adding message to Firestore
        fetchData();
      } catch (error) {
        console.error('Error adding message to Firestore:', error);
        // Handle error (e.g., display error message to the user)
      }
    }
  }

  const handleReply = async (index) => {
    const reply = window.prompt("Enter Answer");

    if (reply) {
      try {
        const messageRef = doc(firestore, 'message', message[index].id);
        await updateDoc(messageRef, { reply: reply });
        // Fetch data again after updating reply in Firestore
        fetchData();
      } catch (error) {
        console.error('Error updating message reply in Firestore:', error);
        // Handle error (e.g., display error message to the user)
      }
    }
  }

  return (
    <div className="threads-container">
      {message.map((message, index) => (
      <div key={index} className="message-container">
      <div>{message.username}: {message.text}</div>
        <div className="timestamp">{formatTimestamp(message.timestamp)}</div>
        {message.isQuestion && (<button onClick={() => handleReply(index)} className="button">Reply</button>)}
        {message.reply && <div>Reply: {message.reply}</div>}
      </div>
  ))}
      <form onSubmit={handleMessageSubmitted} className="input-container">
        <input type="text"
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          placeholder="Type your question" />
        <button type="submit" className="button">Send</button>
      </form>
    </div>
  );
  
}

export default Threads;
