import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import './Posts.css';
import CreateThreadsModal from './CreateThreadsModal';

const Posts = () => {
  const [posts, setPosts] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [showMenu, setShowMenu] = useState(null);
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [isFilterModalOpen, setIsFilterModalOpen] = useState(false);
  const [tagFilter, setTagFilter] = useState('');

  useEffect(() => {
    const fetchPosts = async () => {
      try {
        const response = await axios.get('https://askhole.api.dotfile.sh/v0alpha0/threads/');
        setPosts(response.data);
      } catch (error) {
        console.error(error);
      }
    };

    fetchPosts();
  }, []);

  const handleSearch = (event) => {
    setSearchTerm(event.target.value);
  };

  const toggleMenu = (postId) => {
    setShowMenu(showMenu === postId ? null : postId);
  };

  const handleSubmit = (formData) => {
    // Prepend new post to posts array
    setPosts([formData, ...posts]);
    setIsCreateModalOpen(false);
  };

  const handleTagFilter = (event) => {
    setTagFilter(event.target.value);
  };

  const applyTagFilter = () => {
    setSearchTerm('');
    setIsFilterModalOpen(false);
  };

  const filteredPosts = posts.filter(post =>
    post.title.toLowerCase().includes(searchTerm.toLowerCase()) &&
    (tagFilter === '' || post.tags.includes(tagFilter.toLowerCase()))
  );

  return (
    <div className="post-list">
      <div className="search-bar-container">
        <input
          type="text"
          placeholder="Search by title"
          value={searchTerm}
          onChange={handleSearch}
          className='searchBar'
        />
        <button onClick={() => setIsCreateModalOpen(true)} className="createThreadButton">Create Thread</button>
        <button onClick={() => setIsFilterModalOpen(true)} className="filterButton">Filter by Tag</button>
      </div>
      <CreateThreadsModal isOpen={isCreateModalOpen} onClose={() => setIsCreateModalOpen(false)} onSubmit={handleSubmit} />
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
          <Link to={`/posts/${post.id}`}>Read More</Link>
        </div>
      ))}
      {isFilterModalOpen && (
        <div className="modal">
          <div className="modal-content">
            <h2>Filter by Tag</h2>
            <input
              type="text"
              placeholder="Enter tag"
              value={tagFilter}
              onChange={handleTagFilter}
            />
            <button onClick={applyTagFilter}>Apply</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Posts;
