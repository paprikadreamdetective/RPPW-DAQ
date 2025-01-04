// src/components/Dashboard.js
import React, { useState } from "react";
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
