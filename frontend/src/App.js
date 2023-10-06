import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Plot from 'react-plotly.js';

function App() {
  const [selectedPage, setSelectedPage] = useState('Dashboard');
  const [apiData, setApiData] = useState('');
  const [plotData, setPlotData] = useState({});
  const [selectedData, setSelectedData] = useState('');
  const [plotTitle, setPlotTitle] = useState('');

  useEffect(() => {
    const apiEndpoint = 'http://localhost:5000/analysis';

    const fetchDataFromApi = async () => {
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

    fetchDataFromApi();
  }, []);

  useEffect(() => {
    if (apiData) {
      // Assuming that apiData is an object containing four arrays, e.g., { data_list0: [], data_list1: [], data_list2: [], data_list3: [] }
      setPlotData(apiData);
    }
  }, [apiData]);

  const renderDashboard = () => {
    // Check if plotData is not empty
    if (Object.keys(plotData).length === 0) {
      return <div>Loading...</div>;
    }

    return (
      <div>
        <h1>Real-time Dashboard</h1>
        {Object.keys(plotData).map((dataKey, index) => (
          <div key={index}>
            <Plot
              data={[
                {
                  x: Array.from({ length: plotData[dataKey].length }, (_, i) => i),
                  y: plotData[dataKey],
                  type: 'line',
                  name: dataKey,
                },
              ]}
              layout={{ title: dataKey }}
            />
            <h2>Data Summary</h2>
            <p>Selected Data: {selectedData}</p>
            <p>
              Mean of {selectedData}:{' '}
              {plotData[dataKey].reduce((a, b) => a + b, 0) / plotData[dataKey].length}
            </p>
          </div>
        ))}
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
