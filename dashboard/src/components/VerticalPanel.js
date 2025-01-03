import React, { Component } from "react";
import Slider from "react-slick";
import "./VerticalPanel.css";

function VerticalSwipeToSlide() {
  const settings = {
    dots: false,
    infinite: true,
    slidesToShow: 1,
    slidesToScroll: 1,
    vertical: true,
    verticalSwiping: true,
    swipeToSlide: true,
    arrows: true // Activa las flechas de navegación
    /*beforeChange: function(currentSlide, nextSlide) {
      console.log("before change", currentSlide, nextSlide);
    },
    afterChange: function(currentSlide) {
      console.log("after change", currentSlide);
    }*/
  };
  return (
    <>
    {/*<div className="slider-container">*/}
    
    <div className="vertical-panel-slider">
      <Slider {...settings}>
        <div className="vertical-panel-container">
          <h3>1</h3>
        </div>
        <div className="vertical-panel-container">
          <h3>2</h3>
        </div >
        <div className="vertical-panel-container">
          <h3>3</h3>
        </div>
      </Slider>
    </div>
    </>
  );
}

export default VerticalSwipeToSlide;