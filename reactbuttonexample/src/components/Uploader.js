import React from 'react';
import DropZone from './DropZone';
import '../styles/Uploader.css'

import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Container from "react-bootstrap/Container";
import Sidebar from "./../components/Bar";

import { Navbar, Nav, Form, Button } from 'react-bootstrap';

import PdfItem from "./PdfItem";

class Uploader extends React.Component {
    constructor(props){
        super(props);

        this.state = {files: []}
        this.pdfUploaded = this.pdfUploaded.bind(this)
        this.handleSubmit = this.handleSubmit.bind(this)
        this.onButtonClick = this.onButtonClick.bind(this)
        this.removeFile = this.removeFile.bind(this)
        this.fileInput = React.createRef();
    }

    componentWillMount(){

    }


    handleSubmit(event){
        event.preventDefault();
        this.state.files = this.fileInput.current.files
    }

    pdfUploaded(file){
        var f = this.state.files
        f.push(file)
        this.setState({files: f})
    }

    removeFile(file){
        this.setState({files: this.state.files.filter((f) =>  f.name != file.name ) })
    }

    onButtonClick = () => {
        if (this.state.files.length) this.props.uploadFinished(this.state.files)
    }

    render() {
        return (
            <Container expand="lg" style={{width: "100%", maxWidth: "100%", padding: "0px", height: "100%"}}>
                <Row style={{ width: "100%", margin: 0, padding: "0px", height: "100vh" }}>
                    <Col xs={2} style={{padding: "0px"}}>
                        <Sidebar />
                    </Col>
                    <Col xs={{span:8, offset:1}}>

                        <div style={{padding: "15px"}}>
                            <h1 className="upload-title"> Upload </h1>
                            <p className="upload-description"> Assess uses machine-learning to identify standards referenced in your work and
                                standards relevant to your work. Upload a document or paste a block of text in the window below.
                            </p>
                            
                        </div>

                        <div className="uploader-menu">
                            <button className="text-button"> Upload Documents</button>
                            <button className="text-button"> Upload Text</button>
                        </div>
                            <DropZone 
                                onPdfUploaded={this.pdfUploaded}
                                accept="application/pdf"
                            />
                            <div style={{width:"100%", paddingBottom: "4px", paddingTop: "4px", backgroundColor: "#d1d9e5"}}>
                                {this.state.files.length ? (this.state.files.map((file) => 
                                    <li style={{listStyleType: "none"}}>
                                        <PdfItem 
                                            file={file}
                                            removeFile={this.removeFile}
                                        />    
                                    </li>)) 
                                : null}    
                            </div>
                            <div style={{textAlign: "center", width:"100%", paddingBottom: "20px", paddingTop: "10px", backgroundColor: "#d1d9e5"}}>
                                <Button onClick={this.onButtonClick}>
                                    Get Standards
                                </Button>
                            </div>
     
                    </Col>
                </Row>
            </Container>
        )
    }
}

export default Uploader