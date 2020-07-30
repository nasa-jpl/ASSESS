import React from 'react';
import styled from  'styled-components';
import {Container, Row, Col, Button, Nav} from 'react-bootstrap';

const RecTitle = (props) => {    

    const onButtonClick = () => {
        props.navigateTo('uploader');
    }

    return (
        <Container fliud style={{marginBottom:"20px"}}>
            <Row style={{width: "100%"}}>
                <h1 className="title"> Standards Report </h1>
                <Col xs={10}>
                    <p style={{padding: "10px 0px 0px 15px", display: "inline-block"}}> Find referenced and recommended 
                    standards, by upload, in their respective section below. If you do not find the stand you are 
                    looking for, try searching the database.</p>
                </Col>
                <Col xs={2}  style={{paddingTop: "10px"}} >
                   <Button 
                        onClick={onButtonClick} 
                        variant="outline-primary" 
                   >
                        Start Over
                   </Button>
                </Col>
            </Row>
        </Container>
    )
    
}

export default RecTitle