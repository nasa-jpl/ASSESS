import React, { Component } from "react";
import history from './../history';
import Uploader from './../components/Uploader';
import Sidebar from './../components/Sidebar';
import PdfViewer from "./../components/PdfViewer"
import "./Home.css";
import MyDocument from "./../components/Viewer";


import { Navbar, Nav, Form, Button } from 'react-bootstrap';

class Home extends Component {
  constructor(props){
    super(props);
    this.state = {
      file: []
    }
  }

  //uploadFinished(){

  uploadFinished = (file) => {
    this.setState({file: file})
    this.props.pdfUploaded(file)
  }

  render() {
    return (
      <div>
        <div>
          <Sidebar />
        </div>
        <div className="ui container">
          <Uploader
            uploadFinished={this.uploadFinished}
          />
          <div style={{height: "200px"}}>
            <Nav.Link href="/Report"> Submit for Standards </Nav.Link>
            <Nav.Link href="/PdfViewer"> Preview </Nav.Link>
          </div>
        </div>
      </div>
      
    );
  }
}

export default Home;