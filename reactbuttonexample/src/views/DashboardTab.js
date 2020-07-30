import React, { Component } from "react";
import Tabs from "react-bootstrap/Tabs";
import Tab from "react-bootstrap/Tab";
import Spinner from "react-bootstrap/Spinner";
import { withRouter } from "react-router";
import { connect } from "react-redux";
import { bindActionCreators } from "redux";
import fetchRecsAction from "./../redux/actions/fetchRecs";

import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Container from "react-bootstrap/Container";

import Uploader from "./../components/Uploader"
import Report from "./../Report/Report";

import {
    getRec,
    getRecLoading,
    getRecError,
} from "../redux/selectors";
import PdfViewer from "../PdfViewer/PdfViewer";

class DashboardTab extends Component {
    constructor(props){ 
        super(props);
        this.state = {
            activeKey: 'uploader',
            pdfs: {},
            text: null,
            previewPdf: null
        }

    }

    componentDidMount() {
        if ( !this.props.rec ) this.props.fetchRecs();
    }

    uploadFinished = (files) => {
        this.setState({pdfs: files})
        this.setState({activeKey:"report"})
    }

    renderPdf = (file) => {
        this.setState({previewPdf: file})
        this.setState({activeKey:"preview"})
    }

    navigateTo = (page) => {
        if (page == "uploader"){
            this.setState({ activeKey: page, pdfs: {}, text: null, previewFile: null})
        }
        else if (page == "report" || page == "preview" ) this.setState({ activeKey: page})
    }


    render() {
        if (this.state.activeKey == "uploader"){
            return (
                <Uploader
                    uploadFinished={this.uploadFinished} 
                />
            )
        } else if (this.state.activeKey == "report"){
            return (
                <div style={{ margin: "0px" }}>
                    <Report 
                        pdfs={this.state.pdfs}
                        text={this.state.text}
                        recs={this.props.rec}
                        renderPdf={this.renderPdf}
                        navigateTo={this.navigateTo}
                    />
                </div>
            )
        } else if (this.state.activeKey == "preview"){
            return (
                <div style={{ margin: "0px" }}>
                    <PdfViewer 
                        previewFile={this.state.previewPdf}
                        navigateTo={this.navigateTo}    
                    />
                </div>
            )
        }
    }

}

const mapStateToProps = (state) => ({
    rec: getRec(state),
    recLoading: getRecLoading(state),
    recError: getRecError(state),
});

const mapDispatchToProps = (dispatch) =>
    bindActionCreators(
    {
        fetchRecs: fetchRecsAction,
    },
    dispatch
);


export default withRouter(connect(mapStateToProps, mapDispatchToProps)(DashboardTab));