/*import { createContext, useState, useEffect } from "react";

// Crear contexto
export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);

  // Cargar usuario desde Local Storage (mantener sesión activa)
  useEffect(() => {
    const loggedUser = JSON.parse(localStorage.getItem("user"));
    if (loggedUser) {
      setUser(loggedUser);
    }
  }, []);

  // Función para iniciar sesión (simulación)
  const login = (username, password) => {
    if (username === "admin" && password === "1234") { // Simulación
      const userData = { username };
      setUser(userData);
      localStorage.setItem("user", JSON.stringify(userData)); // Guardar sesión
    } else {
      alert("Usuario o contraseña incorrectos.");
    }
  };

  // Cerrar sesión
  const logout = () => {
    setUser(null);
    localStorage.removeItem("user");
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};*/

import { createContext, useState, useEffect } from "react";
//import { useNavigate } from "react-router-dom";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
   
  useEffect(() => {
    const storedUser = JSON.parse(localStorage.getItem("user"));
    if (storedUser) {
      setUser(storedUser.username);
    }
  }, []);

  const login = (username) => {
    localStorage.setItem("user", JSON.stringify({ username }));
    setUser(username);
  };

  const logout = () => {
    localStorage.removeItem("user");
    setUser(null);
    //navigate("/login");
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

