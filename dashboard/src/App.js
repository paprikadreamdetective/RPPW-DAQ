import React, { useState, useEffect } from 'react';
import PwmControl from './components/PwmControl';
import DaqInfo from './components/DAQInfo';
import Graph from './components/Graph';
import './App.css'

function App() {
  const graphUrl = "http://192.168.100.174/zabbix/index.php?name=Admin&password=&enter=Sign&action=dashboard.view&kiosk=1&dashboardid=47320";
  const [changeMode, setChangeMode] = useState(0);
  const [DAQInfo, setDAQInfo] = useState(null);

  useEffect(() => {
    fetch('http://192.168.100.164:5000/get_daq_info')  
      .then(response => response.json())
      .then(data => setDAQInfo(data))
      .catch(error => console.error('Error fetching the data:', error));
  }, []);

return (
  <>
    <div className="dashboard-container">
      <DaqInfo DAQInfo={DAQInfo} />
      <Graph graphUrl={graphUrl} />
      <PwmControl changeMode={changeMode} setChangeMode={setChangeMode} />
    </div>
  </>
  );
}

export default App;


