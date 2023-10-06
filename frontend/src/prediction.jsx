import React, { useState } from 'react';
import axios from 'axios';
import './App.css'

function Prediction() {
  const [tableData, setTableData] = useState([]); // Initialize table data as an empty array

  const handleEmailClick = async (rowData) => {
    // Implement the logic to send an email with rowData
    try {
      const response = await axios.post('/send_email', rowData); 
      if (response.data) {
        alert('Email sent successfully!');
      }
    } catch (error) {
      console.error('Error sending email:', error);
    }
  };

  // Sample data for the table, you can replace it with your data
  const ttableData = [
    { col1: 'Data 1', col2: 'Data 2', col3: 'Data 3', col4: 'Data 4' },
    { col1: 'Data 5', col2: 'Data 6', col3: 'Data 7', col4: 'Data 8' },
    // Add more rows as needed
  ];

  return (
    <div className='table-header'>      
        <h1>Prediction Page</h1>
    <div className="table-container"> {/* Apply the class to center the table */}
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
          {ttableData.map((rowData, index) => (
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
    </div>
    </div>

  );
}
export default Prediction;
