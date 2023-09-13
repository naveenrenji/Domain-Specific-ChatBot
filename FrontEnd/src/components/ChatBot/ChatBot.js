import React, { useState, useContext, useEffect, useRef } from "react";
import { Link, useNavigate, Navigate } from "react-router-dom";
import "./ChatBot.css";
import { enquiryPhaseFunc } from "./enquiryPhase/Enquiry";
import { mainDialogue } from "./mainDialoguePhase/mainDialogue";
import axios from "axios";
import { UserContext } from "../../context/userContext";

const botIntro = {
  sender: "bot",
  content:
    "Hello, I'm ANN. I'm here to assist you in designing an exceptional engineering project. Whether you're looking to explore a new idea or seeking guidance to improve an existing project, I'm here to help. Your insights and details are crucial for me to offer the most helpful guidance, so thank you in advance for your time and effort in sharing your project's specifics with me. To get started, I'd like to provide some context on generating a new project idea. By understanding the context of your project, I can better assist you in formulating an innovative and impactful engineering design. So, let's embark on this journey together and create something extraordinary!",
};

const chatbotFailMessage = [
  {
    sender: "bot",
    content:
      "The backend chatbot model is offline right now, please try again in sometime",
  },
];
function ChatBot() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [context, setContext] = useState("");
  const [partIndex, setPartIndex] = useState(0);
  const [userInputPhase, setUserInputPhase] = useState("enquiry");
  const [enquiryPhaseStage, setEnquiryPhaseStage] = useState("prompt");

  const messagesEndRef = useRef(null);

  const { user, setUser, token, setToken, authenticated, setAuthenticated } =
    useContext(UserContext);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    localStorage.setItem("chatMessages", JSON.stringify(messages));
    localStorage.setItem("chatContext", JSON.stringify(context));
    scrollToBottom();
  }, [messages, context]);

  useEffect(() => {
    const botMessage = {
      sender: "bot",
      content:
        "Hello, I'm ANN. I'm here to assist you in designing an exceptional engineering project. Whether you're looking to explore a new idea or seeking guidance to improve an existing project, I'm here to help. Your insights and details are crucial for me to offer the most helpful guidance, so thank you in advance for your time and effort in sharing your project's specifics with me. To get started, I'd like to provide some context on generating a new project idea. By understanding the context of your project, I can better assist you in formulating an innovative and impactful engineering design. So, let's embark on this journey together and create something extraordinary!",
    };
    setPartIndex(0);
    setEnquiryPhaseStage("prompt");
    setUserInputPhase("enquiry");
    setMessages([botMessage]);
  }, []);

  const clearChat = () => {
    setMessages([]);
    setContext("");
    localStorage.removeItem("chatMessages");
    localStorage.removeItem("chatContext");
    setMessages([botIntro]);
    setUserInputPhase("enquiry");
    setEnquiryPhaseStage("prompt");
    setPartIndex(0);
  };

  const delay = (ms) => {
    return new Promise((resolve) => {
      setTimeout(resolve, ms);
    });
  };

  const sendMessage = async (e) => {
    e.preventDefault();
    if (input.trim().length === 0) {
      setErrorMessage("Please enter your message first");
      return;
    }
    let response;
    let messagedata = [
      {
        sender: "user",
        content: input,
      },
    ];
    setMessages([...messages, ...messagedata]);
    try {
      let { data } = await axios.post(
        `http://localhost:5000/chat`,
        messagedata[0]
      );
      console.log(data);
      let validityMessage = "";
      if (data["valid"]) {
        validityMessage =
          "Your description has passed the validation test, now proceeding to test for novelty and feasibility.";
      } else {
        validityMessage =
          "Your description did not pass the validation test, all messages to me should be related washing machines";
      }
      console.log(validityMessage);
      let chatbotValidityRes = {
        sender: "bot",
        content: validityMessage,
      };

      setMessages([...messages, ...messagedata, chatbotValidityRes]);

      if (data["valid"]) {
        await delay(3000);
        let chatbotRes = {
          sender: "bot",
          content: data["response"],
        };
        setMessages([
          ...messages,
          ...messagedata,
          chatbotValidityRes,
          chatbotRes,
        ]);
      }
    } catch (error) {
      console.log(Object.keys(error), error.message);
      console.log(messages);
      setMessages([...messages, ...messagedata, ...chatbotFailMessage]);
      console.log(messages);
    }

    setInput("");
    // if (userInputPhase === "enquiry") {
    //   const { responseFromEnquiry, partIndexResult, enquiryPhaseStageResult } =
    //     enquiryPhaseFunc(input, partIndex, enquiryPhaseStage);
    //   setEnquiryPhaseStage(enquiryPhaseStageResult);
    //   setPartIndex(partIndexResult);
    //   response = responseFromEnquiry;
    // } else if (userInputPhase === "mainDialogue") {
    //   response = await mainDialogue(input);
    // }
    // messagedata = [...messagedata, response];
    // setMessages([...messages, ...messagedata]);
    setInput("");
    setErrorMessage("");
  };
  // debugger;
  const handleBubbleClick = (message) => {
    const bubbleMessage = [
      {
        sender: "user",
        content: message,
      },
    ];

    const { responseFromEnquiry, partIndexResult, enquiryPhaseStageResult } =
      enquiryPhaseFunc(message, partIndex, enquiryPhaseStage);
    setEnquiryPhaseStage(enquiryPhaseStageResult);
    setPartIndex(partIndexResult);
    const messagedata = [...bubbleMessage, ...responseFromEnquiry];
    setMessages([...messages, ...messagedata]);
    setInput("");
    setErrorMessage("");
    console.log(messages);
  };

  return (
    <>
      {/* {!authenticated ? <Navigate to="/login" /> : null} */}
      <div className="chat-container">
        <h1 className="chat-title">Academic Chatbot</h1>
        <h2 className="chat-subtitle">Your friendly Academic companion</h2>
        <div>
          {messages.length > 0 && (
            <button className="clear-button" onClick={clearChat}>
              Clear Chat
            </button>
          )}
        </div>
        <div className="chat-messages">
          {messages.map((message, index) => (
            <p className={`chat-message ${message.sender}`} key={index}>
              <b>{message.sender}:</b> {message.content}
            </p>
          ))}
          <div ref={messagesEndRef} />
        </div>
        {["I am not sure...", "I need some motivation"].map((text, i) => (
          <button key={i} onClick={() => handleBubbleClick(text)}>
            {text}
          </button>
        ))}
        <form onSubmit={sendMessage} className="chat-form">
          <input
            className="chat-input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Enter your message"
          />
          <button className="chat-button" type="submit">
            Submit
          </button>
        </form>
        {errorMessage && <p className="error-message">{errorMessage}</p>}
      </div>
    </>
  );
}

export default ChatBot;
