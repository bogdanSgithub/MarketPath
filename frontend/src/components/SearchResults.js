import React, { useContext } from "react";
import StockContext from "../context/StockContext";

const SearchResults = ({ results, setResults }) => {
  const { setStockSymbol } = useContext(StockContext);
  return (
    <ul className="absolute top-12 border-2 w-full rounded-md h-64 overflow-y-scroll bg-white border-neutral-200 custom-scrollbar">
      {results.map((item) => {
        return (
          <li
            className="cursor-pointer p-4 m-2 flex items-center justify-between rounded-md hover:bg-indigo-200 transition duration-300"
            onClick={() => {
              setStockSymbol(item);
              setResults([]);
            }}
          >
            <span>{item}</span>
          </li>
        );
      })}
    </ul>
  );
};

export default SearchResults;
