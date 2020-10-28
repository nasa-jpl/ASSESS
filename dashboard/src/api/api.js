import axios from "axios";

const endpoints = {
    recText: "recommend_text",
    recFile: "recommend_file",
    extract: "extract",
    standardInfo: "standard_info",
    search: "search"
}

const url = "https://assess-api.jpl.nasa.gov/";

let username = 'portal'
let password = 'a$$e$$!'

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

export const getRecFile = async (file) => {
    const formData = new FormData();
    formData.append('pdf', file)
    const response = await fetch(url + endpoints.recFile,
        {
            method: "POST",
            body: formData
        })
        const reader = response.body.getReader();
        console.log(reader);
        const utf8Decoder = new TextDecoder('utf-8')
        let {value: chunk, done: readerDone} = await reader.read();
        chunk = chunk ? utf8Decoder.decode(chunk) : "";
        console.log(chunk)
        return JSON.parse(chunk)
    
}

export const getStandardInfo = async () => {
    return fetch( url + endpoints.standardInfo,
    {
        method: "GET"
    })
    .then(response => console.log(response));
}

export const getSearch = async (input) => {
    const response = await fetch(url + endpoints.search,
        {
            method: "POST",
            body: JSON.stringify({placeholder: input})
        })
        const reader = response.body.getReader();
        console.log(reader);
        const utf8Decoder = new TextDecoder('utf-8')
        let {value: chunk, done: readerDone} = await reader.read();
        chunk = chunk ? utf8Decoder.decode(chunk) : "";
        console.log(chunk)
        return JSON.parse(chunk)
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


