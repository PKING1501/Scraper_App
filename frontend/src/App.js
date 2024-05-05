import React, { useState } from 'react'

const App = () => {
  const [data, setData] = useState([{}])
  const [headers, setHeaders] = useState([
    {
      key: 'User-Agent',
      value: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0'
    },
    {
      key: 'Accept',
      value: 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,/;q=0.8'
    },
    {
      key: 'Accept-Language',
      value: 'en-US,en;q=0.5'
    },
    {
      key: 'Accept-Encoding',
      value: 'gzip, deflate'
    },
    {
      key: 'Connection',
      value: 'keep-alive'
    },
    {
      key: 'Upgrade-Insecure-Requests',
      value: '1'
    },
    {
      key: 'Sec-Fetch-Dest',
      value: 'document'
    },
    {
      key: 'Sec-Fetch-Mode',
      value: 'navigate'
    },
    {
      key: 'Sec-Fetch-Site',
      value: 'none'
    },
    {
      key: 'Sec-Fetch-User',
      value: '?1'
    },
    {
      key: 'Cache-Control',
      value: 'max-age=0'
    },
    {
      key: 'Referer',
      value: 'http://www.google.com/'
    }
  ]);

  const [urls, setUrls] = useState('')
  
  const convertToCSV = async (data) => {
    try {
      const response = await fetch('/scraper1name', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          headers: headers,
          urls: urls
        }),
      });
      if (response.ok) {
        const responseData = await response.json();
        const cityName = responseData.city_name;
        const csvContent = "data:text/csv;charset=utf-8," + 
                          data.map(row => Object.values(row).join(',')).join('\n');
        const encodedURI = encodeURI(csvContent);
        const link = document.createElement('a');
        link.setAttribute('href', encodedURI);
        link.setAttribute('download', `${cityName}_Attractions.csv`);
        document.body.appendChild(link);
        link.click();
      } else {
        console.log('Failed to fetch city name');
      }
    } catch (error) {
      console.log(error);
    }
  };


  const handleAddHeader = () => {
    setHeaders([...headers, { key: '', value: '' }]);
    console.log('Added header:', headers)
  };

  const handleHeaderChange = (index, keyOrValue, value) => {
    const updatedHeaders = [...headers];
    updatedHeaders[index][keyOrValue] = value;
    setHeaders(updatedHeaders);
    console.log('Updated headers:', headers)
  };

  const runPythonCode = async (e) => {
    console.log('Running Python code with initial data:', data)
    e.preventDefault()
    try {
      const response = await fetch('/firstScraper', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          headers: headers,
          urls: urls,
          // urls: urls.split(',').map(url => url.trim()), // Split URLs by comma and remove leading/trailing whitespaces
        }),
      })
      if (response.ok) {
        const responseData = await response.json()
        setData(responseData)
        console.log(data)
        convertToCSV(data)
      } else {
        console.log('Failed to fetch')
      }
      // fetch("/Scrapper1").then(
      //   res => res.json()
      // ).then(
      //   data => {
      //     setData(data)
      //     console.log(data)
      //   }
      // )
    } catch (error) {
      console.log(error)
    }
  };

  return (
    <div>
      <form className='loginForm' onSubmit={runPythonCode}>
        <div className='headers'>
          {headers.map((header, index) => (
            <div key={index}>
              <input
                type='text'
                placeholder='Header Key'
                value={header.key}
                onChange={(e) => handleHeaderChange(index, 'key', e.target.value)}
              />
              <input
                type='text'
                placeholder='Header Value'
                value={header.value}
                onChange={(e) => handleHeaderChange(index, 'value', e.target.value)}
              />
            </div>
          ))}
          <button type='button' onClick={handleAddHeader}>Add Header</button>
        </div>
        <div className='loginPassword'>
          <input
            type='text'
            placeholder='Urls (comma-separated)'
            required
            value={urls}
            onChange={(e) => setUrls(e.target.value)}
          />
        </div>
        <input
          type='submit'
          value='Login'
          className='loginBtn'
        />
      </form>
      <div>
      <h1>Displaying Data</h1>
      <ul>
        {data.map((item, index) => (
          <li key={index}>
            <h2>{item.name}</h2>
            <p>Address: {item.address}</p>
            <p>Rating: {item.rating}</p>
            {/* Add more fields as needed */}
          </li>
        ))}
      </ul>
    </div>
    </div>
  )
}

export default App