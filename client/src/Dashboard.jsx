import { useState, useEffect } from 'react'
import axios from "axios";
import "./App.css"

function Dashboard() {
  const baseUrl = "http://localhost:3000/"
  const apiUrl = "http://localhost:5000/api/"
  const [open, setOpen] = useState(false);

  const handleOpen = () => {
    setOpen(!open);
  };

  const closeDropdown = () => {
    setOpen(false);
  }

  const handleDropdownLink = (id) => {
    console.log(id)
    closeDropdown()
    
  }


  //   for (i = 0; i < dropdown.length; i++) {
  //     dropdown[i].addEventListener("click", function() {
  //       this.classList.toggle("active");
  //       var dropdownContent = this.nextElementSibling;
  //       if (dropdownContent.style.display === "block") {
  //         dropdownContent.style.display = "none";
  //       } else {
  //         dropdownContent.style.display = "block";
  //       }
  //     });
  //   } 
  // }
  

  return (
    <div className="Dashboard">
      <header>
        <div className="topbar">
          <a href={ baseUrl }>Racket Tracker</a>
          <a id='loginbutton' href={ baseUrl + "login" }>Login</a>
        </div>
      </header>
      <div className="topnav">
        <a href={ baseUrl + "dashboard" }>Dashboard</a>
        <a href={ baseUrl + "create-order" }>Create Order</a>
      </div> 
      <button className="dropdown-btn" onClick={handleOpen}>Dropdown
          <i className="fa fa-caret-down"></i>
      </button>
      <div className="sidenav">
        <a href="#about">Temp</a>
        <div className='dropdown'>
          <button className="dropdown-btn" onClick={handleOpen}>Stringing
            <i className="fa fa-caret-down"></i>
          </button>
          { open ? (
            <ul className="dropdown-container">
              <li className='dropdown-item'>
                <button id='orders' onClick={() => handleDropdownLink('orders')}>Orders</button>
              </li>
              <li className='dropdown-item'>
                <button id='history' onClick={() => handleDropdownLink('history')}>History</button>
              </li>
            </ul>
          ) : null}
        </div>
      </div> 
      <div className='pagecontent'>
        {open ? <div>Is Open</div> : <div>Is Closed</div>}
      </div>
      
    </div>
  )
}

export default Dashboard
