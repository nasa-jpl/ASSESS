import React, { useState } from 'react';
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Container from "react-bootstrap/Container";
import { Button } from 'react-bootstrap';
import Loader from "react-loader-spinner";

import "react-loader-spinner/dist/loader/css/react-spinner-loader.css"

import Sidebar from "./../components/Sidebar";
import PdfItem from "./PdfItem";
import DropZone from './DropZone';
import '../styles/Uploader.css'


const Uploader = props => {
    const defaultText = 'Copy and Paste text here!'
    const [files, setFiles] = useState([])
    const [uploadedFiles, setUploadedFiles] = useState(false)
    const [mode, setMode] = useState('text')
    const [text, setText] = useState(defaultText)
    const [loading, setLoading] = useState(false);

    const pdfUploaded = newFile => {
        var f = files;
        f.push(newFile)
        setFiles(f)
        setUploadedFiles(true)
    }

    const removeFile = file => {
        var tmp = files.filter((f) => f.name != file.name)
        setFiles(tmp)
        if (!tmp.length) setUploadedFiles(false)

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
                    <Row>
                        <div style={{padding: "15px", marginTop: "10vh"}}>
                            <h1 className="upload-title"> Upload </h1>
                            <p className="upload-description"> Assess uses machine-learning to identify standards referenced in your work and
                                standards relevant to your work. Upload a document or paste a block of text in the window below.
                            </p>
                        </div>
                    </Row>
                    <Row className="uploader-menu">
                        <Col md={12} lg={6}>
                            <button className={mode=="pdf" ? "text-button-selected" : "text-button"} onClick={() => setUploadMode('pdf')}> Upload Documents</button>
                        </Col>
                        <Col md={12} lg={6}>
                            <button className={mode=="text" ? "text-button-selected" : "text-button"}  onClick={() => setUploadMode('text')}> Upload Text</button>
                        </Col>
                           
                            
                    </Row>
                    
                    {mode == "pdf" ? 
                        <DropZone  onPdfUploaded={pdfUploaded} accept="application/pdf" />
                    : 
                        <div style={{padding:"15px", backgroundColor: "#d1d9e5"}}>
                            <textarea 
                                style={{height:"40vh", width: "100%", fontSize:"2rem", padding: "35px 20px", color: "#ababab", backgroundColor: "#fafafa"}}
                                type='text' 
                                value={text} 
                                onChange={handleTextChange}
                                onClick={()=> {if (text == defaultText) setText('')}}
                            />
                        </div>
                    }

                    <div style={{width:"100%", paddingBottom: "4px", paddingTop: "4px", backgroundColor: "#d1d9e5"}}>
                        {/* TODO: Why can I not just use  files.length as my conditional? also multiple files are not showing up in this list, even when files is changed */}
                        {uploadedFiles ? (files.map((file) => 
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
                        />
                        : null}
                    </div>
                </Col>
            </Row>
        </Container>
    )
}

export default Uploader;