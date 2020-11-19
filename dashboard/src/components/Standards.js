import React, {useState } from 'react';
import styled from  'styled-components';
import {CopyToClipboard} from "react-copy-to-clipboard";
import { useAlert } from 'react-alert'
import { FaCaretRight, FaFileDownload, FaExpandAlt, FaCaretDown, FaCopy } from 'react-icons/fa';
import { UncontrolledCollapse, CardBody, Card } from 'reactstrap';

import CustomButton from "./Custom/Button";

const Styles = styled.div`
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

    const onToggleClick = () => {
        setToggled(toggled => !toggled)
    }

    const onCopyClick = () => {
        alert.show("Copied to clipboard!")
    }
    return (
        <div style={{margin:"20px 35px"}}>
            <Styles>
                <CopyToClipboard text={JSON.stringify(props.standard)}
                    onCopy={() => setCopied(true)}
                >
                    <CustomButton 
                        onClick={onCopyClick}
                        icon={FaCopy}
                        style={{display: "inline-block", fontSize: "2rem", color: "#d5d6a9", margin:"10px"}}
                        className="btn-copy"
                    />
                </CopyToClipboard>
                <CustomButton 
                    icon={toggled ? FaCaretDown : FaCaretRight}
                    className="toggle"
                    id={toggleId}
                    onClick={onToggleClick}
                    style={{display: "inline-block", margin: "0px 5px", color: "#343e4c", fontSize: "1.5rem"}}
                />
                
                <p className="standard-title">{props.standard.title.split("(")[0]}</p>
                <p className="standard-id">{props.standard.id}</p>
                <p className="standard-type">{props.standard.type}</p>
                <p className="standard-specs">{props.standard.tc}</p>

                <CustomButton 
                    href={props.standard.url}
                    target="_blank"
                    className="download"
                    icon={FaFileDownload}
                    style={{display: "inline-block", fontSize: "1.2rem", color: "#ababab", marginLeft:"5px"}}
                />

                <CustomButton 
                    className="expand"
                    icon={FaExpandAlt}
                    style={{display: "inline-block", fontSize: "1.2rem", color: "#ababab", marginLeft:"5px"}}
                />

                <UncontrolledCollapse toggler={toggleSelection}>
                    <p className="standard-text">{props.standard.description}</p>
                </UncontrolledCollapse>
            </Styles>
        </div>
    )
}

export default Standards