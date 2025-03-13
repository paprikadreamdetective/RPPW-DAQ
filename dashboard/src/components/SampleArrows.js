// SampleArrows.js
import React from "react";

export const SampleNextArrow = (props) => {
  const { className, style, onClick } = props;
  return <div className={className} style={{ ...style, display: "block", color: "black" }} onClick={onClick} />;
};

export const SamplePrevArrow = (props) => {
  const { className, style, onClick } = props;
  return <div className={className} style={{ ...style, display: "block", color: "black" }} onClick={onClick} />;
};
