import React, { useState, useEffect } from "react";
import { XMarkIcon, MagnifyingGlassIcon } from "@heroicons/react/24/solid";
import SearchResults from "./SearchResults";

const Search = () => {
  const [input, setInput] = useState("");
  const [results, setResults] = useState([]);
  const [tickers, setTickers] = useState([]);

  useEffect(() => {
    // Fetch the list of S&P 500 companies
    fetch("/sp500")
      .then((response) => response.json())
      .then((data) => setTickers(data));
  }, []);

  const handleSearch = (e) => {
    const searchInput = e.target.value;
    setInput(searchInput);

    if (searchInput.length > 0) {
      const filteredResults = tickers.filter((ticker) =>
        ticker.toLowerCase().startsWith(searchInput.toLowerCase())
      );
      setResults(filteredResults);
    } else {
      setResults([]);
    }
  };

  return (
    <div className="flex items-center my-4 border-2 rounded-md relative z-50 w-96 bg-white border-neutral-200">
      <input
        type="text"
        value={input}
        onChange={handleSearch}
        placeholder="Search stock..."
        className="w-full px-4 py-2 focus:outline-none rounded-md"
      />
      {input && results.length > 0 ? (
        <SearchResults results={results} setResults={setResults} />
      ) : null}
    </div>
  );
};

export default Search;
