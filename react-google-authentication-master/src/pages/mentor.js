import React from "react";
import Logout from "../components/Logout";
import MentorDashboard from "../components/MentorDashboard";
import { Link } from "react-router-dom";
import { Button, Dropdown } from "react-bootstrap";

function Mentor() {

  const handleOptionSelect = (option) => {
    console.log("Selected option:", option); 
  };

  return (
    <div>
      <MentorDashboard />
      <div style={{ position: "absolute", top: "80px", right: "40px" }}>
        <Dropdown>
          <Dropdown.Toggle variant="primary" id="dropdown-basic">
            Show scores
          </Dropdown.Toggle>

          <Dropdown.Menu>
            <Dropdown.Item as={Link} to="/studentScore">
              DAW
            </Dropdown.Item>
            <Dropdown.Item onClick={() => handleOptionSelect("ss")}>
              SS
            </Dropdown.Item>
            <Dropdown.Item onClick={() => handleOptionSelect("it")}>
              IT
            </Dropdown.Item>
          </Dropdown.Menu>
        </Dropdown>
      </div>
      <Logout />
    </div>
  );
}

export default Mentor;
