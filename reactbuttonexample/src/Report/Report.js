import React from 'react';

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


import { FaSearch } from 'react-icons/fa';

const StyledHeader =  styled.div`
    background-color: #343d4c;
    height: 60px;

    h2 {
        color: #fff;
        padding-left: 20px;
        padding-top: 10px;
        display: inline-block
    }

    .dropdown-custom-1 {
        background-color: #343e4c;
        border-color: #343e4c;
        font-size: 1.2em;
        color: #fff;
    }

    .drop-menu {
        background-color: #343e4c;
        color: #fff;
    }

    .menu-item {
        color: #fff;
        font-size: 1.2em
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

class Report extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            standards: props.recs,
            pdfs: props.pdfs,
            searchValue: "Search Recommendations"
        }
        

        this.renderPdf = this.renderPdf.bind(this);
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.clearSearch = this.clearSearch.bind(this);
    }   

    componentWillMount(){
    }

    renderPdf(file){
        this.props.renderPdf(file)
    }

    handleChange(event) {
        this.setState({ searchValue: event.target.value })
    }

    handleSubmit(event) {
        alert("A Search was submitted! want to send to API instead " + this.state.searchValue )
        event.preventDefault();

    }

    clearSearch() {
        this.setState({ searchValue: ""})
    }

    render() {
        return (
            <Container expand="lg" style={{width: "100%", maxWidth: "100%", padding: "0px", height: "100%"}}>
                <Row style={{ width: "100%", margin: 0, padding: "0px", height: "100vh" }}>
                    <Col xs={2} style={{padding: "0px"}}>
                        <Sidebar />
                    </Col>
                    <Col xs={10} style={{padding: "0px"}}>
                        <RecTitle navigateTo={this.props.navigateTo}/>
                        <UploadBar pdfs={this.state.pdfs} renderPdf={this.renderPdf}/>
                        <StyledHeader>
                            <h2> Referenced Standards </h2>
                        </StyledHeader>

                        <References standards={this.state.standards} />


                        <StyledHeader>
                            <h2> Recommended Standards </h2>
                            <div style={{display:"inline-block", marginLeft: "20%"}}>
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
                            </div>

                            <div style={{display:"inline-block", marginLeft: "5%"}}>
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
                            </div>

                            <div style={{display:"inline-block", marginLeft: "10%", height: "55%"}}>
                                <form style={{ height: "100%" }} onSubmit={this.handleSubmit} >
                                    <input 
                                        style={{display:"inline-block", height: "100%", width: "200px", color: "#ababab"}} 
                                        type="text" 
                                        value={this.state.searchValue} 
                                        onChange={this.handleChange}
                                        onClick={this.clearSearch} 
                                    />
                                    <Button >
                                        <p className="search"> <FaSearch /> </p>
                                    </Button>
                                </form>
                            </div>
                        </StyledHeader>
                        <Recommendations standards={this.state.standards} />
                    </Col>
                </Row>
            </Container>


        )
    }
}

export default Report


{/* <div>
<div>
    <RecTitle />
</div>
<UploadBar />
<StyledHeader>
    <h2> Referenced Standards </h2>
</StyledHeader>

<References standards={this.state.standards} />


<StyledHeader>
    <h2> Recommended Standards </h2>
</StyledHeader>
<Recommendations standards={this.state.standards} />

</div> */}