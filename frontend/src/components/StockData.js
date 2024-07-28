import React, { useState, useEffect, useContext } from "react";
import Plot from "react-plotly.js";
import StockContext from "../context/StockContext";

const StockData = () => {
  const { stockSymbol } = useContext(StockContext);
  const [financialData, setFinancialData] = useState({});
  const [historicalData, setHistoricalData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`/data/${stockSymbol}`);
        const [financial, historical] = await response.json();
        setFinancialData(financial);
        setHistoricalData(historical);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, [stockSymbol]);

  const renderTable = (data) => {
    if (!Array.isArray(data) || data.length === 0) {
      return <p>No data available</p>;
    }

    data = data[0];
    const headers = Object.keys(data);

    return (
      <table>
        <thead>
          <tr>
            {headers.map((header) => (
              <th key={header}>{header}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          <tr>
            {headers.map((header) => (
              <td key={header}>
                {typeof data[header] === "boolean"
                  ? data[header]
                    ? "Buy"
                    : "Hold"
                  : data[header]}
              </td>
            ))}
          </tr>
        </tbody>
      </table>
    );
  };

  const renderPlot = (historicalData) => {
    const plotData = historicalData.length
      ? [
          {
            x: historicalData.map((item) => item.Date),
            open: historicalData.map((item) => item.Open),
            high: historicalData.map((item) => item.High),
            low: historicalData.map((item) => item.Low),
            close: historicalData.map((item) => item.Close),
            type: "ohlc",
            xaxis: "x",
            yaxis: "y",
          },
        ]
      : [];

    return (
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
    );
  };

  return (
    <div>
      <h1>Stock Data for {stockSymbol}</h1>
      <h2>OHLC Data</h2>
      {renderPlot(historicalData)}
      <h2>Financial Data Table</h2>
      {renderTable(financialData)}
    </div>
  );
};

export default StockData;
