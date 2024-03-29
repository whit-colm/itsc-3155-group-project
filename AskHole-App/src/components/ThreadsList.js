import React from 'react';
import { Link } from 'react-router-dom';

const ThreadsList = ({ threads }) => {
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

export default ThreadsList;