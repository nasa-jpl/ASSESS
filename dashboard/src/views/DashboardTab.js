import React, { useState } from "react";
import { withRouter } from "react-router";

import Uploader from "./../components/Uploader";
import Report from "../components/Report";
import Search from "../components/Search";

import { fetchData } from "../api/api";

const DashboardTab = (props) => {
  const [pdf, setPdf] = useState(undefined);
  const [activeKey, setActiveKey] = useState("uploader");
  const [text, setText] = useState("");
  const [recs, setRecs] = useState([]);
  const [refs, setRefs] = useState([]);

  const uploadPdf = async (files) => {
    //How am i supposed to handle errors? In this component do i catch a failed response code from the api and display
    // a warning message to the user?
    const resp = await fetchData("recFile", files[0]);
    setRecs(resp.recc);
    setRefs(resp.refs);
    setPdf(files);
    setActiveKey("report");
  };

  const uploadText = async (text) => {
    const resp = await fetchData("recText", text);
    setRecs(resp.recc);
    setRefs(resp.refs);
    setText(text);
    setActiveKey("report");
  };

  const navigateTo = (page) => {
    if (page == "uploader") {
      setActiveKey(page);
      setPdf(null);
      setText("");
    } else if (page == "report") {
      setActiveKey(page);
    } else if (page == "search") {
      setActiveKey(page);
    }
  };

  return (
    <div>
      {(function () {
        switch (activeKey) {
          case "uploader":
            return (
              <Uploader
                uploadPdf={uploadPdf}
                uploadText={uploadText}
                navigateTo={navigateTo}
              />
            );
          case "report":
            return (
              <Report
                pdfs={pdf}
                text={text}
                recs={recs}
                refs={refs}
                navigateTo={navigateTo}
              />
            );
          case "search":
            return <Search navigateTo={navigateTo} />;
          default:
            return null;
        }
      })()}
    </div>
  );
};

export default DashboardTab;
