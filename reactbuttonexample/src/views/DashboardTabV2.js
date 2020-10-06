import React, { useState } from "react";
import Tabs from "react-bootstrap/Tabs";
import Tab from "react-bootstrap/Tab";
import Spinner from "react-bootstrap/Spinner";
import { withRouter } from "react-router";
import { connect } from "react-redux";
import { bindActionCreators } from "redux";

import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Container from "react-bootstrap/Container";

import Uploader from "./../components/UploaderV2"
import Report from "./../Report/ReportV2";

import DummyStandards from "./../Report/DummyStandards";

import PdfViewer from "../PdfViewer/PdfViewer";

import { apiCheck, getRecText, getStandardInfo } from "../api/api";

const DashboardTab = props => {
    const [pdf, setPdf] = useState(undefined)
    const [activeKey, setActiveKey] = useState('uploader')
    const [text, setText] = useState('')
    const [preview, setPreview] = useState(undefined)
    const [recs, setRecs] = useState([])
    const [refs, setRefs] = useState([])

    const uploadPdf = (files) => {
        // console.log('upload pdf!', files)
        // apiCheck();
        setPdf(files)
        setActiveKey('report')
    }

    const uploadText = async (text) => {
        const t = await getRecText(text);
        setRecs(t.recc)
        setRefs(t.refs)
        setText(text)
        setActiveKey('report')
    }

    const renderPdf = (file) => {
        setPreview(file)
        setActiveKey('preview')
    }

    const navigateTo = (page) => {
        if (page == "uploader"){
            setActiveKey(page)
            setPdf(null)
            setText('')
            setPreview(null)
        } else if (page == "report" || page == "preview"){
            setActiveKey(page);
        }
    }  

    return (
        <div>
            {(function() {
                switch (activeKey) {
                    case 'uploader':
                        return <Uploader uploadPdf={uploadPdf} uploadText={uploadText} />
                    case 'report':
                        return (
                            <Report 
                                pdfs={pdf}
                                text={text}
                                recs={recs}
                                refs={refs}
                                renderPdf={renderPdf}
                                navigateTo={navigateTo}
                            />
                        );
                    case 'preview':
                        return <PdfViewer previewFile={preview} navigateTo={navigateTo} />;
                    default:
                        return null;
                }
            })()}
        </div>
    );


}

export default DashboardTab;