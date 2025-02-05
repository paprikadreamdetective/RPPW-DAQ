import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import './Graph.css';
//import MotorControl from './MotorControl';
//import VerticalSwipeToSlide from './VerticalPanel';
function Graph({ graphUrl }) {
  const [data, setData] = useState([]);

  // Genera datos sintéticos de temperatura
  const generateFakeData = () => {
    return {
      time: new Date().toLocaleTimeString().split(' ')[0], // HH:MM:SS
      temp1: (20 + Math.random() * 5).toFixed(2),
      temp2: (22 + Math.random() * 5).toFixed(2),
      temp3: (24 + Math.random() * 5).toFixed(2),
      temp4: (26 + Math.random() * 5).toFixed(2),
    };
  };

  useEffect(() => {
    const interval = setInterval(() => {
      setData((prevData) => {
        const newData = [...prevData, generateFakeData()];
        return newData.length > 20 ? newData.slice(1) : newData; // Mantiene solo 20 datos
      });
    }, 1000);

    return () => clearInterval(interval);
  }, []);
  return (
    <div className="dashboard-charts">
      <h3>Temperatur Graphs</h3>
      <div className="charts-grid">
        {[1, 2, 3, 4].map((i) => (
          <div className="chart-container" key={i}>
            <h4>Sensor {i}</h4>
            <ResponsiveContainer width="100%" height={150}>
              <LineChart data={data}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="time" />
                <YAxis domain={[15, 35]} label={{ value: '°C', angle: -90, position: 'insideLeft' }} />
                <Tooltip />
                <Line type="monotone" dataKey={`temp${i}`} stroke="#8884d8" strokeWidth={2} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        ))}
      </div>
      {/*<div className="charts-content">
      </div>*/}
      
    </div>
  );
}

export default Graph;
