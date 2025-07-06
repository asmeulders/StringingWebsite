import { useState, useEffect } from 'react'
import axios from "axios";
import Home from './Home.jsx';
import Login from './Login.jsx';
import Register from './Register.jsx'
import Dashboard from './Dashboard.jsx'
import CreateOrder from './CreateOrder.jsx'
import { BrowserRouter as Router, Route, Routes} from "react-router-dom"

function App() {
  // axios.defaults.withCredentials = true // login stuff; 'supposed to go in index.js'
  const [user, setUser] = useState(null);
  const apiUrl = "http://localhost:5000/api/"

  // useEffect(() => {
  //   async function fetchData() {
  //     const response = await axios.get(apiUrl + "check_session");
  //     if (response.ok) {
  //       const data = await response.json();
  //       setUser(data);
  //     }
  //   }
  //   fetchData();
  // }, []);

  // function logout() {
  //   setUser(null);
  //   fetch("/api/logout", {
  //     method: "DELETE",
  //   });
  //   navigate("/");
  // }

  return (
    <Router>
      <div className="App">
        {/* Navbar */}
        <div className="content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/create-order" element={<CreateOrder />} />
          </Routes>
        </div>
      </div>
    </Router>
  )
}

export default App
