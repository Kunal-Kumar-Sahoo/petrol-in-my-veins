import React, {useState } from 'react';
import axios from 'axios';
import './App.css';
import emailjs from '@emailjs/browser';


function Prediction(){
  const [data,setData]=useState({0:{fault:"",prob:""},1:{fault:"",prob:""},2:{fault:"",prob:""},3:{fault:"",prob:""},4:{fault:"",prob:""}})

  async function handleClick(){
      const response=await axios.get('http://backend:5000/send_email',{responseType:'json'})
      if(response.status===200){
          setData({0:{fault:response.data[0].fault,prob:response.data[0].prob},1:{fault:response.data[1].fault,prob:response.data[1].prob},2:{fault:response.data[2].fault,prob:response.data[2].prob},3:{fault:response.data[3].fault,prob:response.data[3].prob},4:{fault:response.data[4].fault,prob:response.data[4].prob}})
      }
      else{
        console.log("Error")
      }
  }

  async function handleEmail(){
    emailjs.send("service_6l3g5x3","template_euag8gx",{from_name:data[0].fault,to_name:1,message:data[0].prob},"KECDOyEgarqRiEQjb");
    console.log("Email sent")  
  }

  return(
    <>
    <div className='table-header'>
      <h1>Predictions for faults</h1>
      <div className="table-container"></div>
    <table>
    <thead>
            <tr>
              <th>Pump</th>
              <th>Fault</th>
              <th>Prediction Accuracy</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
      <tr>
        <td>1</td>
        <td>{data[0].fault}</td>
        <td>{data[0].prob}</td>
        <td><button onClick={handleEmail}>Alert</button></td>
      </tr>
      <tr>
        <td>2</td>
        <td>{data[1].fault}</td>
        <td>{data[1].prob}</td>
        <td><button onClick={handleEmail}>Alert</button></td>
      </tr>
      <tr>
        <td>3</td>
        <td>{data[2].fault}</td>
        <td>{data[2].prob}</td>
        <td><button onClick={handleEmail}>Alert</button></td>
      </tr>
      <tr>
        <td>4</td>
        <td>{data[3].fault}</td>
        <td>{data[3].prob}</td>
        <td><button onClick={handleEmail}>Alert</button></td>
      </tr>
      <tr>
        <td>5</td>
        <td>{data[4].fault}</td>
        <td>{data[4].prob}</td>
        <td><button onClick={handleEmail}>Alert</button></td>
      </tr>
      </tbody>
    </table>
    <div >
    <button onClick={handleClick}>Click To predict</button>
    <button onClick={handleClick}>Predict again</button>
    </div>
    </div>
    </>
  )
  }


export default Prediction;
