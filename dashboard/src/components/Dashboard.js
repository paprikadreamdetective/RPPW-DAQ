import { useParams, useNavigate } from "react-router-dom";
import { useLocation } from "react-router-dom";
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
import HomePage from "../pages/HomePage";

import "../App.css";  
import "./SidebarHome.css";
import "./Dashboard.css";


import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faHome, faMicrochip, faMicroscope, faSignOutAlt, faBars } from "@fortawesome/free-solid-svg-icons";
import { faClose } from "@fortawesome/free-solid-svg-icons"; // Usamos íconos de react-icons
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";


function SampleNextArrow(props) {
  const { className, style, onClick } = props;
  return (
    <div
      className={className}
      style={{ ...style, display: "block", color: "black" }}
      onClick={onClick}
    />
  );
}

function SamplePrevArrow(props) {
  const { className, style, onClick } = props;
  return (
    <div
      className={className}
      style={{ ...style, display: "block", color: "black" }}
      onClick={onClick}
    />
  );
}

function Dashboard() {
  const location = useLocation(); 
  
  
  
  const settings = {
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: 1,
    slidesToScroll: 1,
    swipe: false,
    draggable: false,
    nextArrow: <SampleNextArrow />,
    prevArrow: <SamplePrevArrow />
  };
  
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

      {/* Sidebar */}
      <div className={`sidebar ${sidebarOpen ? "open" : ""}`}>
        {/* Botón para abrir/cerrar el Sidebar */}
        <button className="menu-button" onClick={toggleSidebar}>
          <FontAwesomeIcon icon={sidebarOpen ? faClose : faBars} />
        </button>
        {/*Separadores de espacios*/}
        <br/>
        <br/>
        <hr/>
        {/*Separadores de espacios*/}
        <div className="sidebar-options">
          <div className="sidebar-item" title={!sidebarOpen ? "Home" : ""} onClick={() => navigate("/dashboard/Home")}>
            <FontAwesomeIcon icon={faHome} size="2x" color="white" />
            {sidebarOpen && <span className="sidebar-item-text">Home</span>}
          </div>
          <div className="sidebar-item" title={!sidebarOpen ? "Devices" : ""} onClick={() => navigate("/")}>
            <FontAwesomeIcon icon={faMicrochip} size="2x" color="white" />
            {sidebarOpen && <span className="sidebar-item-text">Devices</span>}
          </div>
          <div className="sidebar-item" title={!sidebarOpen ? "Experiments" : ""} onClick={() => navigate("/dashboard/Experiments")}>
            <FontAwesomeIcon icon={faMicroscope} size="2x" color="white" />
            {sidebarOpen && <span className="sidebar-item-text">Experiments</span>}
          </div>
          <div className="sidebar-item" title={!sidebarOpen ? "Logout" : ""} onClick={logout}>
            <FontAwesomeIcon icon={faSignOutAlt} size="2x" color="white" />
            {sidebarOpen && <span className="sidebar-item-text">Logout</span>}
          </div>
        </div>  
      </div>

      {/*Device list*/}
      {location.pathname === "/dashboard/Home" ? ( <HomePage />) : 
      ( !showPanel && (
      <div className="devices-list">
        <h3>Devices</h3>
        {devices.map((device, index) => (
          <div key={index} className="device-item" onClick={() => navigate(`/dashboard/${device.name}`)}>
            {device.name}
          </div>
        ))}
      </div>))}

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
            <Slider {...settings}>
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