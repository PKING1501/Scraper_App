import React, {useEffect, useState} from 'react';
import './style.css';
import { Link, useNavigate } from 'react-router-dom';


const Navbar = () => {
  return (
    <nav className="navbar">
      <div className='connversehead'>
      <p id='Conn1'>Scrapper</p>
      </div>
      
      <ul className="nav-items">
        <li className="nav-item">
          <Link to="/" className="nav-link">
            <span>Home</span>
          </Link>
        </li>
        <li className="nav-item">
          <Link to="/scrape_attractions" className="nav-link">
            <span>Scrape Attractions</span>
          </Link>
        </li>
        <li className="nav-item">
          <Link to="/scrape_reviews" className="nav-link">
            <span>Scrape Reviews</span>
          </Link>
        </li>
      </ul>
    </nav>
  );
}

export default Navbar;
