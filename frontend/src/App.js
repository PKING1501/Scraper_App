import React, { useState, useEffect } from 'react'
import Loader from './Loader'

const App = () => {
  const [data, setData] = useState([{}])
  const [attractionCount, setAttractionCount] = useState(0)
  const [cityName, setCityName] = useState('');
  const [loading, setLoading] = useState(false)
  const [isDataAcquired, setIsDataAcquired] = useState(false)
  const defaultHeaders = [
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
  ];
  const [headers, setHeaders] = useState(defaultHeaders);
  const [urls, setUrls] = useState('');

  const handleAddHeader = () => {
    setHeaders([...headers, { key: '', value: '' }]);
    console.log('Added header:', headers)
  };

  const handleDeleteHeader = (index) => {
    if (index < defaultHeaders.length) {
      alert('Cannot delete default header');
      return;
    }
    const updatedHeaders = [...headers];
    updatedHeaders.splice(index, 1);
    setHeaders(updatedHeaders);
  };

  const handleHeaderChange = (index, keyOrValue, value) => {
    const updatedHeaders = [...headers];
    updatedHeaders[index][keyOrValue] = value;
    setHeaders(updatedHeaders);
    console.log('Updated headers:', headers)
  };

  const runPythonCode = async (e) => {
    setLoading(true)
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
          attractionCount: attractionCount,
          urls: urls,
          // urls: urls.split(',').map(url => url.trim()), // Split URLs by comma and remove leading/trailing whitespaces
        }),
      })
      if (response.ok) {
        const responseData = await response.json()
        setData(responseData)
        console.log(data)
        setLoading(false)
        // Fetch city name
        const cityNameResponse = await fetch('/scraper1name', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            headers: headers,
            urls: urls
          }),
        });
        if (cityNameResponse.ok) {
          const cityNameData = await cityNameResponse.json();
          setCityName(cityNameData.city_name);
        } else {
          console.log('Failed to fetch city name');
        }
        setIsDataAcquired(true)
      } else {
        console.log('Failed to fetch')
        setLoading(false)
      }
    } catch (error) {
      console.log(error)
      setLoading(false)
    }
    setLoading(false)
  };

  const convertToCSV = () => {
    // Extract column names from the first object in the data array
    const columnNames = Object.keys(data[0]);

    // Concatenate column names with data rows
    const csvContent = `data:text/csv;charset=utf-8,${columnNames.join(',')}\n${
      data.map(row => columnNames.map(name => row[name]).join(',')).join('\n')
    }`;

    // Create a downloadable link
    const encodedURI = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedURI);
    link.setAttribute('download', `${cityName}_${attractionCount}_Attractions.csv`);
    document.body.appendChild(link);
    link.click();
  };

  // const convertToCSV = () => {
  //   const csvContent = "data:text/csv;charset=utf-8," + 
  //                      data.map(row => Object.values(row).join(',')).join('\n');
  //   const encodedURI = encodeURI(csvContent);
  //   const link = document.createElement('a');
  //   link.setAttribute('href', encodedURI);
  //   link.setAttribute('download', `${cityName}_${attractionCount}_Attractions.csv`);
  //   document.body.appendChild(link);
  //   link.click();
  // };

  useEffect(() => {
    if (isDataAcquired) {
      convertToCSV();
      setIsDataAcquired(false);
    }
  }, [isDataAcquired]);

  return (
    <>
      { loading? <Loader/> : (
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
              {index >= defaultHeaders.length && (
                <button type='button' onClick={() => handleDeleteHeader(index)}>Delete</button>
              )}
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
          <input
            type='number'
            placeholder='Number Of Attractions To Scrape'
            required
            value={attractionCount}
            onChange={(e) => setAttractionCount(e.target.value)}
          />
        </div>
        <input
          type='submit'
          value='Scrape Data'
          className='loginBtn'
        />
      </form>
      <div>
        
      {/* {isDataAcquired && <button onClick={convertToCSV}>Download CSV</button>} */}
      
      {isDataAcquired && (
        <>
          <h1>Displaying Data:</h1>
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
        </>
      )}
    </div>
    </div>
    )}
    </>
  )
}

export default App