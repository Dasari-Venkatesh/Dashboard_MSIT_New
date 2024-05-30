import React from "react";
import { Jumbotron, Row, Col, Navbar } from "react-bootstrap";
import Login from "./Login";
import LoginPrev from "./LoginPrev"


export default function LandingPage(props) {
  return (
    <div>
      <Jumbotron
        fluid
        style={{
          background: "#001340",
          color: "#CC3314",
          fontSize: "80px",
          height: "50rem",
          margin: 0,
        }}
      >
        <Col>
          <img
            src={process.env.PUBLIC_URL + "/msit_new_logo.png"}
            style={{
              height: "10rem",
              width: "auto",
              borderRadius: "8px",
            }}
          />
        </Col>
        <Col>Dashboard</Col>
        <Col></Col>
        {/* <Col>MSIT Dashboard</Col> */}
        <Col>
          <h5>Use your MSIT account to login.</h5>
          <a href="/">
            <Login
              updateLogin={props.updateLogin}
              updateEmail={props.updateEmail}
              updateMentorFlag={props.updateMentorFlag}
              updateStudentEmailList={props.updateStudentEmailList}
              updateData={props.updateData}
              updateScore={props.updateScore}
              updateSSScore={props.updateSSScore}
              updateDropoutFlag={props.updateDropoutFlag}
            />
          </a>
        </Col>
        <Col>
          <a href="/">
            <LoginPrev
              updateLogin={props.updateLogin}
              updateEmail={props.updateEmail}
              updateMentorFlag={props.updateMentorFlag}
              updateStudentEmailList={props.updateStudentEmailList}
              updateData={props.updateData}
              updateScore={props.updateScore}
              updateSSScore={props.updateSSScore}
              updateDropoutFlag={props.updateDropoutFlag}
            />
          </a>
        </Col>
      </Jumbotron>
    </div>
  );
}
