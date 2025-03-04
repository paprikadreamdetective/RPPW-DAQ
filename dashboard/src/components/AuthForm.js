import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useContext } from "react";
import { AuthContext } from "./AuthContext"; // Importa el contexto
import React from "react";
import "./AuthUserForm.css";

const users = [
  { username: "admin", password: "admin123", role: "Admin" },
  { username: "usuario", password: "user123", role: "Usuario" }
];

const AuthUserForm = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const navigate = useNavigate();
  const { login } = useContext(AuthContext); // Usa la función login del contexto

  const handleLogin = (e) => {
    e.preventDefault();
    const user = users.find(
      (u) => u.username === username && u.password === password
    );

    if (user) {
      //sessionStorage.setItem("username", user.username);
      login(user.username); 
      sessionStorage.setItem("role", user.role);
      setMessage("Autenticado con éxito");
      window.alert(`(${user.role}) Usuario: ${user.username} autenticado con éxito`);
      //navigate(user.role === "Admin" ? "/" : "/HomeUsers");
      navigate("/dashboard"); // Redirigir al dashboard
    } else {
      setMessage("Usuario o contraseña incorrectos");
      window.alert("Usuario o contraseña incorrectos");
    }
  };

  return (
    <div className="login-form">
      
      <form>
      <h2 className="sign-in-title">Iniciar Sesión</h2>
        <label className="sign-in-label">Usuario</label>
        <input
          className="sign-in-username-field"
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />

        <label className="sign-in-label">Contraseña</label>
        <input
          className="sign-in-password-field"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <button className="sign-in-button" type="submit" onClick={handleLogin}>
          Entrar
        </button>
        <p>{message}</p>
        <a href="#" className="sign-in-button-register-now">
          ¿No tienes cuenta? Regístrate
        </a>
      </form>
    </div>
  );
};

export default AuthUserForm;
