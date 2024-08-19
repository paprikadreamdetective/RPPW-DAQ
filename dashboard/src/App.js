import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [option1, setOption1] = useState('');
  const [option2, setOption2] = useState('');
  const [option3, setOption3] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    const data = {
      option1,
      option2,
      option3,
    };

    // Cambia la URL a la dirección IP de tu Raspberry Pi Pico W
    axios.post('http://172.30.5.150:8000', data)
      .then(response => {
        console.log('Datos enviados correctamente:', response.data);
      })
      .catch(error => {
        console.error('Error al enviar los datos:', error);
      });
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Enviar Datos a Raspberry Pi Pico W</h1>
        <form onSubmit={handleSubmit}>
          <div>
            <label>Opción 1:</label>
            <input
              type="text"
              value={option1}
              onChange={(e) => setOption1(e.target.value)}
            />
          </div>
          <div>
            <label>Opción 2:</label>
            <input
              type="text"
              value={option2}
              onChange={(e) => setOption2(e.target.value)}
            />
          </div>
          <div>
            <label>Opción 3:</label>
            <input
              type="text"
              value={option3}
              onChange={(e) => setOption3(e.target.value)}
            />
          </div>
          <button type="submit">Enviar</button>
        </form>
      </header>
    </div>
  );
}

export default App;

