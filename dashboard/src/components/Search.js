import React, { useState } from 'react';
import {Container, Row, Col, Button, Nav} from 'react-bootstrap';

import Sidebar from './Sidebar';
import SectionHead from './SectionHead';
import SearchRecommendations from "./SearchRecommendations";

import {fetchData} from "./../api/api";

const Search = (props) => {
    const [searchRecs, setSearchRecs] = useState([])

    const handleSearch = async (searchVal) => {
        const resp = await fetchData('search', searchVal, 10);
        const keys = Object.keys(resp)
        let tmp = [];
        keys.forEach(d=>{
            tmp.push(resp[d])
        })
        setSearchRecs(tmp)
    }

    return (
        <Container expand="lg" style={{width: "100%", maxWidth: "100%", padding: "0px", height: "100%"}}>            
            <Row style={{ width: "100%", margin: 0, padding: "0px", height: "100vh" }}>
                <Col xs={2} style={{padding: "0px"}}>
                    <Sidebar page='search' navigateTo={props.navigateTo}/>
                </Col>
                <Col xs={10} style={{padding: "15px"}}>
                    <div style={{padding: "2vh 50px"}}>
                        <Row>
                            <h1 className="title"> Database Search </h1>
                        </Row>
                        <Row style={{padding:"30px 0px"}}>
                            <Col xs={12} sm={12} md={12} lg={10} style={{}}>
                                
                                <p className="report-description"> Search the database of standards
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

                    <SectionHead 
                        title="Database Search"
                        tooltipText="Search the database tooltip"
                        handleSearch={handleSearch}
                    />

                    {searchRecs.length ? 
                        <SearchRecommendations
                            displayRecs={searchRecs}
                            standards={searchRecs}
                        />
                    : null}

                </Col>
            </Row>
        </Container>
    )
}

export default Search;