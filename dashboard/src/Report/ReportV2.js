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
import { withStyles, makeStyles } from "@material-ui/core/styles";

import { FormControlLabel } from "@material-ui/core";

import DropdownCheckboxes from "./../components/DropdownCheckboxes";

import Tooltip from '@material-ui/core/Tooltip';
import { FaSearch, FaQuestionCircle } from 'react-icons/fa';
import { Checkbox } from '@material-ui/core';

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

const LightTooltip = withStyles((theme) => ({
    tooltip: {
      backgroundColor: "#fcf8c0",
      color: 'rgba(0, 0, 0, 0.87)',
      boxShadow: theme.shadows[1],
      fontSize: "1.2rem",
      marginTop: "20px"

    },
  }))(Tooltip);

const customDropdown = {
    dropdownButton: (provided, state) => ({
        ...provided,
        backgroundColor: "#000"
    })
}

const Report = (props) => {
    props.recs.forEach(function(d, i){
        d.toggle_id = i
    })

    const uniqueMain = []
    const uniqueCatogories = []
    
    props.recs.forEach(d=> {
        if (!uniqueMain.includes(d.type[0])){
            uniqueMain.push(d.type[0])
        }
    })
    props.recs.forEach(d=> {
        if (!uniqueCatogories.includes(d.tc)){
            uniqueCatogories.push(d.tc)
        }
    })

    const [recs, setRecs] = useState(props.recs)
    const [refs, setRefs] = useState(props.refs)
    const [categories, setCategories] = useState(uniqueCatogories)
    const [main, setMain] = useState(uniqueMain)
    const [filterValue, setFilterValue] = useState("Keyword filter")
    const [userFiltered, setUserFiltered] = useState(false)
    const [pdfs , setPdfs] = useState(props.pdfs)

    const renderPdf = (file) => {
        props.renderPdf(file)
    }

    const handleChange = (event) => {
        setFilterValue(event.target.value)
    }

    const handleSubmit = (event) => {
        alert("A Search was submitted! want to send to API instead " + this.state.searchValue )
        event.preventDefault();
    }

    const clearSearch = () => {
        setFilterValue("")
    }

    const filterSubmit = () => {
        //do api call here!
        console.log(filterValue)
        // pass props to child components
        
    }

    const dropdownChecked = (e) => {
        console.log(e)
    }

    const handleFilter = (filtered, sel) => {
        const tmp = props.recs.filter(function(d){
            if (filtered.includes((sel == "main" ? d.type[0] : d.tc))) return d
        })
        setRecs(tmp)
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
                    <Row style={{background:"#343e4c", minHeight:"85px", padding:"30px 0px"}}>=
                        <Col md={12} lg={6} style={{paddingLeft:"40px"}}>
                            <h2 className="rec-title"> Embedded Standards </h2>
                            <LightTooltip title="Embedded standards are standards that are directly found within the document or text that was uploaded"
                                className="clarify-tooltip"
                            >
                                <Button aria-label="embedded">
                                    <FaQuestionCircle className="info-icon"/>
                                </Button>
                            </LightTooltip>
                        </Col>
                    </Row>
                    <References standards={refs} />
                    <Row style={{background:"#343e4c", minHeight:"85px", paddingTop:"30px"}}>
                        <Col md={12} lg={12} xl={6} style={{paddingLeft:"40px"}}>
                            <h2 className="rec-title"> Recommended Standards </h2>
                            <LightTooltip title="Recommended standards are standards suggested using machine learning models "
                                className="clarify-tooltip"
                            >
                                <Button aria-label="recommended">
                                    <FaQuestionCircle className="info-icon"/>
                                </Button>
                            </LightTooltip>
                        </Col>
                    </Row>
                    <Row style={{background:"#343e4c", paddingBottom: "30px"}}>
                        <Col xs={12} sm={12} md={12} lg={12} xl={4}>
                            <div className="filters-box">
                                <h4 className="filters-title"> Filter: Category</h4>
                            </div>
                            <DropdownCheckboxes
                                className="dropdown-menu-box"
                                values={uniqueMain}
                                handleFilter={handleFilter}
                                dropdownType={'main'}
                            />
                        </Col>
                        <Col xs={12} sm={12} md={12} lg={12} xl={4}>
                            <div className="filters-box">
                                <h4 className="filters-title"> Filter: Body</h4>
                            </div>
                            <DropdownCheckboxes 
                                values={categories}
                                handleFilter={handleFilter}
                                dropdownType={'categories'}
                            />
                        </Col>
                        <Col xs={12} sm={12} md={12} lg={12} xl={4}>
                            <div className="filters-box">
                                <h4 className="filters-title"> Filter: Keyword</h4>
                            </div>
                            <div className="dropdown-menu-box">
                                <form style={{ height: "100%"}} onSubmit={handleSubmit} >
                                    <input 
                                        style={{display:"inline-block", height: "40px", width: "80%", color: "#ababab", marginLeft: "10%"}} 
                                        type="text" 
                                        value={filterValue} 
                                        onChange={handleChange}
                                        onClick={clearSearch}
                                        onSubmit={filterSubmit}
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