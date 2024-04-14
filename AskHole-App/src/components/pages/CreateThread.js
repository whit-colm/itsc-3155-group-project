import React, { useState } from 'react';
// Creates hooks for questions, tags and setting replying questions
const CreateThread = () => {
    const [question, setQuestion] = useState('');
    const [tags, setTags] = useState([]);
    const [questions, setQuestions] = useState([]);
};
// cahnges the page to render a new question once posted
const handleQuestionChange = (e) => {
    setQuestion(e.target.value);
};
// adding and setting tags
const handleTagChange = (e) => {
    const tag = e.target.value;
    if (!tag.includes(tag)) {
        setTags([...tags, tag]);
    }
};
// submittion of questions including tags
const handleSubmit = (e) => {
    e.preventDefault();
    const newQuestion = { question, tags };
    setQuestions([...questions, newQuestion]);
    setQuestion('');
    setTags([]);
};

return (
    <div>
      <h2>Create a New Question</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="question">Question:</label>
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

      <h2>Questions</h2>
      <ul>
        {questions.map((q, index) => (
          <li key={index}>
            <div>{q.question}</div>
            <div>
              Tags: {q.tags.map((tag, index) => (
                <span key={index}>{tag}</span>
              ))}
            </div>
          </li>
        ))}
      </ul>
    </div>
  );

export default CreateThread;

