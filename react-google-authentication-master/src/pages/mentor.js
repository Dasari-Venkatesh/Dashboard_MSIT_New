import React, { useState, useEffect } from "react";
import axios from "axios";
import { Dropdown, Button } from "react-bootstrap";
import { useHistory } from "react-router-dom";
import MentorDashboard from "../components/MentorDashboard";
import Logout from "../components/Logout";

function Mentor() {
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [selectedSubject, setSelectedSubject] = useState("");
  const [successMessage, setSuccessMessage] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [selectedFile, setSelectedFile] = useState(null);
  const history = useHistory();

  // Load uploadedFiles and selectedSubject from localStorage on component mount
  useEffect(() => {
    const storedUploadedFiles = localStorage.getItem("uploadedFiles");
    const storedSelectedSubject = localStorage.getItem("selectedSubject");

    if (storedUploadedFiles) {
      setUploadedFiles(JSON.parse(storedUploadedFiles));
    }
    if (storedSelectedSubject) {
      setSelectedSubject(storedSelectedSubject);
    }

    // Fetch uploaded sheet names
    fetchSheetNames();
  }, []);

  const fetchSheetNames = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:5000/sheet-names");
      setUploadedFiles(response.data);
    } catch (error) {
      console.error("Error fetching sheet names:", error);
    }
  };

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleFileUpload = async () => {
    if (!selectedFile) {
      setErrorMessage("Please select a file to upload.");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await axios.post("http://127.0.0.1:5000/upload-marksheet/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      setSuccessMessage(response.data.message);
      // Refresh uploaded sheet names
      fetchSheetNames();
    } catch (error) {
      setErrorMessage(error.response.data.error || "Error uploading file");
    }
  };

  const handleSubjectSelect = (subject) => {
    setSelectedSubject(subject);
    history.push(`/studentScore?subject=${subject}`);
    // Store selectedSubject in localStorage
    localStorage.setItem("selectedSubject", subject);
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
            {/* Render dropdown items based on uploaded files */}
            {uploadedFiles.map((fileName, index) => (
              <Dropdown.Item key={index}>
                <span onClick={() => handleSubjectSelect(fileName)}>{fileName}</span>
              </Dropdown.Item>
            ))}
          </Dropdown.Menu>
        </Dropdown>
      </div>
      <div style={{ display: "flex", flexDirection: "column", alignItems: "center",marginTop:"2rem" }}>
        <div style={{ border: "2px dotted #ccc", padding: "10px", marginBottom: "20px" ,borderRadius:"10px"}}>
        <h1 style={{fontSize:"24px",marginTop:"1rem",marginBottom:"1rem"}}>Upload student scores here</h1>
            <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
          <input type="file" onChange={handleFileChange} style={{ marginLeft: "8rem", marginTop: "1rem" }} />
          </div>
          <div>
          <Button variant="primary" onClick={handleFileUpload} style={{ marginTop: "2rem", marginBottom: "2rem" }}>
            Submit
          </Button>
          </div>
        </div>
        
        {successMessage && <div style={{ color: "green", marginTop: "1rem" }}>{successMessage}</div>}
        {errorMessage && <div style={{ color: "red", marginTop: "1rem" }}>{errorMessage}</div>}
      </div>

      <Logout />
    </div>
  );
}

export default Mentor;
