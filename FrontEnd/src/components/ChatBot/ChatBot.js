import React, { useState, useEffect, useRef } from "react";
import "./ChatBot.css";
import { enquiryPhaseFunc } from "./enquiryPhase/Enquiry";
import { mainDialogue } from "./mainDialoguePhase/mainDialogue";

const botIntro = {
  sender: "bot",
  content:
    "Hello, I'm ANN (short for Artificial Neural Networks). I'm here to assist you in designing an exceptional engineering project. Your insights and details are crucial for me to offer the most helpful guidance. So, thank you in advance for your time and effort in sharing your project's specifics with me. Before we begin, may I ask how you would like to be addressed?",
};

function ChatBot() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [context, setContext] = useState("");
  const [partIndex, setPartIndex] = useState(0);
  const [userInputPhase, setUserInputPhase] = useState("enquiry");
  const [enquiryPhaseStage, setEnquiryPhaseStage] = useState("prompt");

  const messagesEndRef = useRef(null);

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
        "Hello, I'm ANN (short for Artificial Neural Networks). I'm here to assist you in designing an exceptional engineering project. Your insights and details are crucial for me to offer the most helpful guidance. So, thank you in advance for your time and effort in sharing your project's specifics with me. Before we begin, may I ask how you would like to be addressed?",
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
    setInput("");
    if (userInputPhase === "enquiry") {
      const { responseFromEnquiry, partIndexResult, enquiryPhaseStageResult } =
        enquiryPhaseFunc(input, partIndex, enquiryPhaseStage);
      setEnquiryPhaseStage(enquiryPhaseStageResult);
      setPartIndex(partIndexResult);
      response = responseFromEnquiry;
    } else if (userInputPhase === "mainDialogue") {
      response = await mainDialogue(input);
    }
    messagedata = [...messagedata, response];
    setMessages([...messages, ...messagedata]);
    setInput("");
    setErrorMessage("");
  };

  const handleBubbleClick = (message) => {
    const bubbleMessage = [{
      sender: "user",
      content: message,
    }];
    const { responseFromEnquiry, partIndexResult, enquiryPhaseStageResult } =
      enquiryPhaseFunc(message, partIndex, enquiryPhaseStage);
    setEnquiryPhaseStage(enquiryPhaseStageResult);
    setPartIndex(partIndexResult);
    const messagedata = [...bubbleMessage, responseFromEnquiry]
    setMessages([...messages, ...messagedata]);
    setInput("");
    setErrorMessage("");
  };

  return (
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
  );
}

export default ChatBot;
