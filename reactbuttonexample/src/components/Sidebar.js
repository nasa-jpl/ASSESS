import React from 'react';
import './../styles/Slidbar.css'

class Sidebar extends React.Component {
    render() {
        return (
        <div className="ui wide sidebar inverted vertical menu visible pushable">
            <h1 className="sidebar-title" style={{marginTop: "80px"}}> ASSESS </h1>
            <h3 className="sidebar-section">Standards Report</h3>
            <a href="summary" className="item"> Summary </a>
            <a href="referenced" className="item"> Referenced Standards </a>
            <a href="recommended" className="item"> Recommended Standards </a>
            
            <a href="search" className="item"> Search the Database </a>
        </div>
        )
    }
}

export default Sidebar