// Dashboard.js (Mover a pages/)
import { useParams, useNavigate, useLocation } from "react-router-dom";
import { useContext, useState } from "react";
import { AuthContext } from "../components/AuthContext";
import AuthUserForm from "../components/AuthForm";
import MainSidebar from "../components/MainSidebar";
import DeviceList from "../components/DevicesList";
import DeviceDetails from "../components/DevicesDetails";
import AboutPage from "./AboutPage";
//import DAQSlider from "../components/DAQSlider";
import HomePage from "./HomePage";
import ExperimentsPage from "./ExperimentsPage";
import "../components/Dashboard.css";
import "../App.css";

function DashboardPanel({ showDevices }) {
  const location = useLocation(); 
  const navigate = useNavigate();
  const { user, logout } = useContext(AuthContext);
  const { deviceName } = useParams();
  const [showPanel, setShowPanel] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  
  /*const [changeMode, setChangeMode] = useState(0);*/
  /*const [deviceData, setDeviceData] = useState(null);*/ // Estado para almacenar los datos de dispositivos
  if (!user) return <AuthUserForm />;

  const devices = [
    { name: "Device1", hardware: "Raspberry PI 4", ip: "192.168.100.164", location: "Biprocess Lab", i2c: 0, pwmOutputs: 8, analogInputs: 8, description: "Device description here..." },
    { name: "Device2", hardware: "Arduino Uno", ip: "192.168.100.165", location: "Main Lab", i2c: 1, pwmOutputs: 4, analogInputs: 6, description: "Another device description here..." },
  ];
  const selectedDevice = devices.find((d) => d.name === deviceName);
  

  /*return (
    <div className="app-container">
      <MainSidebar logout={logout} navigate={navigate} />
      {location.pathname === "/dashboard/Home" ? <HomePage /> : !showPanel && <DeviceList navigate={navigate} />}
      <DeviceDetails deviceName={deviceName} setShowPanel={setShowPanel} />
      {showPanel && <DAQSlider changeMode={changeMode} setChangeMode={setChangeMode} />}
    </div>
  );*/

  /*return (
    <div className="app-container">
      <MainSidebar logout={logout} navigate={navigate} />
      {location.pathname === "/dashboard/Home" ? (
        <HomePage />
      ) : !showPanel && deviceData ? ( // Verifica que deviceData esté definido
        <DeviceList data={devices} navigate={navigate} /> // Pasa los datos a DeviceList
      ) : null}
      <DeviceDetails deviceName={devices} setShowPanel={setShowPanel} />
      {showPanel && <DAQSlider changeMode={changeMode} setChangeMode={setChangeMode} />}
    </div>
  );*/
  return (
    <div className={`app-container ${sidebarOpen ? "sidebar-open" : ""}`}>
      <MainSidebar sidebarOpen={sidebarOpen} toggleSidebar={() => setSidebarOpen(!sidebarOpen)} navigate={navigate} logout={logout} />
      
      {location.pathname === "/dashboard/Home" && <HomePage />}

      {location.pathname === "/dashboard/Experiments" && <ExperimentsPage />}

      {location.pathname === "/dashboard/About" && <AboutPage />}

      {/* Mostrar DeviceList solo si no hay un deviceName seleccionado */}
      {showDevices && !deviceName && <DeviceList devices={devices} navigate={navigate} /> }

      {/* Mostrar detalles solo si hay un dispositivo seleccionado */}
      {selectedDevice && !showPanel && <DeviceDetails selectedDevice={selectedDevice}  />}

      {/*showPanel && <DAQSlider />*/}
    </div>
  );
}
export default DashboardPanel;
