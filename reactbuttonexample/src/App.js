import React from 'react';
import './App.css';
import Navigation from './components/Navbar';
import Routes from './Routes';
import Dashboard from "./views/Dashboard"

import { BrowserRouter as Router, Route, Switch } from "react-router-dom";

import Layout from "./views/Layout";

function App() {
  return (
    <div className="App" style={{height: "100vh"}}>
      <Router>
        <Layout>
          <Switch>
            <Dashboard />
          </Switch>
        </Layout>
      </Router>
      
    </div>
  );
}

export default App;
