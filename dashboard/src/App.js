import React, { useState, useEffect } from 'react';

function App() {
    const [value, setValue] = useState(null);
    const [mode, setMode] = useState(null);
    const [isConnected, setIsConnected] = useState(false);

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
        <div>
            <h1>Enviar Instrucción a la Raspberry Pi</h1>
            <form onSubmit={handleSubmit}>
                <textarea
                    value={instruction}
                    onChange={(e) => setInstruction(e.target.value)}
                    placeholder="Escribe la instrucción aquí"
                />
                <button type="submit" >Enviar Instrucción</button>
            </form>
            {/*!isConnected && <p>Conectando al WebSocket...</p>*/}
        </div>
    );
}

export default App;


