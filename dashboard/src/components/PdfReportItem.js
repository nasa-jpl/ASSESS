import React from 'react';
import styled from  'styled-components';
import {Container, Row, Col,  Button} from 'react-bootstrap';


const Styled = styled.div`

`;

const PdfReportItem = (props) => {

    const onButtonClick = () => {
        props.renderPdf(props.file)
    }

    return (
        <div style={{padding: "5px 15px 5px 30px"}}>
            
            <p className="pdf-name" style={{padding: "10px 50px 0px 15px", display: "inline-block", fontSize:"1.5em"}}> {props.file.name} </p>
        
            <Button
                style={{position: "absolute", right: "100px", fontSize: "2em"}}
                onClick={onButtonClick} 
                variant="outline-primary" 
            >
                Preview
            </Button>

        </div>
    )
}

export default PdfReportItem