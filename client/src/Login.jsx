import { useState, useEffect } from 'react'
import axios from "axios";

function Login() {
  const [inputs, setInputs] = useState({});
  const baseUrl = "http://localhost:5000/api/"

  const handleChange = (event) => {
    const username = event.target.name;
    const pwd = event.target.value;
    setInputs(values => ({...values, [username]: pwd}))
  }

  const handleSubmit = async (event) => {
    event.preventDefault();
    console.log(inputs);
    login()
  }

  const login = async () => {
    try {
        const response = await axios.post(baseUrl + "login", {
            username: inputs.username,
            password: inputs.pwd
        })
        console.log(response)
        document.getElementById("loginMessage").innerHTML = response.data.message;
    }
    catch(e) {
        document.getElementById("loginMessage").innerHTML = e.response.data.message;
    }
        

  }

  const createUser = async () => {
    try {
        const response = await axios.put(baseUrl + "create-user", {
        username: inputs.username,
        password: inputs.pwd
        })
        console.log(response)
        document.getElementById("loginMessage").innerHTML = response.data.message;
    }
    catch(e) {
        document.getElementById("loginMessage").innerHTML = e.response.data.message;
    }
  }

  return (
    <div className="App">
      <header>
        <h2>Racket Tracker</h2>
        <p>Login</p>
      </header>
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
      <input type="button" onClick={() => createUser()} value="Create New User"></input>
      <p id="loginMessage"></p>
    </div>
  )
}

export default Login
