// CreateThreadsModal.js

import React, { useState } from 'react';
import './CreateThreadsModal.css'; // Import CSS for modal styling

const CreateThreadsModal = ({ isOpen, onClose, onSubmit }) => {
  const [question, setQuestion] = useState('');
  const [tags, setTags] = useState([]);
  const [title, setTitle] = useState('');

  const handleQuestionChange = (event) => {
    setQuestion(event.target.value);
  };
  const handleTitleChange = (event) => {
    setTitle(event.target.value);
  };

  const handleTagChange = (event) => {
    setTags(event.target.value.split(','));
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    onSubmit({ question, title, tags });
    onClose(); // Close the modal after submit
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
              id="question"
              value={question}
              onChange={handleQuestionChange}
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
          <button type="submit">Submit</button>
        </form>
        <button onClick={onClose}>Cancel</button>
      </div>
    </div>
  );
};

export default CreateThreadsModal;
