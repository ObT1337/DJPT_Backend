import React from 'react';
import './App.css';
import MainComponent from './components/MainComponent/MainComponent';
import logo from './logo.svg';
const App = () => {
  return (
    <div className="App" >
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" width="5%" />
        <MainComponent />
      </header>
    </div>
  );
}

export default App;