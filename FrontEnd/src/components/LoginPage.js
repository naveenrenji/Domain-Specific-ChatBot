import React, { useContext, useState } from "react";
import { Link, useNavigate, Navigate } from "react-router-dom";
import axios from "axios";
import { UserContext } from "../context/userContext";
import "../App.css";

export default function SignInPage() {
  const { user, setUser, token, authenticated, setAuthenticated } =
    useContext(UserContext);

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const navigate = useNavigate();

  const validateEmail = () => {
    // Email validation regex pattern
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  const validatePassword = () => {
    // Password validation regex pattern
    const passwordRegex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$/;
    return passwordRegex.test(password);
  };

  const onSignIn = async (e) => {
    e.preventDefault();
    // if (!validateEmail()) {
    //   alert("Please enter a valid Email");
    //   return;
    // }
    // if (!validatePassword()) {
    //   alert(
    //     "Please enter a password with at least 8 characters, containing at least one lowercase letter, one uppercase letter, and one number."
    //   );
    //   return;
    // }

    try {
      let body = {
        email: email,
        password: password,
      };
      let { data } = await axios.post(`http://localhost:5000/auth/login`, body);
      if (!Object.keys(data).includes("error")) {
        setUser(data);
        setAuthenticated(true);
        setEmail("");
        setPassword("");

        navigate("/home");
      } else {
        console.log(data);
        setEmail("");
        setPassword("");
      }
    } catch (e) {}
  };

  return (
    <div className="text-center m-5-auto">
      {authenticated ? <Navigate to="/home" /> : null}
      <div>
        <h2>Sign in</h2>
        <p>{user.name}</p>
        <form>
          <p>
            <label>Email address</label>
            <br />
            <input
              type="text"
              name="email"
              required
              onChange={(event) => setEmail(event.target.value)}
            />
          </p>
          <p>
            <label>Password</label>
            <br />
            <input
              type="password"
              name="password"
              required
              onChange={(event) => setPassword(event.target.value)}
            />
          </p>

          <p>
            <button id="sub_btn" onClick={onSignIn} type="submit">
              Login
            </button>
          </p>
        </form>

        <footer>
          <p>
            First time? <Link to="/register">Create an account</Link>.
          </p>
          <p>
            <Link to="/">Back to Homepage</Link>.
          </p>
        </footer>
      </div>
    </div>
  );
}
