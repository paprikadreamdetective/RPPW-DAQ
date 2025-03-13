import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { useContext } from "react";
import { AuthProvider, AuthContext } from "./components/AuthContext";
//import Dashboard from "./components/Dashboard";
import AuthUserForm from "./components/AuthForm";
import HomePage from "./pages/HomePage";
import ExperimentsPage from "./pages/ExperimentsPage";
import DashboardPanel from "./pages/DashboardPanel";
import "./App.css";

function AppRoutes() {
  const { user } = useContext(AuthContext);
  
  return (
    <>
    {/*<Routes>
      <Route path="/" element={user ? <Dashboard /> : <Navigate to="/login" />} />
      <Route path="/login" element={user ? <Navigate to="/" /> : <AuthUserForm />} />
    </Routes>*/}
    <Routes>
      <Route path="/" element={<Navigate to="/login" />} />
      {/*<Route path="/" element={user ? <Navigate to="/dashboard" /> : <Navigate to="/login" />} />*/}
      <Route path="/login" element={user ? <Navigate to="/dashboard" /> : <AuthUserForm />} />
      <Route path="Home" element={<HomePage />} />
      <Route path="Experiments" element={<ExperimentsPage />} />
      <Route path="/dashboard" element={<DashboardPanel showDevices={true}/>} />
      {/*<Route path="/dashboard/:Home" element={<HomePage />} />*/} {/* Ruta para dispositivos */}
      <Route path="/dashboard/:deviceName" element={<DashboardPanel />} /> {/* Ruta para dispositivos */}
    </Routes>
    </>
  );
}

function App() {
  return (
    <AuthProvider>
      <Router>
        <AppRoutes />
      </Router>
    </AuthProvider>
  );
}

export default App;
