import React from 'react';
import styled from  'styled-components';
import {Container, Row, Col} from 'react-bootstrap';
import { FaTrash } from 'react-icons/fa';

const Styled = styled.div`

`;

const Button = styled.a`

    .trash {
        display: inline;
        font-size: 1em;
        color: #ababab;
    }
`;

const PdfItem = (props) => {

    const onButtonClick = () => {
        props.removeFile(props.file)
    }

    return (
        <Styled>
            <Container style={{width: "100%", margin: "0px"}}>
                <Row style={{width: "100%", margin: "0px"}}>
                    <Col xs={10}>
                        <p className="pdf-name" > {props.file.name} </p>
                    </Col>
                    <Col xs={2} style={{textAlign: "end"}} className="button-div">
                        <Button onClick={onButtonClick}>
                            <p className="trash">< FaTrash /></p>
                        </Button>
                    </Col>
                </Row>
            </Container>
        </Styled>
    )
}

export default PdfItem