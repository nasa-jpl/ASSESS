import React from 'react';
import styled from  'styled-components';
import {Container, Row, Col, Button, Nav} from 'react-bootstrap';

const RecTitle = (props) => {    

    const onButtonClick = () => {
        props.navigateTo('uploader');
    }

    return (
        <Container expand="lg" style={{width:"100%", maxWidth:"100%", padding:"2vh 50px"}}>
            <Row>
                <Col xs={10} style={{height:"150px"}}>
                    <h1 className="title"> Standards Report </h1>
                    <p className="report-description"> Find referenced and recommended 
                        standards, by upload, in their respective section below. If you do not find the stand you are 
                        looking for, try searching the database.
                    </p>
                </Col>
                <Col xs={2} style={{height:"150px", display: "flex", width:"100%", alignItems:"center"}}>
                    <div style={{width:"100%"}}>
                        <Button 
                            className="start-over-btn"
                            onClick={onButtonClick} 
                            variant="outline-primary" 
                        >
                            Start Over
                        </Button>
                    </div>
                    
                </Col>
            </Row>
        </Container>
        // <div style={{height:"10vh", padding: "15px"}}>
        //     <h1 className="title" style={{fontSize:"2.5em", padding:"30px 30px 0px 0px"}}> Standards Report </h1>
        //     <p style={{padding: "10px 0px 0px 15px", display: "inline-block", fontSize:"1.8em"}}> Find referenced and recommended 
        //     standards, by upload, in their respective section below. If you do not find the stand you are 
        //     looking for, try searching the database.</p>

        //     <Button 
        //         style={{position:"absolute", right:"100px", fontSize:"2em"}}
        //         onClick={onButtonClick} 
        //         variant="outline-primary" 
        //     >
        //         Start Over
        //     </Button>
        // </div>
    )
    
}

export default RecTitle