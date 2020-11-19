import React, { Component } from "react";
import { Button } from 'react-bootstrap';
import history from './../history';
import Sidebar from './../components/Bar';
import PdfViewer from "./../components/PdfViewer"

import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Container from "react-bootstrap/Container";


export default class Home extends Component {
  constructor(props){
    super(props);

    this.state = {
      previewFile: props.previewFile
    }
  }

  //uploadFinished(){
  render() {
    return (
      <Container expand="lg" style={{width: "100%", maxWidth: "100%", padding: "0px", height:"100%"}}>
        <Row style={{ width: "100%", margin: "0", padding: "0px", height: "100vh"}}>
          <Col xs={2} style={{ padding: "0px" }}>
            <Sidebar />
          </Col>
          <Col xs={10} style={{ padding: "0px" }}>
            <PdfViewer 
              previewFile={this.state.previewFile}
              navigateTo={this.props.navigateTo}  
            />
          </Col>
        </Row>
      </Container>
    )
  }
}