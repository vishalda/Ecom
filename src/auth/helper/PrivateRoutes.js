import React, { Component } from "react";
import { Route, Redirect } from "react-router-dom";
import { isAuthenticated } from ".";

const PrivateRoutes = ({ children, ...rest }) => {
  return (
    <Route
      {...rest}
      render={(props) =>
        isAuthenticated ? (
          <Component {...props} />
        ) : (
          <Redirect
            to={{ pathname: "/signin", state: { from: props.locationn } }}
          />
        )
      }
    />
  );
};

export default PrivateRoutes;
