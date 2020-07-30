import React, {useState } from 'react';
import styled from  'styled-components';

import { FaCaretRight, FaFileDownload, FaExpandAlt } from 'react-icons/fa';
import { UncontrolledCollapse, CardBody, Card } from 'reactstrap';

const Button = styled.a`
    display: inline;
    .icon {
        display: inline;
        font-size: 1.5em;
    }

    .download {
        display: inline;
        font-size: 1.2em;
        margin-right: 10px;
        color: #ababab;
    }

    .expand {
        display: inline;
        font-size: 1.2em;
        color: #ababab;
    }

`;

const Container = styled.div`
    display: inline;
`;

const Styles = styled.div`
    .checkbox{
        margin-right: 10px;
    }

    .standard-title {
        font-size: 1.5em;
        font-weight: bold;
        display: inline;
        margin-right: 10px;
    }

    .standard-id {
        font-size: 1.5em;
        font-weight: bold;
        display: inline;
        margin-right: 10px;
    }

    .standard-type {
        font-size: 1.5em;
        font-weight: bold;
        display: inline;
        margin-right: 10px;
    }

    .standard-specs {
        font-size: 1.5em;
        display: inline;
        margin-right: 10px;
    }

`;

const Standards = (props) => {
    const toggleId = "toggle-" + props.category + "-" +  String(props.standard.id)
    const toggleSelection = "#" + toggleId

    return (
        <div>
            <Styles>
                <input type="checkbox" className="checkbox"></input> 

                <Button id={toggleId} style={{ marginBottom: '1rem' }}>
                    <p className="icon">< FaCaretRight /></p> 
                </Button>
                
                <p className="standard-title">{props.standard.title}</p>
                <p className="standard-id">{props.standard.id}</p>
                <p className="standard-type">{props.standard.type}</p>
                <p className="standard-specs">{props.standard.specs}</p>

                <Button>
                    <p className="download">< FaFileDownload /></p>
                </Button>
                <Button>
                    <p className="expand">< FaExpandAlt /></p>
                </Button>

                <UncontrolledCollapse toggler={toggleSelection}>
                    <p className="standard-text">{props.standard.text}</p>
                </UncontrolledCollapse>
            </Styles>
        </div>
        
    )
    
}

export default Standards