import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Plot from 'react-plotly.js';

function App() {
  const [selectedPage, setSelectedPage] = useState('Dashboard');
  const [apiData, setApiData] = useState('');
  const [selectedData, setSelectedData] = useState('');
  const [plotData, setPlotData] = useState([]);
  const [plotTitle, setPlotTitle] = useState('');

  useEffect(() => {
    const apiEndpoint = 'http://localhost:5000/analysis';

    const fetchDataFromApi = async () => {
      try {
        const response = await axios.get(apiEndpoint, { responseType: 'text' });
        if (response.status === 200) {
          console.log(response.data)
          setApiData(response.data);
        } else {
          console.error('Error', response.status);
        }
      } catch (error) {
        console.error('An error occurred:', error);
      }
    };

    fetchDataFromApi();
  }, []);

  useEffect(() => {
    if (apiData) {
      const dataArray = apiData.split('  ').map(Number);
      setPlotData(dataArray);
    }
  }, [apiData]);

  const renderDashboard = () => {
    return (
      <div>
        <h1>Real-time Dashboard</h1>
        <div>
          <Plot
            data={[
              {
                x: Array.from({ length: plotData.length }, (_, i) => i),
                y: plotData,
                type: 'line',
                name: plotTitle,
              },
            ]}
            layout={{ title: plotTitle }}
          />
        </div>
        <h2>Data Summary</h2>
        <p>Selected Data: {selectedData}</p>
        <p>
          Mean of {selectedData}:{' '}
          {plotData.reduce((a, b) => a + b, 0) / plotData.length}
        </p>
      </div>
    );
  };

  return (
    <div>
      <h1>Real-time Plotly Dashboard</h1>
      <div>
        <header>
          <h2>Navigation</h2>
        </header>
        <select
          value={selectedPage}
          onChange={(e) => setSelectedPage(e.target.value)}
        >
          <option value="Dashboard">Dashboard</option>
          <option value="About">About</option>
          <option value="Contact">Contact</option>
        </select>
      </div>

      {selectedPage === 'Dashboard' && <div>{renderDashboard()}</div>}
    </div>
  );
}

export default App;