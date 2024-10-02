import React, { useState, useEffect } from 'react';
import './App.css'

function App() {
  const graphUrl = 'http://192.168.100.174:10051/zabbix/chart.php?from=now-1h&to=now&itemids%5B0%5D=47320&type=0&resolve_macros=1&profileIdx=web.item.graph.filter&profileIdx2=47320&width=1350&height=200';

  const [changeMode, setChangeMode] = useState(0);

  const [pwmChannel, setPwmChannel] = useState(null); 
  const [value, setValue] = useState(null);
  const [mode, setMode] = useState(null);
  const [upperBound, setUpperBound] = useState(null);
  const [lowerBound, setLowerBound] = useState(null);
  const [setpoint, setSetpoint] = useState(null);
  const [adcChannel, setAdcChannel] = useState(null);
  const [time_on, setTime_On] = useState(null);
  const [time_off, setTime_Off] = useState(null);

  const [outputLimits, setOutputLimits] = useState(null);
  const [pidKp, setPidKp] = useState(null); 
  const [pidKi, setPidKi] = useState(null); 
  const [pidKd, setPidKd] = useState(null); 

  const [sampleTimeUs, setSampleTimeUs] = useState(null);
  const [ghFilter, setghFilter] = useState(null);


  const [DAQInfo, setDAQInfo] = useState(null);

  const handleModeChange = (e) => {
    e.preventDefault();
    setChangeMode(Number(e.target.value));
    console.log(changeMode);
  };

  const handle_pwm_set_mode = async (e) => {
    e.preventDefault();
    try {
      const data = {
        pwm_channel: pwmChannel,
        pwm_value: value,
        mode_control: changeMode,
        time_on: time_on,
        time_off: time_off,
        setpoint: setpoint,
        adc_channel: adcChannel,
        upper_bound: upperBound,
        lower_bound: lowerBound
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

  useEffect(() => {
    fetch('http://192.168.100.164:5000/get_daq_info')  
      .then(response => response.json())
      .then(data => setDAQInfo(data))
      .catch(error => console.error('Error fetching the data:', error));
  }, []);

  return (
  <>
    <div className="dashboard-container">
      
      <div className="daq-info">
        <h3>Contenedor 1: DAQ Description</h3>
        
          {DAQInfo ? (
            <div className='daq-info-fields-container'>
              
              <p><strong>Location:</strong> {DAQInfo.location}</p>
              <p><strong>Hardware:</strong> {DAQInfo.hardware}</p>
              <p><strong>Address:</strong> {DAQInfo.address}</p>
              <p><strong>Analog Inputs:</strong> {DAQInfo.analog_inputs}</p>
              <p><strong>PWM Outputs:</strong> {DAQInfo.pwm_outputs}</p>
              <p><strong>I2C Address:</strong> {DAQInfo.i2c_address}</p>
            </div>
            ) : (
            <p>Loading hardware information...</p>
          )}
        
      </div>

      
      <div className="dashboard-charts">
        <h3>Contenedor 2: Charts</h3>
        <div className="charts-content">

        <div style={{ display: 'flex', justifyContent: 'center' }}>
      <iframe
        src={graphUrl}
        title="Zabbix Graph"
        width="1350"
        height="200"
        frameBorder="0"
        allowFullScreen
      />
    </div>

        </div>
      </div>

      
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
            {/*<input type="number" id="pwm-channel" />*/}
            <input
                  type="number"
                  value={pwmChannel}
                  onChange={(e) => setPwmChannel(e.target.value)}
                  placeholder="Ingrese el modo de control"
                  className="input-field"
                />
          </div>

          <div className={`field-group ${changeMode >= 0 && changeMode <= 3 ? 'visible' : ''}`}>
            <label htmlFor="pwm-value">PWM Value</label>
            {/*<input type="number" id="pwm-value" />*/}
            <input
                  type="number"
                  value={value}
                  onChange={(e) => setValue(e.target.value)}
                  placeholder="Ingrese el modo de control"
                  className="input-field"
                />
          </div>

          {changeMode === 1 && (
            <>
          <div className="field-group">
            <label htmlFor="time-on">Time On</label>
            {/*<input type="text" id="time-on" />*/}
            <input
                  type="number"
                  value={time_on}
                  onChange={(e) => setTime_On(e.target.value)}
                  placeholder="Ingrese el modo de control"
                
                />
          </div>
          
          <div className="field-group">
            <label htmlFor="time-off">Time Off</label>
            {/*<input type="text" id="time-off" />*/}
            <input
                  type="number"
                  value={time_off}
                  onChange={(e) => setTime_Off(e.target.value)}
                  
                  
                />
          </div>
          </>
          )}
          {changeMode === 2 && (<>
            <div className="field-group">
              <label htmlFor="setpoint">Setpoint</label>
              {/*<input type="text" id="setpoint" />*/}
              <input
                  type="number"
                  value={setpoint}
                  onChange={(e) => setSetpoint(e.target.value)}
                  className="input-field"
                />
            </div>

          <div className="field-group">
            <label htmlFor="adc-channel">ADC Channel</label>
            {/*<input type="text" id="adc-channel" />*/}
            <input
                  type="number"
                  value={adcChannel}
                  onChange={(e) => setAdcChannel(e.target.value)}
                  className="input-field"
                />
          </div>
          </>)}
          
            {changeMode === 3 && (<>

            <div className="field-group">
            <label htmlFor="adc-channel">ADC Channel</label>
            {/*<input type="text" id="adc-channel" />*/}
            <input
                  type="number"
                  value={adcChannel}
                  onChange={(e) => setAdcChannel(e.target.value)}
                  className="input-field"
                />
          </div>

          <div className="field-group">
            <label htmlFor="lower-bound">Lower Bound</label>
            {/*<input type="text" id="lower-bound" />*/}
            <input
                  type="number"
                  value={lowerBound}
                  onChange={(e) => setLowerBound(e.target.value)}
                  className="input-field"
                />
          </div>

          <div className="field-group">
            <label htmlFor="upper-bound">Upper Bound</label>
            {/*<input type="text" id="upper-bound" />*/}
            <input
                  type="number"
                  value={upperBound}
                  onChange={(e) => setUpperBound(e.target.value)}
                  className="input-field"
                />
          </div>
          </>)}
              <button className="save-button" onClick={handle_pwm_set_mode}>Save</button>
        </div>
      </div>
    </div>
  </>
  );
}

export default App;


