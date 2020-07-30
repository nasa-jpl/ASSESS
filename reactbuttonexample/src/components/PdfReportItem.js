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
            <Container fliud>
                <Row style={{width: "100%"}}>
                    <Col xs={10}>
                        <p className="pdf-name" style={{padding: "10px 0px 0px 15px", display: "inline-block"}}> {props.file.name} </p>
                    </Col>
                    <Col xs={2}  style={{paddingTop: "10px"}} >
                        <Button
                            onClick={onButtonClick} 
                            variant="outline-primary" 
                        >
                            Preview
                        </Button>
                    </Col>
                </Row>
            </Container>
        </div>
    )
}

export default PdfReportItem