import React from "react";
import Container from "react-bootstrap/Container";
import { withRouter } from "react-router";

const Layout = (props) => {
  return (
    <Container style={{ width: "100%", maxWidth: "100%", padding: "0px", height:"100%" }}>
      {props.children}
    </Container>
  );
};

export default withRouter(Layout);