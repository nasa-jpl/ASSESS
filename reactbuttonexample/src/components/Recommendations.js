import React from 'react';
import Standard from "./Standards"
import styled from  'styled-components';


const Recommendations = (props) => {
    // state.standards = 
    const recs = props.standards.map((standard) => 
        <li>
            <Standard 
                standard={standard}
                category="recommendation"
            />
        </li>
    );
    
    return (
        <ul style={{marginTop: "15px"}}> {recs} </ul>
    )
    
}

export default Recommendations