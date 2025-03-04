// src/components/Dashboard.js
/*import React, { useState } from "react";
import Slider from "react-slick";
import PwmControl from "./PwmControl";
import DaqInfo from "./DAQInfo";
import Graph from "./Graph";
import BioMotor from "./BioMotor";
import VerticalSwipeToSlide from "./VerticalPanel";

const graphUrl = "http://192.168.100.174/zabbix/index.php?...";

function Dashboard() {
  const [changeMode, setChangeMode] = useState(0);

  const settings = {
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: 1,
    slidesToScroll: 1,
    swipe: false,
    draggable: false,
  };

  return (
    <div className="slider-container">
      <Slider {...settings}>
        <div className="dashboard-panel"><DaqInfo /></div>
        <div className="dashboard-panel"><Graph graphUrl={graphUrl} /></div>
        <div className="dashboard-panel"><PwmControl changeMode={changeMode} setChangeMode={setChangeMode} /></div>
        <div className="dashboard-panel"><BioMotor /></div>
        <div className="dashboard-panel"><VerticalSwipeToSlide /></div>
      </Slider>
    </div>
  );
}

export default Dashboard;
*/


/*
import React, { useState } from 'react';
import Slider from 'react-slick';
import PwmControl from './PwmControl';
import DaqInfo from './DAQInfo';
import Graph from './Graph';
import BioMotor from './BioMotor';
import VerticalSwipeToSlide from './VerticalPanel';
import '../App.css';

function Dashboard() {
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
    centerMode: true, // Habilita el modo centrado
  centerPadding: "0px", // Espaciado entre slides
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: 1,
    slidesToScroll: 1,
  speed: 500,
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
            <>
          {/*<div className="dashboard-container">
            <DaqInfo />
            <Graph graphUrl={graphUrl} />
            <PwmControl changeMode={changeMode} setChangeMode={setChangeMode}/>
          </div>*//*}

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
          </>
        )}
      </div>
    </div>
  );
}

export default Dashboard;*/
import { useParams, useNavigate } from "react-router-dom";
import { useContext } from "react";
import { AuthContext } from "./AuthContext";
//import Login from "./Login"; // Importamos la pantalla de Login
import AuthUserForm from "./AuthForm";
import React, { useState } from "react";
import Slider from "react-slick";
import PwmControl from "./PwmControl";
import DaqInfo from "./DAQInfo";
import Graph from "./Graph";
import BioMotor from "./BioMotor";
import VerticalSwipeToSlide from "./VerticalPanel";
import "../App.css";  
import "./SidebarHome.css";

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faHome, faSignOutAlt, faBars } from "@fortawesome/free-solid-svg-icons";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";

function Dashboard() {
  const { user, logout } = useContext(AuthContext); // Obtener usuario del contexto
  //const [selectedDevice, setSelectedDevice] = useState(null);
  const [showPanel, setShowPanel] = useState(false);
  const [changeMode, setChangeMode] = useState(0);

  const { deviceName } = useParams(); // Obtiene el dispositivo desde la URL
  const navigate = useNavigate();

  const [sidebarOpen, setSidebarOpen] = useState(false);
  const toggleSidebar = () => setSidebarOpen(!sidebarOpen);
  if (!user) return <AuthUserForm />; // Si no está autenticado, mostrar la pantalla de Login

  const devices = [
    { name: "Device1", hardware: "Raspberry PI 4", ip: "192.168.100.164", location: "Biprocess Lab", i2c: 0, pwmOutputs: 8, analogInputs: 8, description: "Device description here..." },
    { name: "Device2", hardware: "Arduino Uno", ip: "192.168.100.165", location: "Main Lab", i2c: 1, pwmOutputs: 4, analogInputs: 6, description: "Another device description here..." },
  ];

  const selectedDevice = devices.find((d) => d.name === deviceName);

  return (
    <div className={`app-container ${sidebarOpen ? "sidebar-open" : ""}`}>
    {/*<div className="app-container">*/}
      
      {/* Sidebar */}
      <div className={`sidebar ${sidebarOpen ? "open" : ""}`}>
        {/* Botón para abrir/cerrar el Sidebar */}
        <button className="menu-button" onClick={toggleSidebar}>
          <FontAwesomeIcon icon={faBars} />
        </button>

        <br/>
        <br/>
        <hr/>
        
        <div className="sidebar-options">
        
          <div className="sidebar-item" onClick={() => navigate("/")}>
            <FontAwesomeIcon icon={faHome} size="2x" color="white" />
            
          </div>
          <div className="sidebar-item" onClick={logout}>
            <FontAwesomeIcon icon={faSignOutAlt} size="2x" color="white" />
          </div>
        </div>  
      </div>

      <div className="devices-list">
        <h3>Devices</h3>
        {devices.map((device, index) => (
          <div key={index} className="device-item" onClick={() => navigate(`/dashboard/${device.name}`)}>
          {/*<div key={index} className="device-item" onClick={() => setSelectedDevice(device)}>*/}
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
            <button className="use-daq-button" onClick={() => setShowPanel(true)}>Use DAQ</button>
          </>
        )}

        {showPanel && (
          <div className="slider-container">
            <Slider {...{ dots: true, infinite: true, speed: 500, slidesToShow: 1, slidesToScroll: 1 }}>
              <div className="dashboard-panel"><DaqInfo /></div>
              <div className="dashboard-panel"><Graph graphUrl="http://192.168.100.174/zabbix/index.php?name=Admin&password=&enter=Sign&action=dashboard.view&kiosk=1&dashboardid=47320" /></div>
              <div className="dashboard-panel"><PwmControl changeMode={changeMode} setChangeMode={setChangeMode} /></div>
              <div className="dashboard-panel"><BioMotor /></div>
              <div className="dashboard-panel"><VerticalSwipeToSlide /></div>
            </Slider>
          </div>
        )}
      </div>
    </div>
  );
}

export default Dashboard;


