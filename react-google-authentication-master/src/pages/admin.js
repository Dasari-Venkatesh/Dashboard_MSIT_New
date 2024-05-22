import React, { useState, useEffect } from "react";
import Logout from "../components/Logout";
import axios from "axios";
import SearchBar from "../components/SearchBar";
import { Link } from "react-router-dom"; 
import { Button, Dropdown } from "react-bootstrap";

function Admin() {

  function handleAddUser(){
    
  }

  return (
    <div >
      
      <SearchBar/>
      {/* Button using Tailwind CSS */}
      <Link to="/add-user">
        <Button style={{margin:"2rem 2rem"}}>Add user</Button>
      </Link>

      <Logout/>
    </div>
  );
}

export default Admin;
