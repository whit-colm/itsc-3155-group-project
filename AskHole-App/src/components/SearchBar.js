import { useState } from "react";
import { FaSearch } from "react-icons/fa";

import "./SearchBar.css";

export const SearchBar = ({ setResults }) => {
  const [input, setInput] = useState("");
  const fetchData = (value) => {
    const classNames = ['Math', 'English', 'Science', 'History', 'Geography']; // Example array of class names
    const results = classNames.filter(className => {
    return className.toLowerCase().includes(value.toLowerCase());
  });
  setResults(results);
};

  /*const fetchData = (value) => {
    fetch("https://jsonplaceholder.typicode.com/users")
      .then((response) => response.json())
      .then((json) => {
        const results = json.filter((user) => {
          return (
            value &&
            user &&
            user.name &&
            user.name.toLowerCase().includes(value)
          );
        });
        setResults(results);
      });
  };
*/
  const handleChange = (value) => {
    setInput(value);
    fetchData(value);
  };

  return (
    <div className="input-wrapper">
      <FaSearch id="search-icon" />
      <input
        placeholder="Find Your Class..."
        value={input}
        onChange={(e) => handleChange(e.target.value)}
      />
    </div>
  );
};