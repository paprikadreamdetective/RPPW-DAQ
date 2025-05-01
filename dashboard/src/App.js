import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { useContext } from "react";
import { AuthProvider, AuthContext } from "./components/AuthContext";
import AuthUserForm from "./components/AuthUserForm";
import HomePage from "./pages/HomePage";
import ExperimentsPage from "./pages/ExperimentsPage";
import ControlPage from "./pages/ControlPage";
import "./styles/App.css";

function AppRoutes() {
  const { user } = useContext(AuthContext);

  return (
    <Routes>
      <Route path="/" element={<Navigate to="/login" />} />
      <Route path="/login" element={user ? <Navigate to="/home" /> : <AuthUserForm />} />
      <Route path="/home" element={user ? <HomePage /> : <Navigate to="/login" />} />
      <Route path="/experiments" element={user ? <ExperimentsPage /> : <Navigate to="/login" />} />
      {/*<Route path="/option1" element={user ? <HomePage /> : <Navigate to="/login" />} />*/}
      <Route path="/control_panel" element={user ? <ControlPage /> : <Navigate to="/login" />} />
      <Route path="/option3" element={user ? <HomePage /> : <Navigate to="/login" />} />
    </Routes>
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
