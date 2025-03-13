// DAQSlider.js
import Slider from "react-slick";
import PwmControl from "./PwmControl";
import DaqInfo from "./DAQInfo";
import Graph from "./Graph";
import BioMotor from "./BioMotor";
import VerticalSwipeToSlide from "./VerticalPanel";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
function DAQSlider({ changeMode, setChangeMode }) {
  const settings = { dots: true, infinite: true, speed: 500, slidesToShow: 1, slidesToScroll: 1 };
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
