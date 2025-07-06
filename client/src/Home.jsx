import { useState, useEffect } from 'react'
import axios from "axios";

function Home() {
  const baseUrl = "http://localhost:3000/"

  return (
    <div className="Home">
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
      <p>Welcome!</p>
    </div>
  )
}

export default Home
