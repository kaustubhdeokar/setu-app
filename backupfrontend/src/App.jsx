import { useState } from "react";
import "./App.css";
import Login from "./components/Login";
import Registration from "./components/Registration";
import UserStats from "./components/UserStats";
import { NavLink } from "react-router-dom";

import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import Flow from "./components/Flow";

function App() {

  const PrivateRoute = ({ children }) => {
    const token = localStorage.getItem("access_token");
    return token ? children : <Navigate to="/login" />;
  };

  return (
    <>
      <div>
        <Router>
          <Routes>
            <Route path="/register" element={<Registration />} />
            <Route path="/login" element={<Login />} />
            <Route path="/" element={<Login />} />
            <Route
              path="/kyc"
              element={
                <PrivateRoute>
                  <Flow />
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
          </Routes>
          <p>
            Go to <NavLink to="/stats">/stats</NavLink> for statistics. (Admin){" "}
            <br />
            Go to <NavLink to="/login">/login</NavLink> for login. <br />
            Go to <NavLink to="/kyc">/kyc</NavLink> for validation.
          </p>
        </Router>
      </div>
    </>
  );
}

export default App;
