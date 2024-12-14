import React, { useState, useEffect } from 'react';
import Loader from '../Loader/Loader';
import './style.css';
import io from 'socket.io-client';
const socket = io('http://localhost:5000');

const Attractions = () => {
  // State variables for input fields
  const [data1, setData1] = useState([{}])
  const [attractionCount1, setAttractionCount1] = useState(0)
  const [cityName, setCityName] = useState('');
  const [loading, setLoading] = useState(false)
  const [progress1, setProgress1] = useState(0)
  const [isDataAcquired1, setIsDataAcquired1] = useState(false)
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
  const [headers1, setHeaders1] = useState(defaultHeaders);
  const [urls, setUrls] = useState('');

  // useEffect(() => {
  //   const storedIsDataAcquired1 = localStorage.getItem('isDataAcquired1');
  //   if (storedIsDataAcquired1) {
  //     setIsDataAcquired1(JSON.parse(storedIsDataAcquired1));
  //   }
  // }, []);

  const handleAddHeader = () => {
    setHeaders1([...headers1, { key: '', value: '' }]);
    console.log('Added header:', headers1)
  };

  const handleDeleteHeader = (index) => {
    // if (index < defaultHeaders.length) {
    //   alert('Cannot delete default header');
    //   return;
    // }
    const updatedHeaders = [...headers1];
    updatedHeaders.splice(index, 1);
    setHeaders1(updatedHeaders);
  };

  const handleHeaderChange = (index, keyOrValue, value) => {
    const updatedHeaders = [...headers1];
    updatedHeaders[index][keyOrValue] = value;
    setHeaders1(updatedHeaders);
    console.log('Updated headers1:', headers1)
  };

  const runPythonCode1 = async (e) => {
    e.preventDefault();
    setLoading(true);
  
    const urlList = urls.split(',').map(url => url.trim());
  
    for (const url of urlList) {
      try {
        if (!isDataAcquired1) {
          const response = await fetch('http://127.0.0.1:5000/secondScraper', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              headers: headers1,
              attractionCount: attractionCount1,
              urls: url
            }),
          });
  
          if (response.ok) {
            const responseData1 = await response.text();
            console.log('Received data:', responseData1);
            setData1(responseData1);
  
            const cityNameResponse = await fetch('http://127.0.0.1:5000/scraper2name', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json'
              },
              body: JSON.stringify({
                headers: headers1,
                urls: url
              }),
            });
  
            if (cityNameResponse.ok) {
              const cityNameData = await cityNameResponse.json();
              setCityName(cityNameData.city_name);
              setIsDataAcquired1(true);
            } else {
              console.log('Failed to fetch city name');
            }
          } else {
            console.log('Failed to fetch data');
          }
        }
      } catch (error) {
        console.log(error);
      }
    }
    setLoading(false);
  };  

  // const runPythonCode1 = async (e) => {
  //   setLoading(true)
  //   console.log('Running Python code with initial data:', data)
  //   e.preventDefault()
  //   try {
  //     const response = await fetch('/firstScraper', {
  //       method: 'POST',
  //       headers: {
  //         'Content-Type': 'application/json'
  //       },
  //       body: JSON.stringify({
  //         headers: headers,
  //         attractionCount: attractionCount,
  //         urls: urls,
  //         // urls: urls.split(',').map(url => url.trim()), // Split URLs by comma and remove leading/trailing whitespaces
  //       }),
  //     })
  //     if (response.ok) {
  //       const responseData1 = await response.json()
  //       setData(responseData1)
  //       console.log(data)
  //       setLoading(false)
  //       // Fetch city name
  //       const cityNameResponse = await fetch('/scraper1name', {
  //         method: 'POST',
  //         headers: {
  //           'Content-Type': 'application/json'
  //         },
  //         body: JSON.stringify({
  //           headers: headers,
  //           urls: urls
  //         }),
  //       });
  //       if (cityNameResponse.ok) {
  //         const cityNameData = await cityNameResponse.json();
  //         setCityName(cityNameData.city_name);
  //       } else {
  //         console.log('Failed to fetch city name');
  //       }
  //       setIsDataAcquired1(true)
  //     } else {
  //       console.log('Failed to fetch')
  //       setLoading(false)
  //     }
  //   } catch (error) {
  //     console.log(error)
  //     setLoading(false)
  //   }
  //   setLoading(false)
  // };

  // const convertToCSV = () => {
  //   // Extract column names from the first object in the data array
  //   const columnNames = Object.keys(data[0]);

  //   // Concatenate column names with data rows
  //   const csvContent = `data:text/csv;charset=utf-8,${columnNames.join(',')}\n${
  //     data.map(row => columnNames.map(name => row[name]).join(',')).join('\n')
  //   }`;

  //   // Create a downloadable link
  //   const encodedURI = encodeURI(csvContent);
  //   const link = document.createElement('a');
  //   link.setAttribute('href', encodedURI);
  //   link.setAttribute('download', `${cityName}_${attractionCount}_Attractions.csv`);
  //   document.body.appendChild(link);
  //   link.click();
  // };

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
  
  // const convertToCSV = () => {
  //     // Extract column names from the first object in the data array
  //     const columnNames = Object.keys(data[0]);

  //     // Concatenate column names with data rows
  //     const csvContent = `data:text/csv;charset=utf-8,${columnNames.join(',')}\n${
  //       data.map(row => 
  //         columnNames.map(name => {
  //           // If the value contains a comma, enclose it within double quotes
  //           if (typeof row[name] === 'string' && row[name].includes(',')) {
  //             return `"${row[name]}"`;
  //           }
  //           return row[name];
  //         }).join(',')
  //       ).join('\n')
  //     }`;

  //     // Create a downloadable link
  //     const encodedURI = encodeURI(csvContent);
  //     const link = document.createElement('a');
  //     link.setAttribute('href', encodedURI);
  //     link.setAttribute('download', `${cityName}_${attractionCount}_Attractions.csv`);
  //     document.body.appendChild(link);
  //     link.click();
  // };

  const downloadCSV = () => {
      try {
          const csvData1 = data1
          // Create a Blob from CSV data
          const blob = new Blob([csvData1], { type: 'text/csv' });
          // Create a URL for the Blob
          const url = window.URL.createObjectURL(blob);
          // Create a link element and simulate click to initiate download
          const a = document.createElement('a');
          a.href = url;
          a.download = `${cityName}_Reviews.csv`;
          a.click();
          // Clean up by revoking the object URL
          window.URL.revokeObjectURL(url);
      } catch (error) {
          console.error('Error downloading CSV:', error);
      }
  };

  useEffect(() => {
    if (isDataAcquired1) {
      downloadCSV();
      setIsDataAcquired1(false);
    }
  }, [isDataAcquired1]);

  useEffect(() => {
      socket.on('progress', ({ percentage }) => {
          setProgress1(percentage);
      });
      return () => {
          socket.off('progress');
      };
  }, []);

  return (
    <>
    <h1 className="page-heading">TripAdvisor Reviews Scraper</h1>{loading ?
      <>
        <div className='progress-section'>
          <label htmlFor='progress'>Progress:</label>
          <progress style={{ color: '#7A5CFA' }} id='progress' value={progress1} max='100'></progress>
        </div>
        <Loader />
      </>
      : (
    <>
      <div className='body'>
        <div className='input-section1'>
          {headers1.map((header, index) => (
            <div key={index} className="header-input-container">
              <input
                className='header-key-input'
                type='text'
                placeholder='Header Key'
                value={header.key}
                onChange={(e) => handleHeaderChange(index, 'key', e.target.value)}
              />
              <input
                className='header-value-input'
                type='text'
                placeholder='Header Value'
                value={header.value}
                onChange={(e) => handleHeaderChange(index, 'value', e.target.value)}
              />
              {/* {index >= defaultHeaders.length && ( */}
                <button type='button' onClick={() => handleDeleteHeader(index)}>Delete</button>
              {/* )} */}
            </div>
          ))}
            <br/>
            <button type='button' onClick={handleAddHeader}>Add Header</button>
        </div>
        {/* <div className='input-section'>
          <label htmlFor='headers'>Headers:</label>
          <textarea 
            id='headers'
            value={headers} 
            // onChange={handleHeadersChange}
            placeholder='Enter headers...' // Placeholder text for the textarea
            rows='7' // Make textarea bigger by specifying the number of rows
          />
          <br />
          <br />
            <button
              // onClick={handleUpdateHeaders}
            >Add Header</button>
        </div> */}
          <br/>
        <div className='input-section'>
          <label htmlFor='starterLinks'>Starter Links:</label>
          <textarea 
            id='starterLinks' 
            value={urls} 
            onChange={(e) => setUrls(e.target.value)} 
            placeholder='Enter starter links...(Comma Seperated)' // Placeholder text for the textarea
            rows='4' // Make textarea bigger by specifying the number of rows
          />
        </div>
        <div className='input-section'>
          <label htmlFor='numAttractions'>Number of Reviews:</label>
          <input 
            type='number' 
            id='numAttractions' 
            value={attractionCount1} 
            onChange={(e) => setAttractionCount1(e.target.value)} 
            placeholder='Enter attractions count... (Will round up to the nearest multiple of 10 or maximum, Enter 0 for all attractions).'
          />
        </div>
        <div className='input-section' style={{ textAlign: 'right' }}>
          <button onClick={runPythonCode1}>Scrape Reviews</button>
        </div>
        {/* <div className='progress-section'>
          <label htmlFor='progress'>Progress:</label>
          <progress id='progress' value={progress} max='100'></progress>
        </div> */}
      </div>
    </>
  )}
  </>
  );
};

export default Attractions;
