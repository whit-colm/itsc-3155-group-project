// Inside the Posts.js file

import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import './Posts.css';

const Posts = () => {
  const [posts, setPosts] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [showMenu, setShowMenu] = useState(null); // State to track which comment's menu is open


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
    console.log(`Liked post with ID ${postId}`);
  };

  const handleSearch = (event) => {
    setSearchTerm(event.target.value);
  };

  const filteredPosts = posts.filter(post =>
    post.title.toLowerCase().includes(searchTerm.toLowerCase())
  );
  const toggleMenu = (postId) => {
    setShowMenu(showMenu === postId ? null : postId);
  };

  return (
    <div className="post-list">
      <input
        type="text"
        placeholder="Search by title"
        value={searchTerm}
        onChange={handleSearch}
        className='searchBar'
      />
      {filteredPosts.map((post) => (
        <div key={post.id} className="post-item">
          <div className="kabob-menu" onClick={() => toggleMenu(post.id)}>
              <div className="kabob-icon"></div>
              {showMenu === post.id && (
                <div className="kabob-content">
                  <p>Username: {post.userName}</p>
                  <button onClick={() => console.log("Block")}>Block</button>
                  <button onClick={() => console.log("Report")}>Report</button>
                </div>
              )}
            </div>
          <h2 className="post-title">{post.title}</h2>
          <p className="post-body">{post.body}</p>
          <button onClick={() => handleLike(post.id)}>Like</button>
          <Link to={`/posts/${post.id}`}>Read More</Link>
        </div>
      ))}
    </div>
  );
};

export default Posts;
