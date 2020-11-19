import React from 'react';
import Standard from "./Standards"

import SectionHead from './SectionHead';

const Embedded = (props) => {
    const refs = props.standards.map((standard) => 
        <li>
            <Standard 
                standard={standard}
                category="references"
            />
        </li>
    );
    return (
        <div>
            <SectionHead 
                title="Embedded Standards"
                tooltipText="Embedded standards are standards that are directly found within the document or text that was uploaded"
            />
            <div style={{paddingTop:"30px"}}>
                { refs.length ?  <ul style={{marginTop: "15px", marginBottom: "25px", listStyle:"none"}}> {refs} </ul> 
                : <div style={{margin: "50px 0px", paddingLeft: "50px"}}>  
                    <h2> No Embedded Standards </h2>
                </div> }
            </div>
        </div>
    )
}

export default Embedded;