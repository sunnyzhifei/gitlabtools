import React from "react";
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import App from "./App"
import LoginComponent from "./component/Login"

function AppRouter() {
  return (
    <Router>
        <Route path="/" exact component={ App } />
        <Route path="/login" component={ LoginComponent } />
    </Router>
  );
}
export default AppRouter;