// Dashboard.js (Mover a pages/)
import { useParams, useNavigate, useLocation } from "react-router-dom";
import { useContext, useState, useEffect } from "react";
import { AuthContext } from "../components/AuthContext";
import AuthUserForm from "../components/AuthForm";
import MainSidebar from "../components/MainSidebar";
import DeviceList from "../components/DevicesList";
import DeviceDetails from "../components/DevicesDetails";
import DAQSlider from "../components/DAQSlider";
import HomePage from "./HomePage";
import "../components/Dashboard.css";
import "../App.css";

function DashboardPanel() {
  const location = useLocation(); 
  const { user, logout } = useContext(AuthContext);
  const { deviceName } = useParams();
  const navigate = useNavigate();
  const [showPanel, setShowPanel] = useState(false);
  const [changeMode, setChangeMode] = useState(0);
  const [deviceData, setDeviceData] = useState(null); // Estado para almacenar los datos de dispositivos
  
  useEffect(() => {
    // Simula carga de datos (reemplaza con tu lógica real de obtención de datos)
    setTimeout(() => {
      const fakeDeviceData = [
        { id: 1, name: "Device 1" },
        { id: 2, name: "Device 2" },
        { id: 3, name: "Device 3" }
      ];
      setDeviceData(fakeDeviceData);
    }, 1000); // Tiempo simulado de carga
  }, []); // Se ejecuta solo una vez al montar el componente
  
  if (!user) return <AuthUserForm />;

  /*return (
    <div className="app-container">
      <MainSidebar logout={logout} navigate={navigate} />
      {location.pathname === "/dashboard/Home" ? <HomePage /> : !showPanel && <DeviceList navigate={navigate} />}
      <DeviceDetails deviceName={deviceName} setShowPanel={setShowPanel} />
      {showPanel && <DAQSlider changeMode={changeMode} setChangeMode={setChangeMode} />}
    </div>
  );*/

  return (
    <div className="app-container">
      <MainSidebar logout={logout} navigate={navigate} />
      {location.pathname === "/dashboard/Home" ? (
        <HomePage />
      ) : !showPanel && deviceData ? ( // Verifica que deviceData esté definido
        <DeviceList data={deviceData} navigate={navigate} /> // Pasa los datos a DeviceList
      ) : null}
      <DeviceDetails deviceName={deviceName} setShowPanel={setShowPanel} />
      {showPanel && <DAQSlider changeMode={changeMode} setChangeMode={setChangeMode} />}
    </div>
  );
}
export default DashboardPanel;
