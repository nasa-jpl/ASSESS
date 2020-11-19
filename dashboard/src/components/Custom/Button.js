import React, { useState } from 'react';
import styled from  'styled-components';

const Button = styled.a``;

const CustomButton = (props) => {
    return (
        <div style={{display: props.style.display ? props.style.display : "inline-block"}}>
            <Button 
                onClick={props.onClick}
                aria-label={props.label}
                href={props.href}
                target={props.target}
                id={props.id}
            >
                {<props.icon 
                    className={props.className}
                    style={{...props.style, cursor: "pointer"}}

                />}
            </Button>
        </div>
    )

}

export default CustomButton;