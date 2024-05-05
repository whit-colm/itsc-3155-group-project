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
      const threadData = {
        threadID: generateUUID(),
        author: { 
          userID: 'user123',
          username: 'example_user',
        },
        title: btoa(title),
        bodyshort: btoa(body.substring(0, 64)),
        date: Math.floor(Date.now() / 1000),
        tags,
        anonymous,
      };

      const response = await axios.post('https://askhole.api.dotfile.sh/v0alpha0/threads/', threadData);
      console.log('New thread created:', response.data);
      onSubmit(response.data);
      onClose();
      window.location.reload();
    } catch (error) {
      console.error('Error creating new thread:', error);
    }
  };

  const generateUUID = () => {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
      var r = Math.random() * 16 | 0,
          v = c === 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
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
            />
          </div>
          <div>
            <label htmlFor="Body">Question:</label>
            <input
              type="text"
              id="body"
              value={body}
              onChange={handleBodyChange}
            />
          </div>
          <div>
            <label htmlFor="tags">Tags:</label>
            <input
              type="text"
              id="tags"
              value={tags.join(',')}
              onChange={handleTagChange}
            />
          </div>
          <div>
            <label htmlFor="anonymous">Post Anonymously:</label>
            <select id="anonymous" value={anonymous.toString()} onChange={handleAnonymousChange}>
              <option value="true">True</option>
              <option value="false">False</option>
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
