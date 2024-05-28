import React from 'react';
import { Route, Redirect } from 'react-router-dom';

const ProtectedRoute = ({ component: Component, allowedRoles, ...rest }) => {
  return (
    <Route
      {...rest}
      render={props => {
        const userRole = localStorage.getItem("userRole");
        if (allowedRoles.includes(userRole)) {
          return <Component {...props} />;
        } else {
          return <Redirect to="/" />;
        }
      }}
    />
  );
};

export default ProtectedRoute;
