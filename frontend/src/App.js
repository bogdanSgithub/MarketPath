import React, { useState } from "react";
import StockContext from "./context/StockContext";
import Dataplot from "./components/Dataplot";
import Search from "./components/Search";

const App = () => {
  const [stockSymbol, setStockSymbol] = useState("AAPL");
  return (
    <StockContext.Provider value={{ stockSymbol, setStockSymbol }}>
      <Search />
      <Dataplot />
    </StockContext.Provider>
  );
};

export default App;
