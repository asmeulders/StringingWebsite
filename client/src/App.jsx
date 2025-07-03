import { useState, useEffect } from 'react'
import axios from "axios";
import Home from './Home.jsx';
import Login from './Login.jsx';
import { BrowserRouter as Router, Route, Routes} from "react-router-dom"

function App() {
  axios.defaults.withCredentials = true // login stuff; 'supposed to go in index.js'

  return (
    <Router>
      <div className="App">
        {/* Navbar */}
        <div className="content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
          </Routes>
        </div>
      </div>
    </Router>
  )
}

export default App
