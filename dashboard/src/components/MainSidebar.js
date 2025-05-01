import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faBars,
  faTimes,
  faCogs,
  faTable,
  faList,
  faUser,
} from "@fortawesome/free-solid-svg-icons";

import "../styles/MainSidebar.css";

function MainSidebar({ onToggle }) {
  const [isOpen, setIsOpen] = useState(false);
  const navigate = useNavigate();

  const handleTrigger = () => {
    const newState = !isOpen;
    setIsOpen(newState);
    if (onToggle) onToggle(newState);
  };

  const menuItems = [
    { icon: faUser, label: "Inicio", path: "/home" },
    {  icon: faCogs, label: "Experimentos", path: "/experiments" },
    { icon: faTable, label: "Panel de Control", path: "/control_panel" },
    { icon: faList, label: "Opción 3", path: "/option3" },
  ];

  return (
    <div className={`sidebar ${isOpen ? "sidebar--open" : ""}`}>
      <div className="trigger" onClick={handleTrigger}>
        <FontAwesomeIcon icon={isOpen ? faTimes : faBars} />
      </div>

      {menuItems.map((item, index) => (
        <div
          key={index}
          className="sidebar-position"
          onClick={() => navigate(item.path)}
        >
          <FontAwesomeIcon icon={item.icon} />
          <span>{item.label}</span>
        </div>
      ))}
    </div>
  );
}

export default MainSidebar;