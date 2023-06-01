import React, { useState, useEffect, useRef } from "react";
import "./ChatBot.css";
import axios from "axios";

function ChatBot() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [context, setContext] = useState("");
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    localStorage.setItem("chatMessages", JSON.stringify(messages));
    localStorage.setItem("chatContext", JSON.stringify(context));
    scrollToBottom();
  }, [messages, context]);

  const clearChat = () => {
    setMessages([]);
    setContext("");
    localStorage.removeItem("chatMessages");
    localStorage.removeItem("chatContext");
  };

  const sendMessage = async (e) => {
    e.preventDefault();
    if (input.trim().length === 0) {
      setErrorMessage("Please enter your message first");
      return;
    }
    const response = await axios.post("http://127.0.0.1:5000/chat", {
      message: input,
      context,
    });
    let messagedata = {
      sender: "bot",
      content: "I am too tired right now, can we talk later?",
    };
    if (response.data.response) {
      messagedata = [
        {
          sender: "user",
          content: input,
        },
        {
          sender: "bot",
          content: response.data.response,
        },
      ];
    }

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
