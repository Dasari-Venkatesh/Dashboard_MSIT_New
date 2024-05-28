import React from "react";
import { BrowserRouter as Router, Route, Switch, Redirect } from "react-router-dom";
import { Tabs, Tab } from "react-bootstrap";
import "./App.css";
import Logout from "./components/Logout";
import Display from "./components/ScoreDisplay";
import DisplayGrades from "./components/GradesDisplay";
import MentorDashboard from "./components/MentorDashboard";
import PerformanceDisplay from "./components/NEW_PerformanceDisplay";
import LandingPage from "./components/LandingPage";
import PresentationDisplay from "./components/PresentationDisplay";
import Admin from "./pages/admin";
import Mentor from "./pages/mentor";
import Student from "./pages/student";
import AddUser from "./pages/addUser"
import StudentScores from "./pages/studentScore"
import ProtectedRoute from "./components/ProtectedRoute"

export default function App() {
  const [isLoggedin, setIsLoggedin] = React.useState(false);
  const [email, setEmail] = React.useState("");
  const [mentorFlag, setMentorFlag] = React.useState(false);
  const [studentEmailList, setStudentEmailList] = React.useState([]);
  const [data, setData] = React.useState("");
  const [score, setScore] = React.useState("");
  const [ss_score, setSSScore] = React.useState("");
  const [dropoutFlag, setDropoutFlag] = React.useState(false);
  const [key, setKey] = React.useState("performance");

  return (
    <Router>
      <div className="App" style={{ marginLeft: 15, marginRight: 15 }}>
        <Switch>
          <ProtectedRoute path="/admin" component={Admin} allowedRoles={['admin']} />
          <ProtectedRoute path="/mentor" component={Mentor} allowedRoles={['mentor']} />
          <ProtectedRoute path="/add-user" component={AddUser} allowedRoles={['admin']} />
          <ProtectedRoute path="/studentScore" component={StudentScores} allowedRoles={['mentor']} />
          <Route path="/" exact component={LandingPage}>
            {isLoggedin ? (
              mentorFlag ? (
                <Redirect to="/mentor" />
              ) : (
                <Redirect to="/student" />
              )
            ) : null}
          </Route>
        </Switch>
        {isLoggedin && (
          <React.Fragment>
            {mentorFlag ? (
              <div>
                <MentorDashboard
                  mentorFlag={mentorFlag}
                  updateMentorFlag={setMentorFlag}
                  mentorEmail={email}
                  studentEmailList={studentEmailList}
                />
                <br />
                <Logout
                  updateStudentEmailList={setStudentEmailList}
                  updateLogin={setIsLoggedin}
                  updateMentorFlag={setMentorFlag}
                />
                <br />
              </div>
            ) : (
              <React.Fragment>
                <Tabs
                  id="controlled-tab-example"
                  activeKey={key}
                  onSelect={(k) => setKey(k)}
                >
                  <Tab eventKey="performance" title="Performance">
                    <PerformanceDisplay
                      mentor={mentorFlag}
                      email={email}
                      attendance={data.dashboard_data.attendance}
                      grades={data.dashboard_data.grades}
                      lastUpdated={data.last_updated}
                      courseStats={data.course_stats}
                      percentageIT={data.course_attendance.IT}
                      percentageSS={data.course_attendance.SS}
                      learningCenter={data.dashboard_data.learning_center}
                    />
                  </Tab>
                  <Tab eventKey="attendance" title="Attendance">
                    <Display
                      mentor={mentorFlag}
                      userEmail={email}
                      res={data}
                      lastUpdated={data.last_updated}
                      learningCenter={data.dashboard_data.learning_center}
                      score={score}
                      ss_score={ss_score}
                    />
                  </Tab>
                  <Tab eventKey="presentation" title="Presentations">
                    <PresentationDisplay
                      mentor={mentorFlag}
                      email={email}
                      lastUpdated={data.last_updated}
                      res={data}
                      learningCenter={data.dashboard_data.learning_center}
                      pptScores={data.dashboard_data.ppt_scores}
                    />
                  </Tab>
                  <Tab eventKey="transcript" title="Transcript">
                    <DisplayGrades
                      mentor={mentorFlag}
                      email={email}
                      res={data}
                      lastUpdated={data.last_updated}
                      learningCenter={data.dashboard_data.learning_center}
                    />
                  </Tab>
                </Tabs>
                {dropoutFlag && <h5>Student has dropped out.</h5>}
                <br />
                <Logout
                  updateLogin={setIsLoggedin}
                  updateMentorFlag={setMentorFlag}
                />
                <br />
              </React.Fragment>
            )}
          </React.Fragment>
        )}
      </div>
    </Router>
  );
}
