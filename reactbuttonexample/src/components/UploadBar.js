import React from 'react';
import styled from  'styled-components';
import {Container, Row, Col, Button} from 'react-bootstrap';
import PdfReportItem from './PdfReportItem';

const Styled = styled.div`

    background-color: #d1d9e5;
`;

const UploadBar = (props) => {
    return (
        <div style={{width:"100%", paddingBottom: "10px", paddingTop: "10px", backgroundColor: "#d1d9e5"}}>
            
            <Container style={{padding:"0"}}>
                <h1 className="title"> Uploaded </h1>
            </Container>
            {props.pdfs.map((file)=>
            <li style={{listStyleType: "none"}}>
                <PdfReportItem file={file} renderPdf={props.renderPdf}/>
            </li>
            )}
        </div>
    )
    
}

export default UploadBar