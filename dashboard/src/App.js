import React, { useState, useEffect, useRef } from 'react';
import './App.css'
function App() {
    const [value, setValue] = useState('');
    const [mode, setMode] = useState('');
    const [changeMode, setChangeMode] = useState(0);

    const [instruction, setIstruction] = useState('');
    //const iframeRef = useRenf(null);

    const handleModeChange = (e) => {
      e.preventDefault();
      setChangeMode(Number(e.target.value));
      console.log(changeMode);
    };

    const handle_pwm_set_mode = async (e) => {
        e.preventDefault();
        try {
            const data = {
                value: value,
                mode_control: mode,
              };
            const response = await fetch('http://192.168.100.164:5000/set_mode_manual', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
            });
            const responseData = await response.json();
            if (responseData.success) {
                window.confirm(responseData.message);
                //cerrarModalInsertar();
            } else {
                window.confirm(responseData.message);
                //cerrarModalInsertar();
            }
        } catch (error) {
            window.confirm(error);
            //cerrarModalInsertar();
        }
    };

    
    return (
      <>
        {/*<div className="container">
          <div className="modal">
            <h1 className="title">Enviar Instrucción a la Raspberry Pi</h1>
            <form onSubmit={handle_pwm_set_mode}>
              <label>Valor PWM</label>
              <input
                type="number"
                value={value}
                onChange={(e) => setValue(e.target.value)}
                placeholder="Ingrese el valor PWM"
                className="input-field"
              />
              <label>Modo Control</label>
              <input
                type="number"
                value={mode}
                onChange={(e) => setMode(e.target.value)}
                placeholder="Ingrese el modo de control"
                className="input-field"
              />
              <button type="submit" className="submit-button">Enviar Instrucción</button>
            </form>



          </div>

          <div >
                <h2>Dashboard de Node-RED</h2>
                <iframe
                    ref={iframeRef}
                    src="http://192.168.100.164:1880/ui/#/0" // Cambia esta URL a la de tu dashboard
                    title="Node-RED Dashboard"
                    width="600px"
                    height="600px"
                    style={{ border: 'none' }}
                ></iframe>

        
            </div>

        </div>*/}
  
  <div className="dashboard-container">
    {/* Contenedor de DAQ */}
    <div className="daq-info">
      <h3>Contenedor 1: DAQ Description</h3>
      <div className="daq-content"></div>
    </div>

    {/* Contenedor de Charts */}
    <div className="dashboard-charts">
      <h3>Contenedor 2: Charts</h3>
      <div className="charts-content"></div>
    </div>

    {/* Contenedor de Control PWM */}
    <div className="control-container">
      <h3>PWM MODE CONTROL</h3>
      <label htmlFor="mode">Mode</label>
      <select id="mode" className="dropdown" onChange={handleModeChange}>
        <option value={0}>MANUAL</option>
        <option value={1}>TIMER</option>
        <option value={2}>PID</option>
        <option value={3}>ON / OFF</option>
      </select>

      <div className="fields-container">
        
        <div className={`field-group ${changeMode >= 0 && changeMode <= 3 ? 'visible' : ''}`}>
          <label htmlFor="pwm-channel">PWM Channel</label>
          <input type="number" id="pwm-channel" />
        </div>

        <div className={`field-group ${changeMode >= 0 && changeMode <= 3 ? 'visible' : ''}`}>
          <label htmlFor="pwm-value">PWM Value</label>
          <input type="number" id="pwm-value" />
        </div>

        {changeMode === 1 && (
          <>
        <div className="field-group">
          <label htmlFor="time-on">Time On</label>
          <input type="text" id="time-on" />
        </div>
        
        <div className="field-group">
          <label htmlFor="time-off">Time Off</label>
          <input type="text" id="time-off" />
        </div>
        </>
        )}
        {changeMode === 2 && (<>
          <div className="field-group">
            <label htmlFor="setpoint">Setpoint</label>
            <input type="text" id="setpoint" />
          </div>

        <div className="field-group">
          <label htmlFor="adc-channel">ADC Channel</label>
          <input type="text" id="adc-channel" />
        </div>
        </>)}
        
         {changeMode === 3 && (<>
        <div className="field-group">
          <label htmlFor="lower-bound">Lower Bound</label>
          <input type="text" id="lower-bound" />
        </div>

        <div className="field-group">
          <label htmlFor="upper-bound">Upper Bound</label>
          <input type="text" id="upper-bound" />
        </div>
        </>)}
            <button className="save-button">Save</button>
      </div>
    </div>
  </div>
  </>
  );
}

export default App;


