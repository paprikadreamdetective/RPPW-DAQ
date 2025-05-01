import { useContext, useState } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../components/AuthContext";
import MainSidebar from "../components/MainSidebar";

import "../styles/HomePage.css";

function HomePage() {
  const { user, logout } = useContext(AuthContext);
  const navigate = useNavigate();
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  const handleSidebarToggle = (isOpen) => {
    setSidebarOpen(isOpen);
  };

  return (
    <div className="page">
      <MainSidebar onToggle={handleSidebarToggle} />
      <div className={`home-container ${sidebarOpen ? "sidebar-open" : ""}`}>
        <h1>¡Bienvenido, {user}!</h1>
        <p>Esta es tu página de inicio. Estás autenticado correctamente.</p>
        <button className="logout-button" onClick={handleLogout}>
          Cerrar sesión
        </button>
      </div>
    </div>
  );
}

export default HomePage;