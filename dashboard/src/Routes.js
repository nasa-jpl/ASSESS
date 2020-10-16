import React, { Component } from "react";
import { Router, Switch, Route } from "react-router-dom";

import Report from "./Report/Report";
import Home from "./Home/Home";
import history from './history';
import PdfViewer from "./components/PdfViewer";

export default class Routes extends Component {
    constructor(props){
        super(props);

        this.state={
            file:[]
        }

        this.pdfUploaded = this.pdfUploaded.bind(this);
    }

    pdfUploaded(file){
        // console.log('pdf uploaded!', file)
        this.setState({ file:file })
    }


    render() {
        return (
            <Router history={history}>
                <Switch>
                    <Route path="/" exact render={() => <Home pdfUploaded={ this.pdfUploaded } /> } />
                    <Route path="/Report" component={Report} />
                    <Route path="/PdfViewer" render={() => <PdfViewer file={ this.state.file } />} />
                </Switch>
            </Router>
        )
    }
}
