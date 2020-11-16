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
            { refs.length ?  <ul style={{marginTop: "15px", marginBottom: "25px"}}> {refs} </ul> 
            : <div style={{height:"10vh", paddingLeft: "50px", paddingTop: "10vh"}}>  
                <h2> No Referenced Standards </h2>
            </div> }
        </div>
    )
}

export default References