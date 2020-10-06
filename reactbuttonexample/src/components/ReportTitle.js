import React from 'react';
import styled from  'styled-components';
import {Container, Row, Col, Button, Nav} from 'react-bootstrap';

const RecTitle = (props) => {    

    const onButtonClick = () => {
        props.navigateTo('uploader');
    }

    return (
        <div style={{height:"10vh", padding: "15px"}}>
            <h1 className="title" style={{fontSize:"2.5em", padding:"30px 30px 0px 0px"}}> Standards Report </h1>
            <p style={{padding: "10px 0px 0px 15px", display: "inline-block", fontSize:"1.8em"}}> Find referenced and recommended 
            standards, by upload, in their respective section below. If you do not find the stand you are 
            looking for, try searching the database.</p>

            <Button 
                style={{position:"absolute", right:"100px", fontSize:"2em"}}
                onClick={onButtonClick} 
                variant="outline-primary" 
            >
                Start Over
            </Button>
        </div>
    )
    
}

export default RecTitle