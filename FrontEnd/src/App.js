import "./App.css";
import ChatBot from "./components/ChatBot/ChatBot";
import LoginPage from "./components/LoginPage";
import RegisterPage from "./components/RegisterPage";
import Home from "./components/Home/Home";
import Header from "./components/Header/Header";
import UserProvider from "./context/userContext";
import {
  BrowserRouter as Router,
  Route,
  Link,
  Routes,
  Navigate,
} from "react-router-dom";

function App() {
  return (
    <Router>
      <div>
        <Routes>
          <Route path="/" element={<ChatBot />} />
          <Route path="/chatbot" element={<ChatBot />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
