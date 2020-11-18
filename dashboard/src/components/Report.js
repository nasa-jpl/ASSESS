import React, { useState } from 'react';
import {Container, Row, Col, Button, Nav} from 'react-bootstrap';

import Embedded from "./Embedded";
import Recommendations from "./Recommendations";
import UploadBar from './UploadBar';
import Sidebar from './Sidebar';



const Report = (props) => {
    props.recs.forEach(function(d, i){
        d.toggle_id = i
    })

    const [displayRecs, setDisplayRecs] = useState(props.recs)

    const renderPdf = (file) => {
        props.renderPdf(file)
    }

    const updateDispRecs = (updatedRecs) => {
        setDisplayRecs(updatedRecs)
    }


    return (
        <Container expand="lg" style={{width: "100%", maxWidth: "100%", padding: "0px", height: "100%"}}>            
            <Row style={{ width: "100%", margin: 0, padding: "0px", height: "100vh" }}>
                <Col xs={2} style={{padding: "0px"}}>
                    <Sidebar page='report' navigateTo={props.navigateTo}/>
                </Col>
                <Col xs={10} style={{padding: "15px"}}>
                    <div style={{padding: "2vh 50px"}}>
                        <Row>
                            <h1 className="title"> Standards Report </h1>
                        </Row>
                        <Row style={{padding:"30px 0px"}}>
                            <Col xs={12} sm={12} md={12} lg={10} style={{}}>
                                
                                <p className="report-description"> Find referenced and recommended 
                                    standards, by upload, in their respective section below. If you do not find the stand you are 
                                    looking for, try searching the database.
                                </p>
                            </Col>
                            <Col xs={12} sm={12} md={12} lg={2}  style={{display: "flex", width:"100%", alignItems:"center"}}>
                                <div style={{width:"100%"}}>
                                    <Button 
                                        className="start-over-btn"
                                        onClick={()=> {props.navigateTo('uploader')}} 
                                        variant="outline-primary" 
                                    >
                                        Start Over
                                    </Button>
                                </div>
                                
                            </Col>
                        </Row>
                    </div>
                    {/* <Row>
                        Removing pdf preview because was deemed unnecessary for now. 
                        {props.pdfs ? <UploadBar pdfs={props.pdfs} renderPdf={renderPdf}/> : null } 
                    </Row> */}
                    <Embedded 
                        standards={props.refs} 
                    />
                    <Recommendations 
                        standards={props.recs}
                        displayRecs={displayRecs}
                        updateDispRecs={updateDispRecs}    
                    />
                </Col>
            </Row>
        </Container>
    )
}

export default Report;