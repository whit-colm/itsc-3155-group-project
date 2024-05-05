import React, { useState } from 'react';
import axios from 'axios';
import './CreateThreadsModal.css';

const CreateThreadsModal = ({ isOpen, onClose, onSubmit }) => {
  const [body, setBody] = useState('');
  const [tags, setTags] = useState([]);
  const [title, setTitle] = useState('');
  const [anonymous, setAnonymous] = useState(false);

  const handleBodyChange = (event) => {
    setBody(event.target.value);
  };

  const handleTitleChange = (event) => {
    setTitle(event.target.value);
  };

  const handleTagChange = (event) => {
    setTags(event.target.value.split(','));
  };

  const handleAnonymousChange = (event) => {
    setAnonymous(event.target.value === 'true');
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const token = localStorage.getItem('token'); // Retrieve the token from localStorage
      if (!token) {
        throw new Error('No token found in localStorage');
      }
  
      const threadData = {
        title: btoa(title),
        body: btoa(body),
        anonymous: anonymous,
        tags: tags,
      };
  
      const response = await axios.post('http://localhost:8000/threads/new/', threadData, {
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'Authorization': `Token ${token}`
        }
      });
  
      console.log('New thread created:', response.data);
      onSubmit(response.data);
      onClose();
      window.location.reload();
    } catch (error) {
      console.error('Error creating new thread:', error);
    }
  };
  
  return (
    <div className={`modal ${isOpen ? 'open' : ''}`}>
      <div className="modal-content">
        <h2>Create Thread</h2>
        <form onSubmit={handleSubmit}>
          <div>
            <label htmlFor="Title">Title:</label>
            <input
              type="text"
              id="Title"
              value={title}
              onChange={handleTitleChange}
              required
            />
          </div>
          <div>
            <label htmlFor="Body">Question:</label>
            <input
              type="text"
              id="body"
              value={body}
              onChange={handleBodyChange}
              required
            />
          </div>
          <div>
            <label htmlFor="tags">Tags:</label>
            <select
              id="tags"
              value={tags.join(',')}
              onChange={handleTagChange}
              required
            >
              <option value="">Select Tag</option>
              <option value="Python">Python</option>
              <option value="Java">Java</option>
              <option value="Calc">Calc</option>
              <option value="CCI">CCI</option>
              <option value="API">API</option>
            </select>
          </div>
          <div>
            <label htmlFor="anonymous">Post Anonymously:</label>
            <select
              id="anonymous"
              value={anonymous.toString()}
              onChange={handleAnonymousChange}
              required
            >
              <option value="false">False</option>
              <option value="true">True</option>
            </select>
          </div>
          <button type="submit">Submit</button>
        </form>
        <button onClick={onClose}>Cancel</button>
      </div>
    </div>
  );
};

export default CreateThreadsModal;
