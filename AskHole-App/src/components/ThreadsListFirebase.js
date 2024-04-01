import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import firebase from 'firebase/app';
import 'firebase/firestore';

const ThreadsList = () => {
  const [threads, setThreads] = useState([]);

  useEffect(() => {
    // Fetch threads data from Firestore
    const fetchThreads = async () => {
      try {
        const snapshot = await firebase.firestore().collection('threads').get();
        const threadsData = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
        setThreads(threadsData);
      } catch (error) {
        console.error('Error fetching threads:', error);
      }
    };

    fetchThreads();
  }, []);

  return (
    <div>
      <h1>Threads</h1>
      <ul>
        {threads.map(thread => (
          <li key={thread.id}>
            <Link to={`/threads/${thread.id}`}>{thread.title}</Link>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ThreadsListFirebase;
