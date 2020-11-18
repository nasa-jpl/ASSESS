import React, { useState } from 'react';
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Container from "react-bootstrap/Container";
import { FaSearch } from 'react-icons/fa';

import MultiDropdown from "./../components/MultiDropdown";
import CustomButton from "./Custom/Button";

const ResultsFilter = (props) => {
    
    const uniqueCategory = []
    const uniqueStdType = []
    
    props.recs.forEach(d=> {
        if (!uniqueCategory.includes(d.type[0])){
            uniqueCategory.push(d.type[0])
        }
    })

    props.recs.forEach(d=> {
        if (!uniqueStdType.includes(d.tc)){
            uniqueStdType.push(d.tc)
        }
    })
    
    const [filterValue, setFilterValue] = useState("Keyword filter")
    const [userFiltered, setUserFiltered] = useState(false)
    const [filteredRecs, setFilteredRecs] = useState(props.recs)

    const handleFilter = (filtered, sel) => {
        const tmp = props.recs.filter(function(d){
            if (filtered.includes((sel == "categories" ? d.type[0] : d.tc))) return d
        })
        props.updateDispRecs(tmp)
    }

    const handleChange = (event) => {
        setFilterValue(event.target.value)

    }

    const clearSearch = () => {
        setFilterValue("")
    }

    const filterSubmit = () => {
        //TODO: Impliment a fuzzball.js (fuzzywuzzy search) to filter by keyword
    }

    return (
        <Container expand="lg" style={{width: "100%", maxWidth: "100%", padding: "0px"}}>
            <Row style={{background:"#343e4c", paddingBottom: "30px"}}>
                <Col xs={12} sm={12} md={12} lg={12} xl={4}>
                    <div className="filters-box">
                        <h4 className="filters-title"> Filter: Category</h4>
                    </div>
                    <MultiDropdown
                        className="dropdown-menu-box"
                        values={uniqueCategory}
                        handleFilter={handleFilter}
                        dropdownType={'categories'}
                    />
                </Col>
                <Col xs={12} sm={12} md={12} lg={12} xl={4}>
                    <div className="filters-box">
                        <h4 className="filters-title"> Filter: Body</h4>
                    </div>
                    <MultiDropdown 
                        values={uniqueStdType}
                        handleFilter={handleFilter}
                        dropdownType={'stdType'}
                    />
                </Col>
                <Col xs={12} sm={12} md={12} lg={12} xl={4}>
                    <div className="filters-box">
                        <h4 className="filters-title"> Filter: Keyword</h4>
                    </div>
                    <div className="dropdown-menu-box">
                        <form style={{ height: "100%"}}>
                            <input 
                                style={{display:"inline-block", height: "40px", width: "80%", color: "#ababab", marginLeft: "10%", paddingLeft: "20px"}} 
                                type="text" 
                                value={filterValue} 
                                onChange={handleChange}
                                onClick={clearSearch}
                                onSubmit={filterSubmit}
                            />
                            <CustomButton 
                                icon={FaSearch}
                                style={{color: "#ababab", fontSize:"1.5rem", display: "inline-block", marginLeft: "10px"}} 
                                onClick={filterSubmit}                           
                            />

                        </form>
                    </div>
                </Col>
            </Row>
        </Container>
    )
}

export default ResultsFilter;