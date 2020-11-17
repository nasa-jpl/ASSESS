import React from 'react';
import './App.css';
import Navigation from './components/Navbar';
import Routes from './Routes';
import Dashboard from "./views/Dashboard"

import { transitions, positions, Provider as AlertProvider } from 'react-alert'
import AlertTemplate from 'react-alert-template-basic'
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";

import Layout from "./views/Layout";

const alertOptions = {
  // you can also just use 'bottom center'
  position: positions.MIDDLE,
  timeout: 1000,
  offset: '30px',
  // you can also just use 'scale'
  transition: transitions.SCALE
}

function App() {
  return (
    
    <AlertProvider template={AlertTemplate} {...alertOptions}>
      <div className="App" style={{height: "100vh"}}>
        <Router>
          <Layout>
            <Switch>
              <Dashboard />
            </Switch>
          </Layout>
        </Router>
      </div>
    </AlertProvider>
  );
}

export default App;
