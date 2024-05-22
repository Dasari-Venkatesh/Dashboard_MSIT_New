// Logout.js
import React from "react";
import { GoogleLogout } from "react-google-login";
import { useHistory } from "react-router-dom";
const clientId =
  "707788443358-u05p46nssla3l8tmn58tpo9r5sommgks.apps.googleusercontent.com";
function Logout() {
  const history = useHistory();
  const onSuccess = () => {
    console.log("Logout made successfully");
    // Redirect to landing page after successful logout
    history.push("/");
  };
  return (
    <div>
      <GoogleLogout
        clientId={clientId}
        buttonText="Logout"
        onLogoutSuccess={onSuccess}
      />
    </div>
  );
}
export default Logout;