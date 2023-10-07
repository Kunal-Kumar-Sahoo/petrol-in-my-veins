import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Plot from 'react-plotly.js';
import Prediction from './prediction';
import { BrowserRouter as Router, Route, Routes, Link, Outlet } from 'react-router-dom';
import './App.css';

function App() {
  const [apiData, setApiData] = useState('');
  const [plotData, setPlotData] = useState({});
  const [isPredictionPageVisible, setPredictionPageVisible] = useState(false);

  const handlePredictionClick = () => {
    setPredictionPageVisible(true);
  };

  const handleApiCallClick = async () => {
    const apiEndpoint = 'http://backend:5000/analysis';

    try {
      const response = await axios.get(apiEndpoint, { responseType: 'json' });
      if (response.status === 200) {
        setApiData(response.data);
      } else {
        console.error('Error', response.status);
      }
    } catch (error) {
      console.error('An error occurred:', error);
    }
  };

  useEffect(() => {
    handleApiCallClick();
  }, []);

  useEffect(() => {
    if (apiData) {
      setPlotData(apiData);
    }
  }, [apiData]);

  const getRandomColor = () => {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
  };

  const renderDashboard = () => {
    if (Object.keys(plotData).length === 0) {
      return <div>Loading...</div>;
    }
  
    const plotKeys = Object.keys(plotData).slice(0, 4);
  
    return (
      <div className="card-container">
        {plotKeys.map((dataKey, index) => (
          <div key={index} className="card">
            <div className="plot-container">
              <Plot
                data={[
                  {
                    x: plotData['timestamp'],
                    y: plotData[dataKey],
                    type: 'scatter',
                    mode: 'lines+markers',
                    name: dataKey,
                    line: {
                      color: getRandomColor(),
                      width: 2,
                    },
                  },
                ]}
                layout={{
                  title: dataKey,
                  xaxis: { title: 'Timestamp' },
                  yaxis: { title: 'Value' },
                  legend: { traceorder: 'normal' },
                  width: 400,
                  height: 300, // Set the height of each plot
                }}
                className="plotly-plot" // Apply plot styling
              />
            </div>
          </div>
        ))}
      </div>
    );
  };
  
  return (
    <div className='app-container'>
      <h1> Sucker Rod Pump fault detection dashboard</h1>
      <div>
        {renderDashboard()} {/* Render the dashboard component */}
        <div>
          <Outlet /> 
          <div className="button-container">
            <Link to="/prediction">
              <button className="predict-button" onClick={handlePredictionClick}>
                Predict
              </button>
            </Link>
            <button className="refresh-button" onClick={handleApiCallClick}>
              Refresh
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
export default App;
