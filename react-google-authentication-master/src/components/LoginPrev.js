import axios from "axios";
import React, { useState } from "react";

import { GoogleLogin } from "react-google-login";
// refresh token
import { refreshTokenSetup } from "../utils/refreshToken";

const clientId =
  "517972967421-7vd20rig40hriq0rlapi67al4q717n05.apps.googleusercontent.com";
function LoginPrev(props) {
  const onSuccess = (res) => {
    // alert(`Logged in successfully welcome ${res.profileObj.name}`);
    console.log("Login successful");

    axios
      .get(
        `https://7seqbvouv4.execute-api.ap-south-1.amazonaws.com/default/StudentZoomData_MentorDashboard/?mentor_email=${res.profileObj.email}&operation=mentor_check`
      )
      .then((response) => {
        props.updateMentorFlag(response.data.mentor);
        props.updateStudentEmailList(response.data.student_email_list);
      });

    let email = res.profileObj.email;
    if (props.mentor) email = props.studentEmail;

    axios
      .get(
        `https://7seqbvouv4.execute-api.ap-south-1.amazonaws.com/StudentZoom/StudentZoomData_CoursePerformance/?email=vedaravutla@msitprogram.net`
      )
      .then((response) => {
        if (response.data === "Student dropped out") {
          props.updateDropoutFlag(true);
        } else {
          props.updateData(response.data);
          props.updateScore(response.data.course_attendance.IT);
          props.updateSSScore(response.data.course_attendance.SS);
        }
      });

    props.updateLogin(true);
    props.updateEmail(res.profileObj.email);
    refreshTokenSetup(res);
  };

  const onFailure = (res) => {
    console.log("Login failed: res:", res);
    alert(`Failed to login.`);
  };

  return (
    <div>
      <GoogleLogin
        clientId={clientId}
        buttonText="LoginPrev"
        onSuccess={onSuccess}
        onFailure={onFailure}
        cookiePolicy={"single_host_origin"}
        style={{ marginTop: "0px" }}
        isSignedIn={true}
      />
      <br />
      <br />
    </div>
  );
}

export default LoginPrev;