import React, { useState, useEffect } from 'react';
import PwmControl from './components/PwmControl';
import DaqInfo from './components/DAQInfo';
import Graph from './components/Graph';
import './App.css'

function App() {
  const graphUrl = "http://192.168.100.174/zabbix/index.php?name=Admin&password=&enter=Sign&action=dashboard.view&kiosk=1&dashboardid=47320";

  //const [authToken, setAuthToken] = useState(null);
  //const [graphUrl, setGraphUrl] = useState('');

  const [changeMode, setChangeMode] = useState(0);
  /*
  const [showMoreConfig, setShowMoreConfig] = useState(false); 

  const [pwmChannel, setPwmChannel] = useState(null); 
  const [value, setValue] = useState(null);
  const [mode, setMode] = useState(null);
  const [upperBound, setUpperBound] = useState(null);
  const [lowerBound, setLowerBound] = useState(null);
  const [setpoint, setSetpoint] = useState(null);
  const [adcChannel, setAdcChannel] = useState(null);
  const [time_on, setTime_On] = useState(null);
  const [time_off, setTime_Off] = useState(null);

  const [outputLowerLimit, setOutputLowerLimit] = useState(null);
  const [outputUpperLimit, setOutputUpperLimit] = useState(null);
  const [pidKp, setPidKp] = useState(null); 
  const [pidKi, setPidKi] = useState(null); 
  const [pidKd, setPidKd] = useState(null); 

  const [sampleTimeUs, setSampleTimeUs] = useState(null);
  const [ghFilter, setghFilter] = useState(null);*/


  const [DAQInfo, setDAQInfo] = useState(null);

  /*const handleModeChange = (e) => {
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
        lower_bound: lowerBound,
        output_lower_limit: outputLowerLimit,
        output_upper_limit: outputUpperLimit,
        kp_value: pidKp,
        ki_value: pidKi,
        kd_value: pidKd,
        sample_time_us: sampleTimeUs,
        gh_filter: ghFilter
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
  };*/

  useEffect(() => {
    fetch('http://192.168.100.164:5000/get_daq_info')  
      .then(response => response.json())
      .then(data => setDAQInfo(data))
      .catch(error => console.error('Error fetching the data:', error));
  }, []);


  

  return (
  <>
    <div className="dashboard-container">
      {/*<div className="daq-info">
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
      </div>*/}
      <DaqInfo DAQInfo={DAQInfo} />
      <Graph graphUrl={graphUrl} />
      
      {/*<div className="dashboard-charts">
        <h3>Contenedor 2: Charts</h3>
        <div className="charts-content">
          <div style={{ display: 'flex', justifyContent: 'center' }}>
            <iframe
              src={graphUrl}
              title="Zabbix Graph"
              width="1000"
              height="200"
              frameBorder="0"
              allowFullScreen
            />
          </div>
        </div>
      </div>*/}
      
      <PwmControl changeMode={changeMode} setChangeMode={setChangeMode} />

      {/*<div className="control-container">
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
            
            <input
                  type="number"
                  value={time_on}
                  onChange={(e) => setTime_On(e.target.value)}
                  placeholder="Ingrese el modo de control"
                
                />
          </div>
          
          <div className="field-group">
            <label htmlFor="time-off">Time Off</label>
            
            <input
                  type="number"
                  value={time_off}
                  onChange={(e) => setTime_Off(e.target.value)}
                  
                  
                />
          </div>
          </>
          )}


          {changeMode === 2 && (
            <>
              <>
            <div className="field-group">
              <label htmlFor="setpoint">Setpoint</label>
              
              <input
                  type="number"
                  value={setpoint}
                  onChange={(e) => setSetpoint(e.target.value)}
                  className="input-field"
                />
            </div>

          <div className="field-group">
            <label htmlFor="adc-channel">ADC Channel</label>
           
            <input
                  type="number"
                  value={adcChannel}
                  onChange={(e) => setAdcChannel(e.target.value)}
                  className="input-field"
                />
          </div>
          </>


              <div className="field-group">
                <label htmlFor="output-limits">Output Limits</label>
                <input
                  type="number"
                  value={outputLowerLimit}
                  onChange={(e) => setOutputLowerLimit(e.target.value)}
                  className="input-field"
                />
              </div>

              <div className="field-group">
                <label htmlFor="output-limits">Output Limits</label>
                <input
                  type="number"
                  value={outputUpperLimit}
                  onChange={(e) => setOutputUpperLimit(e.target.value)}
                  className="input-field"
                />
              </div>



              <div className="field-group">
                <label htmlFor="pid-kp">PID Kp</label>
                <input
                  type="number"
                  value={pidKp}
                  onChange={(e) => setPidKp(e.target.value)}
                  className="input-field"
                />
              </div>

              <div className="field-group">
                <label htmlFor="pid-ki">PID Ki</label>
                <input
                  type="number"
                  value={pidKi}
                  onChange={(e) => setPidKi(e.target.value)}
                  className="input-field"
                />
              </div>

              <div className="field-group">
                <label htmlFor="pid-kd">PID Kd</label>
                <input
                  type="number"
                  value={pidKd}
                  onChange={(e) => setPidKd(e.target.value)}
                  className="input-field"
                />
              </div>

              <div className="field-group">
                <label htmlFor="sample-time-us">Sample Time (us)</label>
                <input
                  type="number"
                  value={sampleTimeUs}
                  onChange={(e) => setSampleTimeUs(e.target.value)}
                  className="input-field"
                />
              </div>

              <div className="field-group">
                <label htmlFor="gh-filter">GH Filter</label>
                <input
                  type="number"
                  value={ghFilter}
                  onChange={(e) => setghFilter(e.target.value)}
                  className="input-field"
                />
              </div>
              
              
              
              
            </>
          )}
         
          
            {changeMode === 3 && (<>

            <div className="field-group">
            <label htmlFor="adc-channel">ADC Channel</label>
            
            <input
                  type="number"
                  value={adcChannel}
                  onChange={(e) => setAdcChannel(e.target.value)}
                  className="input-field"
                />
          </div>

          <div className="field-group">
            <label htmlFor="lower-bound">Lower Bound</label>
            
            <input
                  type="number"
                  value={lowerBound}
                  onChange={(e) => setLowerBound(e.target.value)}
                  className="input-field"
                />
          </div>

          <div className="field-group">
            <label htmlFor="upper-bound">Upper Bound</label>
           
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
       
      </div>*/}
    </div>
  </>
  );
}

export default App;


