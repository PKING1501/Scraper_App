import React from 'react';
import './HomePage.css'; // Import your CSS file for styling

const HomePage = () => {
  return (
    <div className='home-page' style={{ backgroundColor: '#E4DEFE', color: '#333' }}>
      <div className='welcome-message'>
        <h1 className='welcome-heading'>Welcome to our Web Scraping App</h1>
        <p className='welcome-text'>We help you scrape data from TripAdvisor.com</p>
      </div>
    </div>
  );
};

export default HomePage;
