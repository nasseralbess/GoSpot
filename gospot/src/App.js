import React from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Home from './pages/Home';
import OnBoarding from './pages/OnBoarding';
import Dashboard from './pages/Dashboard';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/Dashboard" element={<Dashboard />} />
        <Route path="/OnBoarding" element={<OnBoarding />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
