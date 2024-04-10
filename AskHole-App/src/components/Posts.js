import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom'; // Import Link from react-router-dom
import './Posts.css'; // Import the CSS file

const Posts = () => {
  const [posts, setPosts] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    const fetchPosts = async () => {
      try {
        const response = await axios.get('https://jsonplaceholder.typicode.com/posts');
        setPosts(response.data);
      } catch (error) {
        console.error(error);
      }
    };

    fetchPosts();
  }, []);

  const handleLike = (postId) => {
    // Implement like functionality here
    console.log(`Liked post with ID ${postId}`);
  };

  const handleSearch = (event) => {
    setSearchTerm(event.target.value);
  };

  const filteredPosts = posts.filter(post =>
    post.title.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="post-list">
      <input
        type="text"
        placeholder="Search by title"
        value={searchTerm}
        onChange={handleSearch} className='searchBar'
      />
      {filteredPosts.map((post) => (
        <div key={post.id} className="post-item">
          <h2 className="post-title">{post.title}</h2>
          <p className="post-body">{post.body}</p>
          <button onClick={() => handleLike(post.id)}>Like</button> {/* Like button */}
          <Link to={`/posts/${post.id}`}>Read More</Link> {/* Link to specific post */}
        </div>
      ))}
    </div>
  );
};

export default Posts;
