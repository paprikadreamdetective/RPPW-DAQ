import React, { Component } from "react";
import Slider from "react-slick";
import "./VerticalPanel.css";
import MotorControl from "./MotorControl";
function VerticalSwipeToSlide() {
  const settings = {
    dots: false,
    infinite: true,
    slidesToShow: 1,
    slidesToScroll: 1,
    vertical: true,
    verticalSwiping: true,
    swipeToSlide: true,
    arrows: true, // Activa las flechas de navegación
    swipe: false, // Deshabilita el deslizamiento con el mouse o touch
    draggable: false, // Deshabilita arrastrar el slider
    beforeChange: function(currentSlide, nextSlide) {
      console.log("before change", currentSlide, nextSlide);
    },
    afterChange: function(currentSlide) {
      console.log("after change", currentSlide);
    }
  };
  return (
    <>
    {/*<div className="slider-container">*/}
    
    {/*<div className="vertical-panel-slider">
    <div className="slider-container">
      <Slider {...settings}>
        <div className="vertical-panel-container">
          <h3>Motor X</h3>
          <MotorControl></MotorControl>
        </div>
        <div className="vertical-panel-container">
          <h3>Motor Y</h3>
          <MotorControl></MotorControl>
        </div >
        <div className="vertical-panel-container">
          <h3>Motor Z</h3>
          <MotorControl></MotorControl>
        </div>
      </Slider>
    </div>
    </div>*/}
    <div className="vertical-panel-container">
      <h2>Motor Control Panel</h2>
      <div className="vertical-panel-list">
        <div className="vertical-panel-item">
          <h3>Motor X</h3>
          <MotorControl />
        </div>
        <div className="vertical-panel-item">
          <h3>Motor Y</h3>
          <MotorControl />
        </div>
        <div className="vertical-panel-item">
          <h3>Motor Z</h3>
          <MotorControl />
        </div>
      </div>
    </div>
    </>
  );
}

export default VerticalSwipeToSlide;