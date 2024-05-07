import React from 'react';
import Navbar from './components/Navbar/Navbar';
import Attractions from './components/Scrape_attractions/attractions';
import Reviews from './components/Scrape_reviews/Reviews';
import HomePage from './components/Home/home';

import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

const Home1 = () => {
  return (
    <>
      <Navbar />
      <HomePage />
    </>
  );
};

const Scrape_attractions1 = () => {
  return (
    <>
      <Navbar />
      <Attractions/>
      {/* Add other components or content for the Members page */}
    </>
  );
};

const Scrape_reviews1 = () => {
  return (
    <>
      <Navbar />
      <Reviews/>
      {/* Add other components or content for the Members page */}
    </>
  );
};

const App = () => {
  return (
    <Router>
      <Routes>
      <Route path="/" element={<Home1/>} />
        <Route path="/scrape_attractions" element={<Scrape_attractions1/>} />
        <Route path="/scrape_reviews" element={<Scrape_reviews1/>} />
      </Routes>
    </Router>
  );
};

export default App;
