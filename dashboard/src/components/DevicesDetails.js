// src/components/DeviceDetails.js
import React from "react";
import { useParams, useNavigate } from "react-router-dom";

const devices = [
  // Misma lista de dispositivos que en DevicesList
  { id: 1, name: "Device1", hardware: "Raspberry PI 4", ip: "192.168.100.164", location: "Biprocess Lab", i2c: 0, pwmOutputs: 8, analogInputs: 8, description: "Device description here..." },
  { id: 2, name: "Device2", hardware: "Arduino Uno", ip: "192.168.100.165", location: "Main Lab", i2c: 1, pwmOutputs: 4, analogInputs: 6, description: "Another device description here..." },
];

function DeviceDetails() {
  const { deviceId } = useParams();
  const navigate = useNavigate();
  const device = devices.find((d) => d.id === parseInt(deviceId));

  if (!device) return <div>Device not found.</div>;

  return (
    <div className="device-details">
      <h2>{device.name}</h2>
      <div className="device-info">
        <p><strong>Hardware:</strong> {device.hardware}</p>
        <p><strong>IP:</strong> {device.ip}</p>
        <p><strong>Location:</strong> {device.location}</p>
        <p><strong>I2C Address:</strong> {device.i2c}</p>
        <p><strong>PWM Outputs:</strong> {device.pwmOutputs}</p>
        <p><strong>Analog Inputs:</strong> {device.analogInputs}</p>
        <p><strong>Description:</strong></p>
        <div className="device-description">{device.description}</div>
      </div>
      <button onClick={() => navigate("/dashboard")}>Use DAQ</button>
    </div>
  );
}

export default DeviceDetails;
