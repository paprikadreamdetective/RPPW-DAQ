import DAQSlider from "../components/DAQSlider";
import MainSidebar from "../components/MainSidebar";
import { useState } from "react";
import '../styles/ControlPage.css';
function ControlPage() {
    const [sidebarOpen, setSidebarOpen] = useState(false);
    const handleSidebarToggle = (isOpen) => {
        setSidebarOpen(isOpen);
    };
    return (
       <>
        <div className="control-panel-page">
            <MainSidebar onToggle={handleSidebarToggle} />
            <div className={`control-panel-container ${sidebarOpen ? "sidebar-open" : ""}`}>
                <DAQSlider />   
            </div>
                
        </div>
        </>
    );
}

export default ControlPage;