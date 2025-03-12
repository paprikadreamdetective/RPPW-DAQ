// src/components/DevicesList.js
// DeviceList.js
import React from "react";
import './DevicesList.css';
const DeviceList = ({ devices, navigate }) => {
  return (
    <div className="devices-list">
      <h3>Devices</h3>
      {devices.map((device, index) => (
        <div key={index} className="device-item" onClick={() => navigate(`/dashboard/${device.name}`)}>
          {device.name}
        </div>
      ))}
    </div>
  );
};

