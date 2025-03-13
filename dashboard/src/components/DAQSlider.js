// DAQSlider.js
import { useState } from "react";
import Slider from "react-slick";
import PwmControl from "./PwmControl";
import DaqInfo from "./DAQInfo";
import Graph from "./Graph";
import BioMotor from "./BioMotor";
import VerticalSwipeToSlide from "./VerticalPanel";
import { SampleNextArrow, SamplePrevArrow } from "./SampleArrows";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
function DAQSlider() {
  const [changeMode, setChangeMode] = useState(0);
  const settings = { dots: true, infinite: true, speed: 500, slidesToShow: 1, slidesToScroll: 1, swipe: false, draggable: false, nextArrow: <SampleNextArrow />, prevArrow: <SamplePrevArrow /> };
  return (
    <div className="slider-container">
      <Slider {...settings}>
        <div className="dashboard-panel"><DaqInfo /></div>
        <div className="dashboard-panel"><Graph /></div>
        <div className="dashboard-panel"><PwmControl changeMode={changeMode} setChangeMode={setChangeMode} /></div>
        <div className="dashboard-panel"><BioMotor /></div>
        <div className="dashboard-panel"><VerticalSwipeToSlide /></div>
      </Slider>
    </div>
  );
}
export default DAQSlider;
