/*
import React, { useState } from 'react';
import Slider from 'react-slick';
import PwmControl from './components/PwmControl';
import DaqInfo from './components/DAQInfo';
import Graph from './components/Graph';
import BioMotor from './components/BioMotor';
import VerticalSwipeToSlide from './components/VerticalPanel';
import './App.css';

function App() {
  const graphUrl = "http://192.168.100.174/zabbix/index.php?name=Admin&password=&enter=Sign&action=dashboard.view&kiosk=1&dashboardid=47320";
  const [selectedDevice, setSelectedDevice] = useState(null);
  const [showPanel, setShowPanel] = useState(false);
  const [changeMode, setChangeMode] = useState(0);
  const devices = [
    { name: 'Device1', hardware: 'Raspberry PI 4', ip: '192.168.100.164', location: 'Biprocess Lab', i2c: 0, pwmOutputs: 8, analogInputs: 8, description: 'Device description here...' },
    { name: 'Device2', hardware: 'Arduino Uno', ip: '192.168.100.165', location: 'Main Lab', i2c: 1, pwmOutputs: 4, analogInputs: 6, description: 'Another device description here...' },
    // Agrega más dispositivos según sea necesario
  ];

  const handleDeviceClick = (device) => {
    setSelectedDevice(device);
    setShowPanel(false);
  };

  const handleUseDaqClick = () => {
    setShowPanel(true);
  };


  const settings = {
    /*dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: 1,
    slidesToScroll: 1,
    dots: true,
  infinite: true,
  speed: 500,
  slidesToShow: 1,
  slidesToScroll: 1,
  swipe: false, // Deshabilita el deslizamiento con el mouse o touch
  draggable: false, // Deshabilita arrastrar el slider
  //nextArrow: <CustomNextArrow />, // Botón personalizado de siguiente
  //prevArrow: <CustomPrevArrow />, // Botón personalizado de anterior
  };

  function CustomNextArrow(props) {
    const { className, style, onClick } = props;
    return (
      <div
        className={className}
        style={{
          ...style,
          display: "block",
          background: "black",
          width: "50px",
          height: "50px",
          borderRadius: "50%",
          color: "white",
        }}
        onClick={onClick}
      />
    );
  }
  
  function CustomPrevArrow(props) {
    const { className, style, onClick } = props;
    return (
      <div
        className={className}
        style={{
          ...style,
          display: "block",
          background: "black",
          width: "50px",
          height: "50px",
          borderRadius: "50%",
          color: "white",
        }}
        onClick={onClick}
      />
    );
  }
  
  return (
    <div className="app-container">
      <div className="devices-list">
        <h3>Devices</h3>
        {devices.map((device, index) => (
          <div 
            key={index} 
            className="device-item" 
            onClick={() => handleDeviceClick(device)}
          >
            {device.name}
          </div>
        ))}
      </div>

      <div className="device-details">
        {selectedDevice && !showPanel && (
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
            <button className="use-daq-button" onClick={handleUseDaqClick}>Use DAQ</button>
          </>
        )}
        
        {showPanel && (
          /*<div className="dashboard-container">
            <DaqInfo />
            <Graph graphUrl={graphUrl} />
            <PwmControl changeMode={changeMode} setChangeMode={setChangeMode}/>
          </div>
          <div className="slider-container">
            <Slider {...settings}>
              <div className="dashboard-panel">
                <DaqInfo />
              </div>
              <div className="dashboard-panel">
                <Graph graphUrl={graphUrl} />
              </div>
              <div className="dashboard-panel">
                <PwmControl changeMode={changeMode} setChangeMode={setChangeMode} />
              </div >
              <div className="dashboard-panel">
                <BioMotor/>
              </div>
              <div className="dashboard-panel">
                <VerticalSwipeToSlide/>
              </div>
            </Slider>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;*/

// src/App.js
/*import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import DevicesList from "./components/DevicesList";
import DeviceDetails from "./components/DevicesDetails";
import Dashboard from "./components/Dashboard";
//import NotFound from "./components/NotFound";
import "./App.css";*/
/*
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { useContext } from "react";
import { AuthProvider, AuthContext } from "./components/AuthContext";
import Dashboard from "./components/Dashboard";
import Login from "./components/Login";
import "./App.css";

function AppRoutes() {
  const { user } = useContext(AuthContext);

  return (
    <Routes>
      <Route path="/" element={user ? <Dashboard /> : <Navigate to="/login" />} />
      <Route path="/login" element={user ? <Navigate to="/" /> : <Login />} />
    </Routes>
  );
}

function App() {
  return (
    <AuthProvider>
      <Router>
        <AppRoutes />
      </Router>
    </AuthProvider>
  );
}

export default App;*/

import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { useContext } from "react";
import { AuthProvider, AuthContext } from "./components/AuthContext";
import Dashboard from "./components/Dashboard";
import AuthUserForm from "./components/AuthForm";
import HomePage from "./pages/HomePage";
import "./App.css";

function AppRoutes() {
  const { user } = useContext(AuthContext);
  
  return (
    <>
    {/*<Routes>
      <Route path="/" element={user ? <Dashboard /> : <Navigate to="/login" />} />
      <Route path="/login" element={user ? <Navigate to="/" /> : <AuthUserForm />} />
    </Routes>*/}
    <Routes>
      <Route path="/" element={<Navigate to="/login" />} />
      {/*<Route path="/" element={user ? <Navigate to="/dashboard" /> : <Navigate to="/login" />} />*/}
      <Route path="/login" element={user ? <Navigate to="/dashboard" /> : <AuthUserForm />} />
      <Route path="Home" element={<HomePage />} />
      <Route path="/dashboard" element={<Dashboard />} />
      {/*<Route path="/dashboard/:Home" element={<HomePage />} />*/} {/* Ruta para dispositivos */}
      <Route path="/dashboard/:deviceName" element={<Dashboard />} /> {/* Ruta para dispositivos */}
    </Routes>
    </>
  );
}

function App() {
  return (
    <AuthProvider>
      <Router>
        <AppRoutes />
      </Router>
    </AuthProvider>
  );
}

export default App;
