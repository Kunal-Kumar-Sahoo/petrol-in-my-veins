import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function Prediction() {
  const [tableData, setTableData] = useState([]);

  const handleEmailClick = async (rowData) => {
    try {
      const response = await axios.post('/send_email', rowData);
      if (response.data) {
        alert('Email sent successfully!');
      }
    } catch (error) {
      console.error('Error sending email:', error);
    }
  };

  const exportToCSV = () => {
    if (tableData.length === 0) {
      alert('No data to export.');
      return;
    }
  
    const headerRow = ['Pump', 'Fault', 'Prediction Value'];
    const csvData = [headerRow].concat(
      tableData.map((rowData) => {
        return Object.values(rowData).map((value) => `"${value}"`).join(',');
      })
    );
  
    const csvBlob = new Blob([csvData.join('\n')], { type: 'text/csv' });
    const csvUrl = URL.createObjectURL(csvBlob);
    const link = document.createElement('a');
    link.href = csvUrl;
    link.setAttribute('download', 'tableData.csv');
    document.body.appendChild(link);
    link.click();
    URL.revokeObjectURL(csvUrl);
    document.body.removeChild(link);
  };
  

  return (
    <div className='table-header'>
      <h1>Predictions for faults</h1>
      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>Pump</th>
              <th>Fault</th>
              <th>Prediction Value</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {tableData.map((rowData, index) => (
              <tr key={index}>
                <td>{rowData.col1}</td>
                <td>{rowData.col2}</td>
                <td>{rowData.col3}</td>
                <td>
                  <button onClick={() => handleEmailClick(rowData)}>Send Email</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        <div className='button-container'>
        <button className="export-button" onClick={exportToCSV}>
          Export to CSV
        </button>
        </div>
      </div>
    </div>
  );
}

export default Prediction;
