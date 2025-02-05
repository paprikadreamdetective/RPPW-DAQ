import React, { useState, useEffect } from 'react';

import './DAQInfo.css';
function DaqInfo() {
  const [DAQInfo, setDAQInfo] = useState(null);
  useEffect(() => {
    fetch('http://192.168.100.164:5001/get_daq_info')  
      .then(response => response.json())
      .then(data => setDAQInfo(data))
      .catch(error => console.error('Error fetching the data:', error));
  }, []);
  return (
    <div className="daq-info">
      <h2>DAQ Description</h2>
      {DAQInfo ? (
        <div className="daq-info-fields-container">
          <p><strong>Location:</strong> {DAQInfo.location}</p>
          <p><strong>Hardware:</strong> {DAQInfo.hardware}</p>
          <p><strong>Address:</strong> {DAQInfo.address}</p>
          <p><strong>Analog Inputs:</strong> {DAQInfo.analog_inputs}</p>
          <p><strong>PWM Outputs:</strong> {DAQInfo.pwm_outputs}</p>
          <p><strong>I2C Address:</strong> {DAQInfo.i2c_address}</p>
        </div>
      ) : (
        <p>Loading hardware information...</p>
      )}
    </div>
  );
}

export default DaqInfo;