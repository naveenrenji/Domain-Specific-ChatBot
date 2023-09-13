import "./App.css";
import ChatBot from "./components/ChatBot/ChatBot";
import LoginPage from "./components/LoginPage";
import RegisterPage from "./components/RegisterPage";
import UserProvider from "./context/userContext";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <Router>
          <UserProvider>
            <Routes>
              <Route path="/" element={<ChatBot />} />
              <Route path="/login" element={<LoginPage />} />
              <Route path="/register" element={<RegisterPage />} />
              {/* <Route path="/forget-password" element={<ForgetPasswordPage />} /> */}
              {/* <Route path="/home" element={<HomePage />} /> */}
            </Routes>
          </UserProvider>
        </Router>
      </header>
    </div>
  );
}

export default App;
