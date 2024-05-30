import axios from "axios";
import React, { useState, useEffect } from "react";
import { GoogleLogin } from "react-google-login";
import { withRouter } from "react-router-dom";

const clientId = "517972967421-7vd20rig40hriq0rlapi67al4q717n05.apps.googleusercontent.com";

function Login(props) {
  const [redirected, setRedirected] = useState(false);

  const fetchUserRole = async (email) => {
    try {
      const response = await axios.get(`http://127.0.0.1:5000/get-role/${email}`);
      const role = response.data.role;
      return role;
    } catch (error) {
      console.error("Failed to fetch user role:", error);
      throw error;
    }
  };

  const onSuccess = async (res) => {
    const userEmail = res.profileObj.email;
    try {
      const role = await fetchUserRole(userEmail);
      localStorage.setItem("userEmail", userEmail);
      localStorage.setItem("userRole", role);
      setRedirected(true); // Set redirected to true to trigger redirection
    } catch (error) {
      alert(`Failed to fetch user role.`);
    }
  };

  const onFailure = (res) => {
    console.log("Login failed: res:", res);
    alert(`Failed to login.`);
  };

  useEffect(() => {
    if (redirected) {
      redirectToRolePage();
    }
  }, [redirected]);

  const redirectToRolePage = () => {
    const userRole = localStorage.getItem("userRole");
    switch (userRole) {
      case "admin":
        props.history.push("/admin");
        break;
      case "mentor":
        props.history.push("/mentor");
        break;
      case "student":
        props.history.push("/student")
      default:
        alert("User role not found or not specified.");
        break;
    }
  };

  return (
    <div>
      {redirected ? null : (
        <GoogleLogin
          clientId={clientId}
          buttonText="Login"
          onSuccess={onSuccess}
          onFailure={onFailure}
          cookiePolicy={"single_host_origin"}
          style={{ marginTop: "0px" }}
          isSignedIn={true}
        />
      )}
      <br />
      <br />
    </div>
  );
}

export default withRouter(Login);
