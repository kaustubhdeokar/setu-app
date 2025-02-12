import { useState } from "react";
import "./App.css";
import KYCValidation from "./components/KYCValidation";
import Login from "./components/Login";
import Registration from "./components/Registration";
import { NavLink } from "react-router-dom";

import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import UserStats from "./components/UserStats";

const PrivateRoute = ({ children }) => {
  const token = localStorage.getItem("access_token");
  return token ? children : <Navigate to="/login" />;
};

function App() {

  return (
    <div>
      <Router>
        <Routes>
          <Route path="/register" element={<Registration />} />
          <Route path="/login" element={<Login />} />
          <Route
            path="/kyc"
            element={
              <PrivateRoute>
                <KYCValidation />
              </PrivateRoute>
            }
          />
          <Route
            path="/stats"
            element={
              <PrivateRoute>
                <UserStats />
              </PrivateRoute>
            }
          />

        <Route path="/" element={<Login />} />
        </Routes>
        <p>
        Go to <NavLink to="/stats">/stats</NavLink> for statistics. (Admin){" "}
        <br />
        Go to <NavLink to="/login">/login</NavLink> for login. <br />
        Go to <NavLink to="/kyc">/kyc</NavLink> for validation.
      </p>

      </Router>
    </div>
  );
}

export default App;
