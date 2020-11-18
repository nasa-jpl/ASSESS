import React from 'react';
import {Container, Row, Col, Button, Nav} from 'react-bootstrap';
import './../styles/Slidbar.css'

import styled from  'styled-components';

const Styled = styled.div`
    .nav-btn {
        width: 100%;
        font-size: 1.8rem;
        background-color: #343e4c;
        border: none;
        text-align: left;
        padding-left: 50px;
        margin: 5px 0px;
    }

    .nav-btn-active {
        width: calc(100% - 30px);
        font-size: 1.8rem;
        background-color: #4f5f75;
        border: none;
        text-align: left;
        padding-left: 35px;
        margin: 5px 0px;
    }

    .nav-btn:hover, .nav-btn-active:hover {
        background-color: #728aab;
        border: none;
    }

    .nav-btn:focus {
        background-color: #343e4c;
        border: none;
    }

    .rect-show {
        display: inline-block;
        width: 15px;
        background: #71c992;
    }
    .rect-hide {
        display: inline-block;
        width: 15px;
        background: #343e4c;
    }
`;


const Sidebar = (props) => {


    return (
        <Container style={{ width: "100%", height: "100%", backgroundColor: "#343d4c"}}>
            <Row>
                <Col>
                    <h1 className="sidebar-title" style={{paddingTop: "80px"}}> ASSESS </h1>
                </Col>
                
            </Row>

            {props.page != 'uploader' ? 
                <Styled>
                    <Row style={{marginTop: "5vh"}}>
                        <div className={props.page == 'report' ? 'rect-show' : 'rect-hide'}> </div>
                        <Button 
                            className={props.page == 'report' ? "nav-btn-active": 'nav-btn'} 
                            onClick={()=> props.navigateTo('report')}
                        >
                            Standards Report
                        </Button>
                    </Row>
                    <Row>
                        <div className={props.page == 'search' ? 'rect-show' : 'rect-hide'}> </div>
                        <Button 
                            className={props.page == 'search' ? "nav-btn-active": 'nav-btn'}
                            onClick={()=> props.navigateTo('search')}
                        >
                            Search the Database
                        </Button>
                    </Row>
                </Styled>
            : null}
        </Container>
    )

}

export default Sidebar