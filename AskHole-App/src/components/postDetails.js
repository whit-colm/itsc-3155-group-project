import React, { useEffect, useState, useCallback } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';
import './PostDetails.css'; // Import the CSS file

const PostDetails = () => {
  const { postId } = useParams();
  const [post, setPost] = useState(null);
  const [newMessage, setNewMessage] = useState('');

  // Function to decode URL-safe Base64 strings
  const decodeUrlSafeBase64 = (urlSafeBase64) => {
    const base64 = urlSafeBase64
      .replace(/-/g, '+') // Convert '-' to '+'
      .replace(/_/g, '/'); // Convert '_' to '/'
    return decodeURIComponent(escape(atob(base64)));
  };

  // Function to filter responses with question field equals true
  const filterQuestionResponses = (responses) => {
    return responses.filter((response) => response.question === false);
  };

  const fetchPost = useCallback(async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        console.error('No token found in localStorage');
        return;
      }

      const response = await axios.get(`http://localhost:8000/thread/${postId}/`, {
        headers: {
          Accept: 'application/json',
          Authorization: `Token ${token}`,
        },
      });

      console.log('Response Data:', response.data); // Log response data

      if (response.status === 200) {
        const filteredResponses = filterQuestionResponses(response.data.responses);
        setPost({ ...response.data, responses: filteredResponses });
      } else {
        console.error('Failed to fetch post:', response.statusText);
      }
    } catch (error) {
      console.error('Error fetching post:', error.message);
    }
  }, [postId, filterQuestionResponses]);

  useEffect(() => {
    fetchPost();
  }, [fetchPost]);

  const handleSubmit = async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        console.error('No token found in localStorage');
        return;
      }

      const encodedMessage = btoa(newMessage); // Encode the message body in base64

      await axios.post(`http://localhost:8000/thread/${postId}/new/`, { body: encodedMessage }, {
        headers: {
          Accept: 'application/json',
          Authorization: `Token ${token}`,
        },
      });

      // After successful post, refetch the post details to update the responses
      fetchPost();
    } catch (error) {
      console.error('Error posting message:', error.message);
    }
  };

  if (!post) {
    return <div>Loading...</div>;
  }

  return (
    <div className="post-details-container">
      <div className="post-title">
        <h1>{decodeUrlSafeBase64(post.title)}</h1>
      </div>
      <div className="post-body">
        <div className="question">
          <h2>Question:</h2>
          <p>{decodeUrlSafeBase64(post.question.body)}</p>
        </div>

        <div className="responses">
          <h2>Responses:</h2>
          {post.responses.length > 0 ? (
            post.responses.map((response, index) => (
              <div className="comment-box" key={index}>
                <div className="response-header">
                  <p className="author">{response.author.uid}</p>
                  <p className="date">{new Date(response.date * 1000).toLocaleString()}</p>
                </div>
                <p className="comment-body">{decodeUrlSafeBase64(response.body)}</p>
              </div>
            ))
          ) : (
            <p>No answers yet.</p>
          )}
        </div>
        <div className="comment-form">
          <textarea
            rows="4"
            cols="50"
            placeholder="Write your response..."
            value={newMessage}
            onChange={(e) => setNewMessage(e.target.value)}
            className="comment-input"
          ></textarea>
          <button onClick={handleSubmit} className="comment-submit-btn">Submit</button>
        </div>
      </div>
    </div>
  );
};

export default PostDetails;
