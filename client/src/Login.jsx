import { useState, useEffect } from 'react'
import axios from "axios";

function Login() {
  const [inputs, setInputs] = useState({});
  const baseUrl = "http://localhost:3000/"
  const apiUrl = "http://localhost:5000/api/"

  const handleChange = (event) => {
    const name = event.target.name;
    const value = event.target.value;
    setInputs(values => ({...values, [name]: value}))
  }

  const handleSubmit = async (event) => {
    event.preventDefault();
    console.log(inputs);
    let status = await login()
    if ( status == 'success' ) {
      window.location.href = baseUrl + 'dashboard'
    }
  }

  const login = async () => {
    try {
      const response = await axios.post(apiUrl + "login", {
        username: inputs.username,
        password: inputs.pwd
      })
      console.log(response)
      document.getElementById("loginMessage").innerHTML = response.data.message;
      return response.data.status
    }
    catch(e) {
      console.log(e.response)
      document.getElementById("loginMessage").innerHTML = e.response.data.message;
      return e.response.data.status
    }
  }

  return (
    <div className="Login">
      <header>
        <div class="topbar">
          <a href={ baseUrl }>Racket Tracker</a>
          <a id='loginbutton' href={ baseUrl + "login" }>Login</a>
        </div>
        <div class="topnav">
          <a href={ baseUrl + "dashboard" }>Dashboard</a>
          <a href={ baseUrl + "create-order" }>Create Order</a>
        </div> 
      </header>
      <p>
        No account yet? <a href={baseUrl + "register"}>Create an account</a>
      </p>
      <form onSubmit={handleSubmit}>
        <input 
          type="text" 
          placeholder="Username"
          name="username" 
          value={inputs.username || ""} 
          onChange={handleChange}
        />
        <br></br>
          <input 
            type="password"
            placeholder="Password"
            name="pwd"
            value={inputs.pwd || ""} 
            onChange={handleChange}
          />
          <br></br>
          <input type="submit" value="Login"/>
      </form>
      <p id="loginMessage"></p>
    </div>
  )
}

export default Login
