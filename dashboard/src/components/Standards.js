import React, {useState } from 'react';
import styled from  'styled-components';
import {CopyToClipboard} from "react-copy-to-clipboard";
import { useAlert } from 'react-alert'


import { FaCaretRight, FaFileDownload, FaExpandAlt, FaCaretDown, FaCopy } from 'react-icons/fa';
import { UncontrolledCollapse, CardBody, Card } from 'reactstrap';

const Button = styled.a`
    display: inline;
    .icon {
        display: inline;
        font-size: 1.5rem;
    }

    .download {
        display: inline;
        font-size: 1.2rem;
        margin-right: 10px;
        color: #ababab;
    }

    .expand {
        display: inline;
        font-size: 1.2rem;
        color: #ababab;
    }

    .copy {
        display: inline;
        font-size 2rem;
        color: #d5d6a9;
    }


    .copy:hover, .icon:hover, .expand:hover{
        cursor: pointer;
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
        font-size: 1.7rem;
        font-weight: bold;
        display: inline;
        margin-right: 10px;
    }

    .standard-id {
        font-size: 1.3rem;
        font-weight: bold;
        display: inline;
        margin-right: 10px;
    }

    .standard-type {
        font-size: 1.3rem;
        font-weight: bold;
        display: inline;
        margin-right: 10px;
    }

    .standard-specs {
        font-size: 1.3rem;
        display: inline;
        margin-right: 10px;
    }
    .standard-text {
        font-size: 1.5rem;
        color: #262626;
        padding-left: 50px;
    }

`;


const Standards = (props) => {

    const toggleId = "toggle-" + props.category + "-" +  String(props.standard.toggle_id)
    const toggleSelection = "#" + toggleId
    const [toggled, setToggled] = useState(false)
    const [copied, setCopied] = useState(false);
    const alert = useAlert();

    const onButtonClick = () => {
        setToggled(toggled => !toggled)
    }

    const onCopyClick = () => {
        alert.show("Copied to clipboard!")
    }



    var title = props.standard.title.split("(")[0]
    return (
        <div style={{margin:"20px 35px"}}>
            <Styles>
                {/* <input type="checkbox" className="checkbox"></input>  */}
                <CopyToClipboard text={JSON.stringify(props.standard)}
                    onCopy={() => setCopied(true)}
                >
                    <Button target="_blank" onClick={onCopyClick}>
                        <p className="copy"> <FaCopy /> </p>
                    </Button>
                </CopyToClipboard>

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