import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';
import './PostDetails.css'; // Import the CSS file for styling

const PostDetails = () => {
  const { postId } = useParams();
  const [post, setPost] = useState(null);
  const [comments, setComments] = useState([]);
  const [commentText, setCommentText] = useState('');
  const [showMenu, setShowMenu] = useState(null); // State to track which comment's menu is open

  useEffect(() => {
    const fetchPost = async () => {
      try {
        const response = await axios.get(`https://jsonplaceholder.typicode.com/posts/${postId}`);
        setPost(response.data);
      } catch (error) {
        console.error(error);
      }
    };

    const fetchComments = async () => {
      try {
        const response = await axios.get(`https://jsonplaceholder.typicode.com/posts/${postId}/comments`);
        setComments(response.data);
      } catch (error) {
        console.error(error);
      }
    };

    fetchPost();
    fetchComments();
  }, [postId]);

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await axios.post(`https://jsonplaceholder.typicode.com/posts/${postId}/comments`, {
        postId,
        body: commentText,
      });
      const newComment = response.data;
      setComments([...comments, newComment]);
      setCommentText('');
    } catch (error) {
      console.error(error);
    }
  };

  // Function to toggle the menu for a comment
  const toggleMenu = (commentId) => {
    setShowMenu(showMenu === commentId ? null : commentId);
  };

  if (!post) {
    return <div>Loading...</div>;
  }

  const handleLike = (postId) => {
    console.log(`Liked post with ID ${postId}`);
  };

  return (
    <div className="post-details-container">
      <h2 className="post-title">{post.title}</h2>
      <p className="post-body">{post.body}</p>

      <h3 className="comments-header">Comments</h3>
      <div className="comments-container">
        {comments.map(comment => (
          <div key={comment.id} className="comment-box">
            {/* Icons */}
            <div className="comment-icons">
              {/* Icon 1 */}
              <div className="icon">Icon 1</div>
              {/* Icon 2 */}
              <div className="icon">Icon 2</div>
              {/* Icon 3 */}
              <div className="icon">Icon 3</div>
            </div>
            {/* End of Icons */}

            {/* Kabob menu */}
            <div className="kabob-menu" onClick={() => toggleMenu(comment.id)}>
              <div className="kabob-icon"></div>
              {showMenu === comment.id && (
                <div className="kabob-content">
                  <p>Username: {comment.userName}</p>
                  <button onClick={() => console.log("Block")}>Block</button>
                  <button onClick={() => console.log("Report")}>Report</button>
                </div>
              )}
            </div>
            {/* End of Kabob menu */}

            <strong className="comment-name">{comment.name}</strong>: 
            <p className="comment-body">{comment.body}</p>
            <button onClick={() => handleLike(post.id)}>Like</button>
          </div>
        ))}
      </div>

      <form onSubmit={handleSubmit} className="comment-form">
        <textarea
          value={commentText}
          onChange={(e) => setCommentText(e.target.value)}
          placeholder="Leave a comment..."
          required
          className="comment-input"
        ></textarea>
        <button type="submit" className="comment-submit-btn">Submit</button>
      </form>
    </div>
  );
};

export default PostDetails;
