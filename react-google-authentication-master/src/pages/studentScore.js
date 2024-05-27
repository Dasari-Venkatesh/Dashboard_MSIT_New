import axios from "axios";
import React, { useState, useEffect } from "react";
import { Link, useLocation } from "react-router-dom";
import { FaArrowLeft } from "react-icons/fa";

function StudentScores() {
  const [studentData, setStudentData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Get the subject name from the query parameters
  const location = useLocation();
  const searchParams = new URLSearchParams(location.search);
  const subjectName = searchParams.get("subject");

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Use the subjectName in the API call
        const response = await axios.get(`http://127.0.0.1:5000/subject-scores/${subjectName}`);
        setStudentData(response.data);
      } catch (error) {
        setError(error.message);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [subjectName]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!studentData.length) return <div>No student data available</div>;

  const tableStyle = {
    width: '80%', // Set the width of the table
    margin: 'auto', // Center the table horizontally
    marginTop: '20px', // Add spacing on top
    marginBottom: '20px', // Add spacing on bottom
    borderCollapse: 'collapse',
  };
  const thStyle = {
    backgroundColor: '#42c8f5', // Light cement color for heading row
    border: '1px solid black', // Black border for outside table lines
    padding: '8px',
  };
  const cellStyle = {
    border: '1px solid black', // Black border for outside table lines
    padding: '8px',
  };

  return (
    <div>
      <Link to="/mentor">
        <div style={{ position: "absolute", left: "20px" }}>
          <FaArrowLeft style={{ height: "28px", color: "black" }} />
        </div>
      </Link>
      <h1>Student Scores</h1>
      <table style={tableStyle}>
        <thead>
          <tr>
            <th style={thStyle}>Name</th>
            <th style={thStyle}>Email ID</th>
            <th style={thStyle}>Discussions (10%)</th>
            <th style={thStyle}>Quiz (10%)</th>
            <th style={thStyle}>Assignment (20%)</th>
            <th style={thStyle}>Weekly (30%)</th>
            <th style={thStyle}>Total (70%)</th>
            <th style={thStyle}>End Sem (30%)</th>
            <th style={thStyle}>Total (100)</th>
            <th style={thStyle}>Grade</th>
          </tr>
        </thead>
        <tbody>
          {studentData.map((student, index) => (
            <tr key={index}>
              <td style={cellStyle}>{student["Name"]}</td>
              <td style={cellStyle}>{student["Email ID"]}</td>
              <td style={cellStyle}>{student["Discussions (10%)"]}</td>
              <td style={cellStyle}>{student["Quiz (10%)"]}</td>
              <td style={cellStyle}>{student["Assignment (20%)"]}</td>
              <td style={cellStyle}>{student["Weekly (30%)"]}</td>
              <td style={cellStyle}>{student["Total (70%)"]}</td>
              <td style={cellStyle}>{student["End Sem (30%)"]}</td>
              <td style={cellStyle}>{student["Total (100)"]}</td>
              <td style={cellStyle}>{student["Grade "]}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default StudentScores;
