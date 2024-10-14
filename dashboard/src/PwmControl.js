import React, { useState } from 'react';
import './App.css';

function PwmControl({ changeMode, setChangeMode }) {
  const [pwmChannel, setPwmChannel] = useState(null);
  const [value, setValue] = useState(null);
  const [time_on, setTime_On] = useState(null);
  const [time_off, setTime_Off] = useState(null);
  const [setpoint, setSetpoint] = useState(null);
  const [adcChannel, setAdcChannel] = useState(null);
  const [upperBound, setUpperBound] = useState(null);
  const [lowerBound, setLowerBound] = useState(null);
  const [outputLowerLimit, setOutputLowerLimit] = useState(null);
  const [outputUpperLimit, setOutputUpperLimit] = useState(null);
  const [pidKp, setPidKp] = useState(null);
  const [pidKi, setPidKi] = useState(null);
  const [pidKd, setPidKd] = useState(null);
  const [sampleTimeUs, setSampleTimeUs] = useState(null);
  const [ghFilter, setghFilter] = useState(null);

  const handleModeChange = (e) => {
    e.preventDefault();
    setChangeMode(Number(e.target.value));
  };

  const handle_pwm_set_mode = async (e) => {
    e.preventDefault();
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
    try {
      const response = await fetch('http://192.168.100.164:5000/set_mode_manual', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
      const responseData = await response.json();
      window.confirm(responseData.message);
    } catch (error) {
      window.confirm(error);
    }
  };

  return (
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
              
              {/*<button className="save-button" onClick={handle_pid_set_mode}>Save</button>*/}
              
              
            </>
          )}
         
          
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
  );
}

export default PwmControl;
