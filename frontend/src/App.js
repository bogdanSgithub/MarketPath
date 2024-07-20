import React, { useEffect, useState } from "react";
import Plot from "react-plotly.js";

const App = () => {
  const [data, setData] = useState([]);
  const [ticker, setTicker] = useState("NVDA");

  useEffect(() => {
    fetch(`/historical_data?stock=${ticker}`)
      .then((response) => response.json())
      .then((data) => setData(data));
  }, []);

  const plotData = data.length
    ? [
        {
          x: data.map((item) => item.Date),
          y: data.map((item) => item.Close),
          type: "scatter",
          mode: "lines+markers",
          marker: { color: "black" },
        },
      ]
    : [];

  return (
    <div>
      <h1>Stock Price Data</h1>
      <Plot data={plotData} layout={{ title: `Stock Price Of ${ticker}` }} />
    </div>
  );
};

export default App;
