import React, {useCallback} from 'react'
import {useDropzone} from 'react-dropzone'

import '../styles/Uploader.css'

import {Button } from 'react-bootstrap';


var file = null;

function DropZone(props) {
    const onDrop = useCallback(acceptedFiles => {
        // console.log(acceptedFiles)
        props.onPdfUploaded(acceptedFiles[0])
    }, [])


    const {getRootProps, getInputProps, isDragActive} = useDropzone({onDrop})

    return (
        <div className="uploader">
            <div className="" {...getRootProps()}>
                <div className="drop-area">
                    <input {...getInputProps()} />
                    {
                        <p className="center-text">Drag files here or <em className="em-blue"> Browse </em></p>
                    }
                </div>
            </div>

        </div>
        
    )
}

export default DropZone;