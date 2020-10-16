import React, {useState } from 'react';
import styled from  'styled-components';

import { FaCaretRight, FaFileDownload, FaExpandAlt, FaCaretDown } from 'react-icons/fa';
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
        font-size: 2em;
        font-weight: bold;
        display: inline;
        margin-right: 10px;
    }

    .standard-id {
        font-size: 2em;
        font-weight: bold;
        display: inline;
        margin-right: 10px;
    }

    .standard-type {
        font-size: 2em;
        font-weight: bold;
        display: inline;
        margin-right: 10px;
    }

    .standard-specs {
        font-size: 2em;
        display: inline;
        margin-right: 10px;
    }
    .standard-text {
        font-size: 1.5em;
        color: #262626;
        padding-left: 50px;
    }

`;

const Standards = (props) => {

    const toggleId = "toggle-" + props.category + "-" +  String(props.standard.toggle_id)
    const toggleSelection = "#" + toggleId
    const [toggled, setToggled] = useState(false)

    const onButtonClick = () => {
        setToggled(toggled => !toggled)
    }

    var title = props.standard.title.split("(")[0]
    return (
        <div style={{margin:"5px 0px"}}>
            <Styles>
                <input type="checkbox" className="checkbox"></input> 

                <Button id={toggleId} style={{ marginBottom: '1rem' }} onClick={onButtonClick}>
                    <p className="icon">
                        {toggled ? <FaCaretDown /> : <FaCaretRight />}
                    </p> 
                </Button>
                
                <p className="standard-title">{title}</p>
                <p className="standard-id">{props.standard.id}</p>
                <p className="standard-type">{props.standard.type}</p>
                <p className="standard-specs">{props.standard.tc}</p>

                <Button href={props.standard.url} target="_blank">
                    <p className="download">< FaFileDownload /></p>
                </Button>
                <Button>
                    <p className="expand">< FaExpandAlt /></p>
                </Button>

                <UncontrolledCollapse toggler={toggleSelection}>
                    <p className="standard-text">{props.standard.description}</p>
                </UncontrolledCollapse>
            </Styles>
        </div>
        
    )
    
}

export default Standards