// src/components/DevicesList.js
import React from "react";
import { useNavigate } from "react-router-dom";
import './DevicesList.css';
const devices = [
  { id: 1, name: "Device1", hardware: "Raspberry PI 4", ip: "192.168.100.164", location: "Biprocess Lab", i2c: 0, pwmOutputs: 8, analogInputs: 8, description: "Device description here..." },
  { id: 2, name: "Device2", hardware: "Arduino Uno", ip: "192.168.100.165", location: "Main Lab", i2c: 1, pwmOutputs: 4, analogInputs: 6, description: "Another device description here..." },
];

function DevicesList() {
  const navigate = useNavigate();

  const handleDeviceClick = (deviceId) => {
    navigate(`/device/${deviceId}`);
  };

  return (
    <div className="devices-list">
      <h3>Devices</h3>
      {devices.map((device) => (
        <div key={device.id} className="device-item" onClick={() => handleDeviceClick(device.id)}>
          {device.name}
        </div>
      ))}
    </div>
  );
}

export default DevicesList;
