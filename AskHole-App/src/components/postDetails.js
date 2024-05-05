import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

const PostDetails = () => {
  const { postId } = useParams();
  const [post, setPost] = useState(null);

  useEffect(() => {
    const fetchPost = async () => {
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
        
        if (response.status === 200) {
          setPost(response.data);
        } else {
          console.error('Failed to fetch post:', response.statusText);
        }
      } catch (error) {
        console.error('Error fetching post:', error.message);
      }
    };

    fetchPost();
  }, [postId]);

  if (!post) {
    return <div>Loading...</div>;
  }

  return (
    <div className="post-details">
      <h1>{post.title}</h1>
      <div className="question">
        <h2>Question:</h2>
        <p>{post.question.content}</p>
      </div>
      <div className="responses">
        <h2>Responses:</h2>
        <ul>
          {post.responses.map((response, index) => (
            <li key={index}>{response.message}</li>
          ))}
        </ul>
      </div>
      <div className="comment-form">
        <textarea rows="4" cols="50" placeholder="Write your response..."></textarea>
        <button>Submit</button>
      </div>
    </div>
  );
};

export default PostDetails;
