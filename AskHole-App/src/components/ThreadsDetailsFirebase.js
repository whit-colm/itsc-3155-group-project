import React, { useState, useEffect } from 'react';
import firebase from 'firebase/app';
import 'firebase/firestore';

const ThreadDetail = ({ match }) => {
  const [thread, setThread] = useState(null);

  useEffect(() => {
    // Get thread ID from URL params
    const threadId = match.params.threadId;

    // Fetch thread data from Firestore
    const fetchThread = async () => {
      try {
        const threadRef = firebase.firestore().collection('threads').doc(threadId);
        const doc = await threadRef.get();

        if (doc.exists) {
          setThread(doc.data());
        } else {
          console.log('No such document!');
        }
      } catch (error) {
        console.error('Error fetching thread:', error);
      }
    };

    fetchThread();
  }, [match.params.threadId]);

  // Render thread details
  return (
    <div>
      {thread ? (
        <div>
          <h2>{thread.title}</h2>
          <p>{thread.content}</p>
          <h3>Answers</h3>
          <ul>
            {thread.answers.map((answer, index) => (
              <li key={index}>{answer}</li>
            ))}
          </ul>
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

export default ThreadDetailFirebase;
