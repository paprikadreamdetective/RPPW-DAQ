import React from 'react';

function DaqInfo({ DAQInfo }) {
  return (
    <div className="daq-info">
      <h3>Contenedor 1: DAQ Description</h3>
      {DAQInfo ? (
        <div className="daq-info-fields-container">
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
  );
}

export default DaqInfo;