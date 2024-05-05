import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Link, Navigate } from 'react-router-dom';
import './Posts.css';
import CreateThreadsModal from './CreateThreadsModal';

const Posts = () => {
  const [posts, setPosts] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [showMenu, setShowMenu] = useState(null);
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [isFilterModalOpen, setIsFilterModalOpen] = useState(false);
  const [tagFilter, setTagFilter] = useState('');
  const [redirect, setRedirect] = useState(null);

  useEffect(() => {
    const fetchPosts = async () => {
      try {
        const token = localStorage.getItem('token');
        if (token) {
          const response = await axios.get('http://localhost:8000/threads/', {
            headers: {
              Accept: 'application/json',
              Authorization: `Token ${token}`,
            },
          });
          if (response.status === 200) {
            const decodedPosts = response.data.threads.map(post => ({
              ...post,
              title: atob(post.title),
              bodyshort: atob(post.bodyshort)
            }));
            setPosts(decodedPosts);
          } else {
            console.error('Failed to fetch posts:', response.statusText);
          }
        } else {
          console.log('No token found in localStorage');
        }
      } catch (error) {
        console.error('Error fetching posts:', error.message);
      }
    };

    fetchPosts();
  }, []);

  const handleSearch = (event) => {
    setSearchTerm(event.target.value);
  };

  const toggleMenu = (threadID) => {
    setShowMenu(showMenu === threadID ? null : threadID);
  };

  const handleSubmit = (formData) => {
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

  const handlePostClick = (threadID) => {
    setRedirect(`/posts/${threadID}`);
  };

  if (redirect) {
    return <Navigate to={redirect} />;
  }

  const filteredPosts = posts.filter(
    (post) =>
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
          className="searchBar"
        />
        <button onClick={() => setIsCreateModalOpen(true)} className="createThreadButton">
          Create Thread
        </button>
        <button onClick={() => setIsFilterModalOpen(true)} className="filterButton">
          Filter by Tag
        </button>
      </div>
      <CreateThreadsModal
        isOpen={isCreateModalOpen}
        onClose={() => setIsCreateModalOpen(false)}
        onSubmit={handleSubmit}
      />
      {filteredPosts.map((post, index) => {
        console.log('Thread ID:', post.threadID);
        return (
          <div key={index} className="post-item" onClick={() => handlePostClick(post.threadID)}>
            <p>{post.anonymous ? 'Posted Anonymously' : `Username: ${post.author.uid}`}</p>
            <h2 className="post-title">{post.title}</h2>
            <p className="post-body">{post.bodyshort}</p>
            <div className="kabob-menu" onClick={() => toggleMenu(post.threadID)}>
              <div className="kabob-icon"></div>
              {showMenu === post.threadID && (
                <div className="kabob-content">
                  <button onClick={() => console.log('Block')}>Block</button>
                  <button onClick={() => console.log('Report')}>Report</button>
                </div>
              )}
            </div>
            <Link to={`/posts/${post.threadID}`}>Read More</Link>
          </div>
        );
      })}
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
