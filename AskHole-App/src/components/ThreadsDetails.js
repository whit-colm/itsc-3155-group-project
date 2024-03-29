import React, { useState, useEffect } from 'react';

const ThreadDetail = ({ match }) => {
  const [thread, setThread] = useState(null);

  useEffect(() => {
    // Fetch thread data from the backend using the thread ID
    const fetchThread = async () => {
      try {
        const response = await fetch(`/api/threads/${match.params.threadId}`);
        const data = await response.json();
        setThread(data);
      } catch (error) {
        console.error('Error fetching thread:', error);
      }
    };

    fetchThread();
  }, [match.params.threadId]);

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

export default ThreadDetail;
