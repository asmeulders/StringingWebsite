import { useState, useEffect } from 'react'
import axios from "axios";

function App() {
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
    const response = await axios.put(baseUrl + "create-user", {
      username: inputs.username,
      password: inputs.pwd
    })
    console.log(response)
  }

  const login = async () => {
    const response = await axios.post(baseUrl + "login", {
      username: "test",
      password: "test"
    })
  }
  const createOrder = async () => {
    const response = await axios.post(baseUrl + "create-order", {
      customer: "Alex",
      order_date: "2025-7-2",
      racket: "Wilson Pro Staff 97",
      mains_tension: 52,
      mains_string: "Luxilon ALU Power",
      crosses_tension: 50,
      crosses_string: null,
      replacement_grip: null,
      paid: false
    })
    console.log(response)
  }

  return (
    <div className="App">
      <form onSubmit={handleSubmit}>
        <label>Username:
        <input 
          type="text" 
          name="username" 
          value={inputs.username || ""} 
          onChange={handleChange}
        />
        </label>
        <br></br>
        <label>Password:
          <input 
            type="password"
            name="pwd"
            value={inputs.pwd || ""} 
            onChange={handleChange}
          />
          </label>
          <input type="submit" value="Submit"/>
      </form>
      <input type="button" onClick={() => login()} value="Login test"></input>
      <input type="button" onClick={() => createOrder()} value="Create order test"></input>
    </div>
  )
}

export default App
