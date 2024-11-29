import React, { useState } from "react";
import "./MotorControl.css";

const MotorControl = () => {
  const [speed, setSpeed] = useState("");
  const [revolutions, setRevolutions] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    const data = {
      speed: parseInt(speed),
      revolutions: parseInt(revolutions),
    };

    try {
      const response = await fetch("http://192.168.100.164:5000/control_motor", {
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

  return (
    <div className="container">
      <h1>Stepper Motor Peristaltic Liquid Pump Control</h1>
      <form className="form" onSubmit={handleSubmit}>
        <input
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
        />
        <button type="submit" className="button">
          Enviar Comando
        </button>
        {error && <p className="error">{error}</p>}
      </form>
    </div>
  );
};

export default MotorControl;
