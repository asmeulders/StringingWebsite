import { useState, useEffect } from 'react'
import axios from "axios";

function Register() {
  const [inputs, setInputs] = useState({});
  const baseUrl = "http://localhost:3000/"
  const apiUrl = "http://localhost:5000/api/"

  const handleChange = (event) => {
    const username = event.target.name;
    const pwd = event.target.value;
    setInputs(values => ({...values, [username]: pwd}))
  }

  const handleSubmit = async (event) => {
    event.preventDefault();
    console.log(inputs);
    await createUser()
    window.location.href = baseUrl + "login"
  }    

  const createUser = async () => {
    try {
      const response = await axios.put(apiUrl + "create-user", {
        username: inputs.username,
        password: inputs.pwd
      })
      console.log(response)
      document.getElementById("registerMessage").innerHTML = response.data.message;
    }
    catch(e) {
      document.getElementById("registerMessage").innerHTML = e.response.data.message;
    }
  }

  return (
    <div className="Register">
      <header>
        <h2>Racket Tracker</h2>
        <p>Register</p>
      </header>
      <p>
        Have an account? <a href={baseUrl + "login"}>Login</a>
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
          <input type="submit" value="Create Account"/>
      </form>
      <p id="registerMessage"></p>
    </div>
  )
}

export default Register
