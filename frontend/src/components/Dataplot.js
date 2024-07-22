import React, { useState, useEffect, useContext } from "react";
import Plot from "react-plotly.js";
import StockContext from "../context/StockContext";

const Dataplot = () => {
  const { stockSymbol } = useContext(StockContext);
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch(`/historical_data/${stockSymbol}`)
      .then((response) => response.json())
      .then((data) => setData(data));
  }, [stockSymbol]);

  const plotData = data.length
    ? [
        {
          x: data.map((item) => item.Date),
          open: data.map((item) => item.Open),
          high: data.map((item) => item.High),
          low: data.map((item) => item.Low),
          close: data.map((item) => item.Close),
          type: "ohlc",
          xaxis: "x",
          yaxis: "y",
        },
      ]
    : [];

  return (
    <div>
      <h1>{stockSymbol} Data</h1>
      <Plot
        data={plotData}
        layout={{
          title: "OHLC Chart",
          xaxis: {
            title: "Date",
            rangeslider: { visible: false },
          },
          yaxis: { title: "Price" },
        }}
      />
    </div>
  );
};

export default Dataplot;
