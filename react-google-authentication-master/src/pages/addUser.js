import React, { useState, useRef } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import Admin from "../pages/admin"
import { FaArrowLeft } from "react-icons/fa";

function AddUser() {
  const countryCodeOptions = ["+91", "+1", "+44", "+61", "+86"];
  const [selectedAction, setSelectedAction] = useState("addSingleUser");
  const [file, setFile] = useState(null);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [idNumber, setIdNumber] = useState("");
  const [phoneNumber, setPhoneNumber] = useState("");
  const [role, setRole] = useState("");
  const [batch, setBatch] = useState("");
  const [errors, setErrors] = useState({});
  const fileInputRef = useRef(null);

  const handleFileChange = (event) => {
    const uploadedFile = event.target.files[0];
    setFile(uploadedFile);
  };

  const handleUpload = async () => {
    try {
      const formData = new FormData();
      formData.append("file", file);
      const response = await axios.post("http://127.0.0.1:5000/add-users/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      console.log("File uploaded successfully:", response.data);
      // Clear the file input
      setFile(null);
      if (fileInputRef.current) {
        fileInputRef.current.value = null;
      }
    } catch (error) {
      console.error("Error uploading file:", error.message);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const newErrors = {};

    if (!name) newErrors.name = "Name is required";
    if (!email) newErrors.email = "Email is required";
    if (!idNumber) newErrors.idNumber = "ID number is required";
    if (!phoneNumber) {
      newErrors.phoneNumber = "Phone number is required";
    } else if (phoneNumber.length !== 10) {
      newErrors.phoneNumber = "Phone number must be 10 digits long";
    }

    setErrors(newErrors);

    if (Object.keys(newErrors).length > 0) return;

    const userData = {
      name,
      email,
      idNumber,
      phoneNumber,
      role,
      batch,
    };

    try {
      const response = await fetch("http://127.0.0.1:5000/add-users/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(userData),
      });

      if (!response.ok) {
        throw new Error("Failed to add user");
      }

      console.log("User added successfully");
      // Reset form fields after successful submission
      setName("");
      setEmail("");
      setIdNumber("");
      setPhoneNumber("");
      setRole("");
      setBatch("");
    } catch (error) {
      console.error("Error:", error.message);
    }
  };

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        padding: "0.625rem 0.9375rem",
        margin: "auto",
        width: "100%",
        fontSize: "0.875rem",
        color: "#000000",
        backgroundColor: "#FFFFFF",
        maxWidth: "480px",
      }}
    >
      <Link to="/admin">  <div style={{position:"absolute",left:"20px"}}><FaArrowLeft style={{height:"28px",color:"black"}}/>
