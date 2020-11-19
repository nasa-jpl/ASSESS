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

            <h1 className="title" style={{paddingLeft: "30px", fontSize:"2.5em"}}> Uploaded </h1>

            {props.pdfs.map((file)=>
            <li style={{listStyleType: "none"}}>
                <PdfReportItem file={file} renderPdf={props.renderPdf}/>
            </li>
            )}
        </div>
    )
    
}

export default UploadBar