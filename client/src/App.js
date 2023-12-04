import { BrowserRouter, Route, Routes } from "react-router-dom";
import React from "react";

import DashboardPage from "./Pages/DashboardPage";
import LoginPage from "./Pages/LoginPage";
import ResultPage from "./Pages/ResultPage";
import RegisterPage from "./Pages/RegisterPage";
import TestPage from "./Pages/TestPage";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="" element={<DashboardPage />} />
          <Route path="test/:testid" element={<TestPage />} />
          <Route path="test/:testid/results" element={<ResultPage />} />
          <Route path="register" element={<RegisterPage />} />
          <Route path="login" element={<LoginPage />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
