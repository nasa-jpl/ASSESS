import React, { useState } from 'react';
import DropZone from './DropZone';
import '../styles/Uploader.css'

import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Container from "react-bootstrap/Container";
import Sidebar from "./../components/Bar";

import { Navbar, Nav, Form, Button } from 'react-bootstrap';

import PdfItem from "./PdfItem";

import Loader from "react-loader-spinner";
import "react-loader-spinner/dist/loader/css/react-spinner-loader.css"


const Uploader = props => {
    const defaultText = 'Copy and Paste text here!'
    const [files, setFiles] = useState([])
    const [flag, setFlag] = useState(false)
    const [mode, setMode] = useState('text')
    const [text, setText] = useState(defaultText)
    const [loading, setLoading] = useState(false);

    const pdfUploaded = file => {
        var f = files;
        f.push(file)
        setFiles(f)
        setFlag(true)
    }

    const removeFile = file => {
        var tmp = files.filter((f) => f.name != file.name)
        setFiles(tmp)
        if (!tmp.length) setFlag(false)

    }

    const onButtonClick = () => {
        if (mode == 'pdf' && files.length) {
            props.uploadPdf(files)
            setLoading(true)
        }
        else if (mode == 'text' && text != '' && text != defaultText) {
            props.uploadText(text)
            setLoading(true)
        }
    }   

    const setUploadMode = (m) => {
        setMode(m)
        if (m == "text") setFiles([])
    }

    const handleTextChange = event => {
        setText(event.target.value)
    }

    return (
        <Container expand="lg" style={{width: "100%", maxWidth: "100%", padding: "0px", height: "100%"}}>
            <Row style={{ width: "100%", margin: 0, padding: "0px", height: "100vh" }}>
                <Col xs={2} style={{padding: "0px"}}>
                    <Sidebar />
                </Col>
                <Col xs={{span:8, offset:1}}>
                    <div style={{padding: "15px", marginTop: "10vh"}}>
                        <h1 className="upload-title"> Upload </h1>
                        <p className="upload-description"> Assess uses machine-learning to identify standards referenced in your work and
                            standards relevant to your work. Upload a document or paste a block of text in the window below.
                        </p>
                        
                    </div>

                    <div className="uploader-menu">
                        <button className="text-button" onClick={() => setUploadMode('pdf')}> Upload Documents</button>
                        <button className="text-button" onClick={() => setUploadMode('text')}> Upload Text</button>
                    </div>
                    {mode == "pdf" ? 
                        <DropZone  onPdfUploaded={pdfUploaded} accept="application/pdf" />
                    : 
                        <div style={{padding:"15px", backgroundColor: "#d1d9e5"}}>
                            <textarea 
                                style={{height:"45vh", width: "100%", fontSize:"2em", padding: "35px 20px", color: "#ababab", backgroundColor: "#fafafa"}}
                                type='text' 
                                value={text} 
                                onChange={handleTextChange}
                                onClick={()=> {if (text == defaultText) setText('')}}
                            />
                        </div>
                    }

                    <div style={{width:"100%", paddingBottom: "4px", paddingTop: "4px", backgroundColor: "#d1d9e5"}}>
                        {flag ? (files.map((file) => 
                            <li style={{listStyleType: "none"}}>
                                <PdfItem  file={file} removeFile={removeFile} />    
                            </li>)) 
                        : null}    
                    </div>
                    <div style={{textAlign: "center", width:"100%", paddingBottom: "20px", paddingTop: "10px", backgroundColor: "#d1d9e5"}}>
                        <Button onClick={onButtonClick} className="standards-btn" style={{display:"inline-block"}}>
                            Get Standards
                        </Button>
                        { loading ? 
                        <Loader 
                            style={{display: "inline-block", marginLeft: "30px"}}
                            type="Oval"
                            color="#00BFFF"
                            height={70}
                            width={70}
                            // timeout={10000}
                        />
                        : null}
                    </div>
                    
                    
                </Col>
            </Row>
        </Container>
    )
}

export default Uploader;