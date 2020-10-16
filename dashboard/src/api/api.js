import axios from "axios";

const endpoints = {
    recText: "recommend_text",
    recFile: "recommend_file",
    extract: "extract",
    standardInfo: "standard_info"
}

const url = "https://assess-api.jpl.nasa.gov/";

let username = 'portal'
let password = '***REMOVED***'

//Axios request

export const apiCheck = async () => {
    // axios.get(url,{}
    //     // {
    //     //     headers:{
    //     //         'Access-Control-Allow-Origin': '*'
    //     //     },
    //     //     // auth: {
    //     //     //     username: username,
    //     //     //     password: password
    //     //     // }
    //     // }
    // )
    // .then(response => console.log(response))
    // .then(json => console.log(json));
    return fetch(url, {
        method: "GET"
    })
    .then(res=> console.log(res))
}


export const getRecText = async (text) => {
    const response = await fetch(url + endpoints.recText,
    {
        method: "POST",
        body: JSON.stringify({ text_field: text})
    })
    const reader = response.body.getReader();
    const utf8Decoder = new TextDecoder('utf-8')
    let {value: chunk, done: readerDone} = await reader.read();
    chunk = chunk ? utf8Decoder.decode(chunk) : "";
    return JSON.parse(chunk)

}

export const getStandardInfo = async () => {
    return fetch( url + endpoints.standardInfo,
    {
        method: "GET"
    })
    .then(response => console.log(response));
}


// let headers = new Headers();
// headers.set('Authorization', 'Basic ' + btoa(username + ":" + password));
// headers.set('Access-Control-Allow-Origin', "*")


// Fetch request
// export const apiCheck = async () => {
//     const headers = {
//         // 'Authorization': 'Basic ' + btoa(username + ":" + password),
//         'Access-Control-Allow-Origin': "*"
//     }
    
//     return fetch(url, {
//         method: "POST",
//         headers: headers,
//         // mode: 'cors'
//     })
//     .then(response => response.json())
//     .then(json => console.log(json));
// }


