import React from 'react';
import Standard from "./Standards"
import SectionHead from './SectionHead';
import ResultsFilter from "./ResultsFilter";

const Recommendations = (props) => {
    const recs = props.displayRecs.map((standard) => 
        <li>
            <Standard 
                standard={standard}
                category="recommendation"
            />
        </li>
    );
    
    return (
        <div>
            <SectionHead
                title="Recommended Standards"
                tooltipText="Recommended standards are standards suggested using machine learning models"
            />
            <ResultsFilter 
                recs={props.standards}
                updateDispRecs={props.updateDispRecs}
            />

            <div style={{paddingTop: "30px"}}>
                <ul style={{marginTop: "15px", listStyle:"none"}}> {recs} </ul>
            </div>
        </div>
    )
}

export default Recommendations;