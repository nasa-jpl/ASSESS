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
        <div style={{paddingTop: "30px"}}>
            <ul style={{marginTop: "15px"}}> {recs} </ul>
        </div>
        
    )
    
}

export default Recommendations