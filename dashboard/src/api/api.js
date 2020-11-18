import axios from "axios";

const apiValues = {
    recText: {endpoint: "recommend_text", method: 'post'},
    recFile: {endpoint: "recommend_file", method: 'post'},
    extract: {endpoint: "extract", method: 'post'},
    standardInfo: {endpoint: "standard_info", method: 'get'},
    search: {endpoint: "search", method: 'get'},
    check: {endpoint: '', method: 'get'}
}

const baseUrl = "https://assess-api.jpl.nasa.gov/";

let username = 'portal'
let password = '***REMOVED***'

export const fetchData = async ( selection, data, size=10) => {
    var url = baseUrl + apiValues[selection].endpoint
    var uploadData;

    if (selection == 'search'){
        //If searching the database the url must look appropriate for an E.S. query
        if (!data) return null;
        let searchText;
        data.split(' ').forEach(function(d, i){
            if (!i) searchText = d
            else searchText += "%20" + d
        })
        url += "/" + searchText + "size=" + size;
        
    }

    if (selection == 'recText') uploadData = JSON.stringify({text_field: data})    
    else if (selection == 'recFile') {
        uploadData = new FormData();
        uploadData.append('pdf', data)
    } else if ( selection == 'standardInfo') uploadData = {}


    const options = {
        url: url,
        method: apiValues[selection].method,
        headers: {},
        data: uploadData
    }

    const response = await axios(options)
    if (response.status == 200) return response.data
    else return null;
}   




