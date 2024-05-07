import React, { useState } from 'react';
import './style.css';

const defaultHeaders = `{
  "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0",
  "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,/;q=0.8",
  "Accept-Language": "en-US,en;q=0.5",
  "Accept-Encoding": "gzip, deflate",
  "Connection": "keep-alive",
  "Upgrade-Insecure-Requests": "1",
  "Sec-Fetch-Dest": "document",
  "Sec-Fetch-Mode": "navigate",
  "Sec-Fetch-Site": "none",
  "Sec-Fetch-User": "?1",
  "Cache-Control": "max-age=0",
  "Referer": "http://www.google.com/"
}`;

const Reviews = () => {
  // State variables for input fields
  const [headers, setHeaders] = useState(defaultHeaders);
  const [starterLinks, setStarterLinks] = useState('');
  const [numAttractions, setNumAttractions] = useState('');
  const [progress, setProgress] = useState(80); // Adjusted progress value for demonstration

  // Handler functions to update state variables
  const handleHeadersChange = (e) => {
    setHeaders(e.target.value);
  };

  const handleStarterLinksChange = (e) => {
    setStarterLinks(e.target.value);
  };

  const handleNumAttractionsChange = (e) => {
    setNumAttractions(e.target.value);
  };

  const handleUpdateHeaders = () => {
    // Logic to update headers
    alert('Updating headers:', headers);
  };

  const handleScrapeAttractions = () => {
    // Logic to scrape attractions
    console.log('Scraping attractions...');
  };

  return (
    <div className='body'>
      <div className='input-section'>
        <label htmlFor='headers'>Headers:</label>
        <textarea 
          id='headers' 
          value={headers} 
          onChange={handleHeadersChange}
          placeholder='Enter headers...' // Placeholder text for the textarea
          rows='7' // Make textarea bigger by specifying the number of rows
        />
        <br />
        <br />
        <button onClick={handleUpdateHeaders}>Update Headers</button>
      </div>
      <div className='input-section'>
        <label htmlFor='starterLinks'>Starter Links:</label>
        <textarea 
          id='starterLinks' 
          value={starterLinks} 
          onChange={handleStarterLinksChange} 
          placeholder='Enter starter links...(To Enter multiple links , add each link in new line)' // Placeholder text for the textarea
          rows='4' // Make textarea bigger by specifying the number of rows
        />
      </div>
      <div className='input-section'>
        <label htmlFor='numAttractions'>Number of Reviews:</label>
        <input 
          type='number' 
          id='numAttractions' 
          value={numAttractions} 
          onChange={handleNumAttractionsChange} 
          placeholder='Enter number of reviews...(To scrape all available reviews enter 0' // Placeholder text for the input
        />
      </div>
      <div className='input-section' style={{ textAlign: 'right' }}>
        <button onClick={handleScrapeAttractions}>Scrape Attractions</button>
      </div>
      <div className='progress-section'>
        <label htmlFor='progress'>Progress:</label>
        <progress id='progress' value={progress} max='100'></progress>
      </div>
    </div>
  );
};

export default Reviews;
