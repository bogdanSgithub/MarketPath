import React, { useState } from "react";
import StockContext from "./context/StockContext";
import Search from "./components/Search";
import StockData from "./components/StockData";

const App = () => {
  const [stockSymbol, setStockSymbol] = useState("NVDA");
  return (
    <StockContext.Provider value={{ stockSymbol, setStockSymbol }}>
      <Search />
      <StockData />
    </StockContext.Provider>
  );
};

export default App;
