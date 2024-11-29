import React from 'react';
import './Graph.css';
import MotorControl from './MotorControl';

function Graph({ graphUrl }) {
  return (
    <div className="dashboard-charts">
      <h3>Contenedor 2: Charts</h3>
      <div className="charts-content">
        {/*
        {<div style={{ display: 'flex', justifyContent: 'center' }}>
          <iframe
            src={graphUrl}
            title="Zabbix Graph"
            width="1000"
            height="200"
            frameBorder="0"
            allowFullScreen
          />
          
          
        </div>*/}
        <MotorControl></MotorControl>
      </div>
      
    </div>
  );
}

export default Graph;
