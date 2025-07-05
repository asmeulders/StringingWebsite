import { useState, useEffect } from 'react'
import axios from "axios";

function Dashboard() {
  const [inputs, setInputs] = useState({});
  const baseUrl = "http://localhost:5173/"
  const apiUrl = "http://localhost:5000/api/"

  const today = () => {
    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
    var yyyy = today.getFullYear();

    today = yyyy + '-' + mm + '-' + dd;
    return today;
  }

  const handleChange = (event) => {
    const name = event.target.name;
    const value = event.target.value;
    setInputs(values => ({...values, [name]: value}))
  }

  const handleSubmit = async (event) => {
    event.preventDefault();
    console.log(inputs);
    await createOrder()
    for (let field in inputs) {
      inputs[field] = ''
    }
    handleChange(event) // refactor this?
  }

  const createOrder = async () => {
    var dateToday = today()

    let paid = document.getElementById("paidCheckbox").value == 'Paid'

    const response = await axios.post(apiUrl + "create-order", {
      customer: inputs.customer,
      order_date: dateToday,
      racket: inputs.racket,
      mains_tension: parseInt(inputs.mainsTension),
      mains_string: inputs.mainsString,
      crosses_tension: parseInt(inputs.mainsTension),
      crosses_string: inputs.mainsString,
      replacement_grip: inputs.replacementGrip,
      paid: paid
    })
    console.log(response)
  }

  return (
    <div className="Dashboard">
      <header>
        <h2>Racket Tracker</h2>
        <p>Dashboard</p>
      </header>
      <a href={apiUrl + 'logout'}>Logout</a><br/>
      <form id="orderForm" onSubmit={handleSubmit}>
        <input 
          id='customer'
          type="text" 
          placeholder="Customer"
          name="customer" 
          value={inputs.customer || ""} 
          onChange={handleChange}
        /><br/>
        <input 
          type="text"
          placeholder="Racket"
          name="racket"
          value={inputs.racket || ""} 
          onChange={handleChange}
        /><br/>
        <input 
          type="number"
          placeholder="Mains tension"
          name="mainsTension"
          value={inputs.mainsTension || ""}
          onChange={handleChange}
        /><br/>
        <input 
          type="text"
          placeholder="Mains string"
          name="mainsString"
          value={inputs.mainsString || ""}
          onChange={handleChange}
        /><br/>
        <input 
          type="text"
          placeholder="Replacement Grip"
          name="replacementGrip"
          value={inputs.replacementGrip || ""}
          onChange={handleChange}
        /><br/>
        <input 
          id='paidCheckbox'
          type="checkbox"
          name="paid"
          value='Paid'
          onChange={handleChange}
        />
        <label for="paid"> Paid</label><br/>
        <input type="submit" value="Create Order"/>
      </form>
      <p id="orderMessage"></p>
    </div>
  )
}

export default Dashboard
