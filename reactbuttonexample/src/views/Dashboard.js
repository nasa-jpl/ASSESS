import React from "react";
import { Route } from "react-router-dom";
import DashboardTab from "./DashboardTabV2";
import Container from "react-bootstrap/Container";

const Dashboard = ({ match }) => (
    <Route path="/" component={DashboardTab} />
);

export default Dashboard;