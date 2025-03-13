// src/components/DeviceDetails.js
import { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import './DevicesDetails.css';
import DAQSlider from "./DAQSlider";
// DeviceDetails.js
import React from "react";
/*
function DeviceDetails ({ selectedDevice, setShowPanel }) {
  return (
    <div className="device-details">
      {selectedDevice && (
        <>
          <h2>{selectedDevice.name}</h2>
          <div className="device-info">
            <p><strong>Hardware:</strong> {selectedDevice.hardware}</p>
            <p><strong>IP:</strong> {selectedDevice.ip}</p>
            <p><strong>Location:</strong> {selectedDevice.location}</p>
            <p><strong>I2C Address:</strong> {selectedDevice.i2c}</p>
            <p><strong>PWM Outputs:</strong> {selectedDevice.pwmOutputs}</p>
            <p><strong>Analog Inputs:</strong> {selectedDevice.analogInputs}</p>
            <p><strong>Description:</strong></p>
            <div className="device-description">{selectedDevice.description}</div>
          </div>
          <button className="use-daq-button" onClick={() => setShowPanel(true)}>Use DAQ</button>
        </>
      )}
    </div>
  );
};*/

function DeviceDetails({ selectedDevice }) {
  const [onUseDaq, setOnUseDaq] = useState(false);
  return (
    <div className="device-details">
      {( selectedDevice && !onUseDaq &&
      <>
        <h2>{selectedDevice.name}</h2>
        <div className="device-info">
          <p><strong>Hardware:</strong> {selectedDevice.hardware}</p>
          <p><strong>IP:</strong> {selectedDevice.ip}</p>
          <p><strong>Location:</strong> {selectedDevice.location}</p>
          <p><strong>I2C Address:</strong> {selectedDevice.i2c}</p>
          <p><strong>PWM Outputs:</strong> {selectedDevice.pwmOutputs}</p>
          <p><strong>Analog Inputs:</strong> {selectedDevice.analogInputs}</p>
          <p><strong>Description:</strong></p>
          <div className="device-description">{selectedDevice.description}</div>
        </div>
        {/*<button className="use-daq-button" onClick={onUseDaq}>Use DAQ</button>*/}
        <button className="use-daq-button" onClick={() => setOnUseDaq(true)}>Use DAQ</button >
      </>)}
      {onUseDaq && <DAQSlider />}
    </div>
  );
}

export default DeviceDetails;