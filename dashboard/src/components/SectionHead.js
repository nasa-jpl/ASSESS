import React, {useState} from 'react';
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Container from "react-bootstrap/Container";
import { FaQuestionCircle, FaSearch } from 'react-icons/fa';
import styled from  'styled-components';

import LightTooltip from "./Custom/Tooltip";
import CustomButton from "./Custom/Button";

const Button = styled.a`

    .search {
        margin-left: 8px;
        display: inline;
        font-size: 1.3em;
        color: #ababab;
    }
`;

const SectionHead = (props) => {

    const [searchValue, setSearchValue] = useState("Keyword filter")

    const handleFilter = (filtered, sel) => {
        const tmp = props.recs.filter(function(d){
            if (filtered.includes((sel == "categories" ? d.type[0] : d.tc))) return d
        })
        props.updateDispRecs(tmp)
    }

    const handleChange = (event) => {
        setSearchValue(event.target.value)

    }

    const clearSearch = () => {
        setSearchValue("")
    }

    const searchSubmit = () => {
        props.handleSearch(searchValue);
        
    }

    return (
        <Container expand="lg" style={{width: "100%", maxWidth: "100%", padding: "0px"}}>
            <Row style={{background:"#343e4c", minHeight:"85px", padding:"30px 0px"}}>
                <Col md={12} lg={6} style={{paddingLeft:"40px"}}>
                    <h2 className="rec-title"> {props.title} </h2>
                    <LightTooltip title={props.tooltipText}
                        className="clarify-tooltip"
                    >
                        <Button >
                            <FaQuestionCircle className="info-icon"/>
                        </Button>
                    </LightTooltip>
                </Col>
                {props.title=="Database Search" ?
                    <Col md={12} lg={6} style={{paddingLeft:"40px"}}>
                        <div className="dropdown-menu-box">
                            <form style={{ height: "100%"}}>
                                <input 
                                    style={{display:"inline-block", height: "40px", width: "80%", color: "#ababab", marginLeft: "10%", paddingLeft: "20px"}} 
                                    type="text" 
                                    value={searchValue} 
                                    onChange={handleChange}
                                    onClick={clearSearch}
                                />
                                <CustomButton 
                                    icon={FaSearch}
                                    style={{color: "#ababab", fontSize:"1.5rem", display: "inline-block", marginLeft: "10px"}} 
                                    onClick={searchSubmit}                           
                                />
                            </form>
                        </div>
                    </Col>
                : null}
            </Row>
        </Container>
    )
}

export default SectionHead;