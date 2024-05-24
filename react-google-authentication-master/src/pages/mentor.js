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
            <Dropdown.Item >
              SS
            </Dropdown.Item>
            <Dropdown.Item >
              IT
            </Dropdown.Item>
          </Dropdown.Menu>
        </Dropdown>
      </div>
      <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
  <input type="file" style={{ marginLeft:"8rem",marginTop:"2rem"}}  />
  <button
    type="button"
    style={{
      padding: "0.5rem",
      fontSize: "1rem",
      fontWeight: "bold",
      textAlign: "center",
      color: "#FFFFFF",
      backgroundColor: "blue",
      borderRadius: "0.75rem",
        
      margin:"2rem"
    }}
  >
    Upload Marks
  </button>
</div>

     
      <Logout />
    </div>
  );
}

export default Mentor;
