import React from 'react';
import Standard from "./Standards"
import styled from  'styled-components';


const References = (props) => {
    // state.standards = 
    const recs = props.standards.map((standard) => 
        <li>
            <Standard 
                standard={standard}
                category="references"
            />
        </li>
    );
    
    return (
        <ul style={{marginTop: "15px", marginBottom: "25px"}}> {recs} </ul>
    )
}

export default References