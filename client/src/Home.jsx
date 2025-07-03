import { useState, useEffect } from 'react'
import axios from "axios";

function Home() {
  const [inputs, setInputs] = useState({});
  const baseUrl = "http://localhost:5173/"

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
      <header>
        <h2>Racket Tracker</h2>
        <p>Home</p>
      </header>
      <a href={baseUrl + "login"}>Login</a><br />
      <input type="button" onClick={() => createOrder()} value="Create order test"></input>
    </div>
  )
}

export default Home