</div></Link>
    
      
      <nav
        style={{
          display: "flex",
          padding: "0.25rem 0",
          marginTop: "4rem",
          fontWeight: "bold",
          backgroundColor: "#E5E5E5",
          borderRadius: "0.75rem",
        }}
      >
        <div
          style={{
            justifyContent: "center",
            padding: "0.75rem 1.5rem",
            marginLeft: "1rem",
            cursor: "pointer",
            backgroundColor: selectedAction === "addSingleUser" ? "#FFFFFF" : "",
            borderRadius: "1rem",
          }}
          onClick={() => setSelectedAction("addSingleUser")}
        >
          Add Single User
        </div>
        <div
          style={{
            justifyContent: "center",
            padding: "0.75rem 1.5rem",
            marginLeft: "4rem",
            cursor: "pointer",
            backgroundColor: selectedAction === "uploadData" ? "#FFFFFF" : "",
            borderRadius: "1rem",
          }}
          onClick={() => setSelectedAction("uploadData")}
        >
          Upload Data
        </div>
      </nav>
      <main>
        {selectedAction === "addSingleUser" && (
          <form onSubmit={handleSubmit}>
            <div style={{ marginTop: "1.5rem" }}>Name*</div>
            <input
              style={{
                width: "380px",
                marginLeft: "0.375rem",
                padding: "0.75rem 1rem",
                borderRadius: "0.75rem",
                border: "1px solid #E5E5E5",
                color: "rgba(0, 0, 0, 0.5)",
              }}
              placeholder="Name"
              type="name"
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
            {errors.name && <div style={{ color: "red", marginLeft: "0.375rem" }}>{errors.name}</div>}
            
            <div style={{ marginTop: "1.5rem" }}>Email Address*</div>
            <input
              style={{
                width: "380px",
                marginLeft: "0.375rem",
                padding: "0.75rem 1rem",
                borderRadius: "0.75rem",
                border: "1px solid #E5E5E5",
                color: "rgba(0, 0, 0, 0.5)",
              }}
              placeholder="Your email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
            {errors.email && <div style={{ color: "red", marginLeft: "0.375rem" }}>{errors.email}</div>}
            
            <div style={{ marginTop: "1.5rem" }}>ID number*</div>
            <input
              style={{
                width: "380px",
                marginLeft: "0.375rem",
                padding: "0.75rem 1rem",
                borderRadius: "0.75rem",
                border: "1px solid #E5E5E5",
                color: "rgba(0, 0, 0, 0.5)",
              }}
              placeholder="ID number"
              type="text"
              value={idNumber}
              onChange={(e) => setIdNumber(e.target.value)}
            />
            {errors.idNumber && <div style={{ color: "red", marginLeft: "0.375rem" }}>{errors.idNumber}</div>}
            
            <div style={{ marginTop: "1.5rem" }}>Phone Number*</div>
            <div style={{ display: "flex" }}>
              <select
                style={{
                  width: "60px",
                  borderRadius: "0.75rem",
                  border: "1px solid #E5E5E5",
                  color: "rgba(0, 0, 0, 0.5)",
                  marginLeft:"2.3rem"
                }}
              >
                {countryCodeOptions.map((option, index) => (
                  <option key={index}>{option}</option>
                ))}
              </select>
              <input
                style={{
                  width: "320px", // Adjusted width to fit next to select
                  marginLeft: "0.5rem",
                  padding: "0.75rem 1rem",
                  borderRadius: "0.75rem",
                  border: "1px solid #E5E5E5",
                  color: "rgba(0, 0, 0, 0.5)",
                }}
                placeholder="Mobile number"
                type="text"
                value={phoneNumber}
                onChange={(e) => setPhoneNumber(e.target.value)}
              />
            </div>
            {errors.phoneNumber && <div style={{ color: "red", marginLeft: "0.375rem" }}>{errors.phoneNumber}</div>}
            
            <div style={{ marginTop: "1.5rem" }}>Role*</div>
            <select
              style={{
                width: "380px",
                marginLeft: "0.375rem",
                padding: "0.75rem 1rem",
                borderRadius: "0.75rem",
                border: "1px solid #E5E5E5",
                color: "rgba(0, 0, 0, 0.5)",
              }}
              value={role}
              onChange={(e) => setRole(e.target.value)}
            >
              <option value="" disabled>Select role</option>
              <option value="mentor">Mentor</option>
              <option value="student">Student</option>
              <option value="admin">Admin</option>
            </select>
            
            <div style={{ marginTop: "1.5rem" }}>Batch (Optional)</div>
            <input
              style={{
                width: "380px",
                marginLeft: "0.375rem",
                padding: " 0.75rem 1rem",
                borderRadius: "0.75rem",
                border: "1px solid #E5E5E5",
                color: "rgba(0, 0, 0, 0.5)",
              }}
              placeholder="Batch"
              type="text"
              value={batch}
              onChange={(e) => setBatch(e.target.value)}
            />
            
            <button
              type="submit"
              style={{
                alignSelf: "center",
                padding: "1rem 4rem",
                marginTop: "1.5rem",
                fontSize: "1rem",
                fontWeight: "bold",
                textAlign: "center",
                color: "#FFFFFF",
                backgroundColor: "#000000",
                borderRadius: "0.75rem",
              }}
            >
              Submit
            </button>
          </form>
        )}
        {selectedAction === "uploadData" && (
          <div style={{ marginTop: "1.5rem" }}>
            {/* File input for uploading data */}
            <input type="file" ref={fileInputRef} onChange={handleFileChange} style={{padding:"4rem 8rem"}} />
            {/* Button to trigger file upload */}
            <button
              type="button"
              onClick={handleUpload}
              style={{
                alignSelf: "center",
                padding: "1rem 4rem",
                fontSize: "1rem",
                fontWeight: "bold",
                textAlign: "center",
                color: "#FFFFFF",
                backgroundColor: "#000000",
                borderRadius: "0.75rem",
              }}
            >
              Upload
            </button>
            
          </div>
        )}
      </main>
    </div>
  );
}

export default AddUser;
