import React, { Component } from 'react';
import { Document, Page } from 'react-pdf';
import { pdfjs } from 'react-pdf';
import samplePdf from "./../pdf-test.pdf"
import { FaChevronRight, FaChevronLeft } from 'react-icons/fa';
import styled from  'styled-components';
import { Button } from "react-bootstrap";

import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Container from "react-bootstrap/Container";



pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.js`;




const IconButton = styled.a`
    .left {
        display: inline-block;
        font-size: 1em;
        color: #ababab;       
    }
    .right {
        display: inline-block;
        font-size: 1em;
        color: #ababab;
    }
`;

class PdfViewer extends Component {
    constructor(props){
        super(props);
        this.state = {
            file: props.previewFile,
            numPages: null,
            pageNumber: 1
        }

        // this.state.file = "https://s3-ap-southeast-1.amazonaws.com/happay-local/HVP/BILL20198261213473719445688HP.pdf"
    }

    onDocumentLoadSuccess = ({ numPages }) => {
        this.setState({ numPages })
    }

    incriment = () => {
        if (this.state.pageNumber < this.state.numPages){
            this.setState({ pageNumber: this.state.pageNumber + 1 })
        }
    }

    decriment = () => {
        if (this.state.pageNumber > 1){
            this.setState({ pageNumber: this.state.pageNumber - 1 })
        }
    }

    onButtonClick = () => {
        this.props.navigateTo('report')
    }

    render(){
        const { pageNumber, numPages } = this.state;
        return (
            <div>
                <div style={{height:"10vh"}}>
                    <Container fliud>
                        <Row style={{width: "100%"}}>
                            <Col xs={10}>
                                <h2 style={{ paddingLeft: "20px", paddingTop: "10px"}}> Preview </h2>
                            </Col>
                            <Col xs={2}  style={{paddingTop: "10px"}} >
                                <Button variant="outline-primary" onClick={this.onButtonClick}>
                                    Back to Standards
                                </Button>
                            </Col>
                        </Row>
                    </Container>
                    
                    
                </div>
                <div style={{ padding: "20px 40px 20px 40px", backgroundColor: "#525659"}}>
                    <div style={{ paddingLeft: "25%"}}>
                        <Document
                            file={this.state.file}
                            style={{ width: "85%"}}
                            onLoadSuccess={this.onDocumentLoadSuccess}
                        >
                            <Page pageNumber={pageNumber} />
                        </Document>
                        <div style={{marginTop: "10px"}}>
                            <IconButton onClick={this.decriment}>
                                <p className="left">< FaChevronLeft /></p>
                            </IconButton>
                            <p style={{display:"inline-block", margin: "0 10px 0 10px", color:"#fff"}}>Page {pageNumber} of {numPages}</p>
                            <IconButton onClick={this.incriment}>
                                <p className="right">< FaChevronRight /></p>
                            </IconButton>
                        </div>
                    </div>
                </div>
                
            </div>
        )
    }
}

export default PdfViewer;