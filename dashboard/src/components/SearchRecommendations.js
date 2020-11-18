import React from 'react';
import Standard from "./Standards"

const SearchRecommendations = (props) => {
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
            <div style={{paddingTop: "30px"}}>
                <ul style={{marginTop: "15px", listStyle:"none"}}> {recs} </ul>
            </div>
        </div>
    )
}

export default SearchRecommendations;