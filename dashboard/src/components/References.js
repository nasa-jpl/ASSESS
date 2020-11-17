import React from 'react';
import Standard from "./Standards"
import styled from  'styled-components';

const References = (props) => {
    // state.standards = 

    const refs = props.standards.map((standard) => 
        <li>
            <Standard 
                standard={standard}
                category="references"
            />
        </li>
    );
    return (
        <div style={{paddingTop:"30px"}}>
            { refs.length ?  <ul style={{marginTop: "15px", marginBottom: "25px", listStyle:"none"}}> {refs} </ul> 
            : <div style={{margin: "50px 0px", paddingLeft: "50px"}}>  
                <h2> No Embedded Standards </h2>
            </div> }
        </div>
    )
}

export default References