import { useState, useEffect } from 'react'
import axios from "axios";

function Dashboard() {
  const baseUrl = "http://localhost:3000/"
  const apiUrl = "http://localhost:5000/api/"

  var dropdown = document.getElementsByClassName("dropdown-btn");
  var i;

  for (i = 0; i < dropdown.length; i++) {
    dropdown[i].addEventListener("click", function() {
      this.classList.toggle("active");
      var dropdownContent = this.nextElementSibling;
      if (dropdownContent.style.display === "block") {
        dropdownContent.style.display = "none";
      } else {
        dropdownContent.style.display = "block";
      }
    });
  } 

  return (
    <div className="Dashboard">
      <header>
        <div class="topbar">
          <a href={ baseUrl }>Racket Tracker</a>
          <a id='loginbutton' href={ baseUrl + "login" }>Login</a>
        </div>
      </header>
      <div class="topnav">
        <a href={ baseUrl + "dashboard" }>Dashboard</a>
        <a href={ baseUrl + "create-order" }>Create Order</a>
      </div> 
      <div class="sidenav">
        <a href="#about">About</a>
        <a href="#services">Services</a>
        <a href="#clients">Clients</a>
        <a href="#contact">Contact</a>
        <button class="dropdown-btn">Dropdown
          <i class="fa fa-caret-down"></i>
        </button>
        <div class="dropdown-container">
          <a href="#">Link 1</a>
          <a href="#">Link 2</a>
          <a href="#">Link 3</a>
        </div>
        <a href="#contact">Search</a>
      </div> 
      <div class='pagecontent'>
        <p>sduiofhoewi</p>
      </div>
      
    </div>
  )
}

export default Dashboard
