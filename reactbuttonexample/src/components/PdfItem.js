import React from 'react';
import styled from  'styled-components';
import {Container, Row, Col} from 'react-bootstrap';
import { FaTrash } from 'react-icons/fa';

const Styled = styled.div`
    .pdf-name {
        display: inline-block;
        font-size: 2em;
        padding-left: 50px;
    }
`;

const Button = styled.a`

    .trash {
        position: absolute;
        right: 70px;
        font-size: 2em;
        color: #ababab;
    }

    .trash:hover{
        color: #fff;
        cursor: pointer;
    }


`;

const PdfItem = (props) => {

    const onButtonClick = () => {
        props.removeFile(props.file)
    }

    return (
        <Styled>
            <p className="pdf-name" > {props.file.name} </p>
            <Button onClick={onButtonClick}>
                <p className="trash" style={{display: "inline-block"}}>< FaTrash /></p>
            </Button>
            {/* <Container style={{width: "100%", margin: "0px", fontSize: "2em"}}>
                <Row style={{width: "100%", margin: "0px"}}>
                    <Col xs={10}>

                    </Col>
                    <Col xs={2} style={{textAlign: "end"}} className="button-div">

                    </Col>
                </Row>
            </Container> */}
        </Styled>
    )
}

export default PdfItem