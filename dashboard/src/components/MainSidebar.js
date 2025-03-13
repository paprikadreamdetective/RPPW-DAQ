// Sidebar.js

import { useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faHome, faMicrochip, faMicroscope, faSignOutAlt, faBars, faClose, faCircleQuestion } from "@fortawesome/free-solid-svg-icons";
import "./SidebarHome.css";

function MainSidebar({ sidebarOpen, toggleSidebar, navigate, logout }) {
  /*const [sidebarOpen, setSidebarOpen] = useState(false);*/
  return (
    <div className={`sidebar ${sidebarOpen ? "open" : ""}`}>
      <button className="menu-button" onClick={toggleSidebar}>
        
        <FontAwesomeIcon icon={sidebarOpen ? faClose : faBars} />
        {sidebarOpen && <span className="sidebar-text">BioReactify</span>}
      </button>
      <br/>
      
      <hr/>
      <div className="sidebar-options">
        <div className="sidebar-item" onClick={() => navigate("/dashboard/Home")}> 
          <FontAwesomeIcon icon={faHome} size="2x" color="white"/> 
          {sidebarOpen && <span className="sidebar-item-text">Home</span>}
        </div>
        <div className="sidebar-item" onClick={() => navigate("/")}> 
          <FontAwesomeIcon icon={faMicrochip} size="2x" color="white"/> 
          {sidebarOpen && <span className="sidebar-item-text">Devices</span>}
        </div>
        <div className="sidebar-item" onClick={() => navigate("/dashboard/Experiments")}> 
          <FontAwesomeIcon icon={faMicroscope} size="2x" color="white"/> 
          {sidebarOpen && <span className="sidebar-item-text">Experiments</span>}
        </div>
        <div className="sidebar-item" onClick={() => navigate("/dashboard/About")}> 
          <FontAwesomeIcon icon={faCircleQuestion} size="2x" color="white"/> 
          {sidebarOpen && <span className="sidebar-item-text">About</span>}
        </div>
        <div className="sidebar-item" onClick={logout}> 
          <FontAwesomeIcon icon={faSignOutAlt} size="2x" color="white"/> 
          {sidebarOpen && <span className="sidebar-item-text">Logout</span>}
        </div>
      </div>
    </div>
  );
}

export default MainSidebar;