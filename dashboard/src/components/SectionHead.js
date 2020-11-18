import React from 'react';
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Container from "react-bootstrap/Container";
import { FaQuestionCircle } from 'react-icons/fa';
import styled from  'styled-components';

import LightTooltip from "./Custom/Tooltip";

const Button = styled.a`

    .search {
        margin-left: 8px;
        display: inline;
        font-size: 1.3em;
        color: #ababab;
    }
`;

const SectionHead = (props) => {
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
            </Row>
        </Container>
    )
}

export default SectionHead;