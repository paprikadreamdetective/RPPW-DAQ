import React, { useState } from "react";
import { Slider, Typography, Button, Switch, FormControlLabel } from "@mui/material";
import "./MotorControl.css";
import "./BioMotor.css";
//mport "./SliderControl.css";

const BioMotor = () => {
    const [sliderValue, setSliderValue] = useState(0); // Valor del slider
  const [speed, setSpeed] = useState("");
  const [revolutions, setRevolutions] = useState("");
  const [error, setError] = useState("");
  const [isMotorOn, setIsMotorOn] = useState(false); // Estado del toggle switch

  const handleSubmit = async (e) => {
    e.preventDefault();
    const data = {
      speed: parseInt(speed),
      revolutions: parseInt(revolutions),
    };

    try {
      const response = await fetch("http://192.168.100.164:5001/control_motor", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
      const responseData = await response.json();
      window.confirm(responseData.message);
    } catch (error) {
      setError("Error al enviar la solicitud.");
    }
  };

  
  const handlePowerCommand = async (command) => {
    try {
      const response = await fetch("http://192.168.100.164:5001/control_motor", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ command }),
      });
      const responseData = await response.json();
      //window.confirm(responseData.message);
    } catch (error) {
      setError("Error al enviar el comando de encendido/apagado.");
    }
  };

  const toggleMotor = () => {
    const command = isMotorOn ? "POWER OFF" : "POWER ON";
    setIsMotorOn(!isMotorOn);
    handlePowerCommand(command);
  };

  return (
    <div className="stirring-container">
      <h3>Stirring Motor Control</h3>
      <form className="form" onSubmit={handleSubmit}>
        {/*<input
          type="number"
          className="input"
          placeholder="Velocidad (RPM)"
          value={speed}
          onChange={(e) => setSpeed(e.target.value)}
        />
        <input
          type="number"
          className="input"
          placeholder="Revoluciones"
          value={revolutions}
          onChange={(e) => setRevolutions(e.target.value)}
        />*/}

<div className="slider-container-speed">
<Typography gutterBottom>Velocidad (RPM): {speed}</Typography>
          <Slider
            value={speed}
            min={0}
            max={2000}
            step={10}
            onChange={(e, newValue) => setSpeed(newValue)}
            valueLabelDisplay="auto"
          />
        </div>
        <div className="slider-container-rpm">
        <Typography gutterBottom>Revoluciones: {revolutions}</Typography>
          <Slider
            value={revolutions}
            min={0}
            max={2000}
            step={10}
            onChange={(e, newValue) => setRevolutions(newValue)}
            valueLabelDisplay="auto"
          />
        </div>
        <Button variant="contained" type="submit" className="button">
          Enviar Comando
        </Button>
        {error && <p className="error">{error}</p>}
      </form>

      

      <div className="toggle-switch-container">
        <label className="toggle-switch">
          <input
            type="checkbox"
            checked={isMotorOn}
            onChange={toggleMotor}
          />
          <span className="slider"></span>
        </label>
        <p>{isMotorOn ? "Motor Encendido" : "Motor Apagado"}</p>
      </div>
    </div>
  );
};

export default BioMotor;