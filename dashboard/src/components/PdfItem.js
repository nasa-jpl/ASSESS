import React from 'react';
import styled from  'styled-components';
import {Container, Row, Col} from 'react-bootstrap';
import { FaTrash } from 'react-icons/fa';
import CustomButton from "./Custom/Button";



// const Styled = styled.div`
//     .pdf-name {
//         display: inline-block;
//         font-size: 2em;
//         padding-left: 50px;
//     }
// `;

// const Button = styled.a`

//     .trash {
//         position: absolute;
//         right: 70px;
//         font-size: 2em;
//         color: #ababab;
//     }

//     .trash:hover{
//         color: #fff;
//         cursor: pointer;
//     }


// `;

const PdfItem = (props) => {

    const onButtonClick = () => {
        props.removeFile(props.file)
    }

    return (
        <Container expand="lg" style={{width: "100%", marginBottom:"10px"}}>
            <Row style={{width: "100%"}}>
                <Col xs={11}>
                    <p className="pdf-name" style={{fontSize:"2em"}}> {props.file.name} </p>
                </Col>
                <Col xs={1} >
                    <CustomButton 
                        icon={FaTrash}
                        style={{fontSize:"2em", color:"#ababab", display:"inline-block"}}
                        onClick={onButtonClick}
                    />
                </Col>
            </Row>
        </Container>
    )
}

export default PdfItem