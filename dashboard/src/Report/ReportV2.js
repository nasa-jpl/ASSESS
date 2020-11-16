import React, { useState } from 'react';

import styled from  'styled-components';

import References from "./../components/References";
import Recommendations from "./../components/Recommendations";
import RecTitle from "../components/ReportTitle";
import UploadBar from './../components/UploadBar';
import Sidebar from './../components/Bar';
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Container from "react-bootstrap/Container";
import { Dropdown } from "react-bootstrap"


import { FaSearch, FaQuestionCircle } from 'react-icons/fa';

const StyledHeader =  styled.div`
    background-color: #343d4c;
    height: 100px;

    h2 {
        color: #fff;
        font-size: 2.5em;
        padding-left: 20px;
        padding-top: 30px;
        display: inline-block
    }

    .dropdown-custom-1 {
        background-color: #343e4c;
        border-color: #343e4c;
        font-size: 2em;
        color: #fff;
    }

    .drop-menu {
        background-color: #343e4c;
        color: #fff;
    }

    .menu-item {
        color: #fff;
        font-size: 2em;
        margin: 10px 0px;
    }
`;

const Button = styled.a`

    .search {
        margin-left: 8px;
        display: inline;
        font-size: 1.3em;
        color: #ababab;
    }
`;


// const useStyles = makeStyles((theme) => ({
//     absolute: {
//         position: "absolute", 
//         bottom: theme.spacing(2),
//         right: theme.spacing(3)
//     }
// }))

const Report = (props) => {
    props.recs.forEach(function(d, i){
        d.toggle_id = i
    })
    const [recs, setRecs] = useState(props.recs)
    const [refs, setRefs] = useState(props.refs)
    const [searchValue, setSearchValue] = useState("Search the database")
    const [userSearched, setUserSearched] = useState(false)
    const [pdfs , setPdfs] = useState(props.pdfs)

    const renderPdf = (file) => {
        props.renderPdf(file)
    }

    const handleChange = (event) => {
        setSearchValue(event.target.value)
    }

    const handleSubmit = (event) => {
        alert("A Search was submitted! want to send to API instead " + this.state.searchValue )
        event.preventDefault();
    }

    const clearSearch = () => {
        setSearchValue("")
    }

    const searchSubmit = () => {
        //do api call here!
        console.log(searchValue)
        // pass props to child components
        
    }

    return (
        <Container expand="lg" style={{width: "100%", maxWidth: "100%", padding: "0px", height: "100%"}}>
            <Row style={{ width: "100%", margin: 0, padding: "0px", height: "100vh" }}>
                <Col xs={2} style={{padding: "0px"}}>
                    <Sidebar />
                </Col>
                <Col xs={10} style={{padding: "0px"}}>
                    <Row>
                        <RecTitle navigateTo={props.navigateTo}/>
                        {pdfs ? <UploadBar pdfs={pdfs} renderPdf={renderPdf}/> : null }
                    </Row>
                    <Row style={{background:"#343e4c", height:"5vh", minHeight:"85px", paddingTop:"20px"}}>

                        <Col xs={5} style={{paddingLeft:"40px"}}>
                            <h2 className="rec-title"> Referenced Standards </h2>
                            <Tooltip title="Embedded">
                                <Button aria-label="embedded">
                                    <FaQuestionCircle className="info-icon"/>
                                </Button>
                            </Tooltip>
                        </Col>
                    </Row>
                    <References standards={refs} />
                    <Row style={{background:"#343e4c", height:"5vh", minHeight:"85px", paddingTop:"20px"}}>
                        <Col xs={5} style={{paddingLeft:"40px"}}>
                            <h2 className="rec-title"> Recommended Standards </h2>
                        </Col>
                        <Col xs={2}>
                            <Dropdown >
                                <Dropdown.Toggle className="dropdown-custom-1">
                                    Category: All
                                </Dropdown.Toggle>

                                <Dropdown.Menu className="drop-menu">
                                    <Dropdown.Item className="menu-item" href="#/action-1">Item 1</Dropdown.Item>
                                    <Dropdown.Item className="menu-item" href="#/action-2">Item 2</Dropdown.Item>
                                    <Dropdown.Item className="menu-item" href="#/action-3">Item 3</Dropdown.Item>
                                </Dropdown.Menu>
                            </Dropdown>
                        </Col>
                        <Col xs={2}>
                            <Dropdown >
                                <Dropdown.Toggle className="dropdown-custom-1">
                                    Body: All
                                </Dropdown.Toggle>

                                <Dropdown.Menu className="drop-menu">
                                    <Dropdown.Item className="menu-item" href="#/action-1">Item 1</Dropdown.Item>
                                    <Dropdown.Item className="menu-item" href="#/action-2">Item 2</Dropdown.Item>
                                    <Dropdown.Item className="menu-item" href="#/action-3">Item 3</Dropdown.Item>
                                </Dropdown.Menu>
                            </Dropdown>
                        </Col>
                        <Col xs={3}>
                            <div>
                                <form style={{ height: "100%" }} onSubmit={handleSubmit} >
                                    <input 
                                        style={{display:"inline-block", height: "40px", width: "60%", color: "#ababab"}} 
                                        type="text" 
                                        value={searchValue} 
                                        onChange={handleChange}
                                        onClick={clearSearch}
                                        onSubmit={searchSubmit}
                                    />
                                    <Button >
                                        <p className="search"> <FaSearch /> </p>
                                    </Button>
                                </form>
                            </div>
                        </Col>
                    </Row>

                        
                        <div style={{display:"inline-block", marginLeft: "20%"}}>
   
                        </div>

                        <div style={{display:"inline-block", marginLeft: "5%"}}>
                            
                        </div>

                        
                    <Recommendations standards={recs} />
                </Col>
            </Row>
        </Container>
    )
}

export default Report;