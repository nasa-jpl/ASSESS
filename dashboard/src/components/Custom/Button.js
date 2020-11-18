import React, { useState } from 'react';
import styled from  'styled-components';

const Button = styled.a``;

const CustomButton = (props) => {
    return (
        <div style={{display: props.style.display}}>
            <Button 
                onClick={props.onClick}
                aria-label={props.label}
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