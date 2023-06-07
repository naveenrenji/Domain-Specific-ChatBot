import React, { useState, useEffect, useRef } from "react";
import "./ChatBot.css";
import { enquiryPhaseFunc } from "./enquiryPhase/Enquiry";
import { mainDialogue } from "./mainDialoguePhase/mainDialogue";
import { parts } from "./enquiryPhase/Enquiry";

const botIntro = {
  sender: "bot",
  content:
    "Hello, I'm ANN (short for Artificial Neural Networks). I'm here to assist you in designing an exceptional engineering project. Your insights and details are crucial for me to offer the most helpful guidance. So, thank you in advance for your time and effort in sharing your project's specifics with me. Before we begin, may I ask how you would like to be addressed?",
};

const optionButtons = ["Answer", "I'm not sure...", "I need some motivation"];

function ChatBot() {
  const [messages, setMessages] = useState([botIntro]);
  const [input, setInput] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [context, setContext] = useState("");
  const [partIndex, setPartIndex] = useState(0);
  const [userInputPhase, setUserInputPhase] = useState("answerEnquiry");
  const [enquiryPhaseStage, setEnquiryPhaseStage] = useState("prompt");
  const [userName, setUserName] = useState("");
  const [enquiryResults, setEnquiryResults] = useState([]);

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
    setUserInputPhase("answerEnquiry");
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

  const handleFirstInput = (input) => {
    const messageData = [
      { sender: "user", content: input },
      {
        sender: "bot",
        content: "Hi " + input + ". It is nice to talk to you, I would like to ask you a few questions about the engineering design project you have in mind."
      }
    ];
    setUserName(input);
    setMessages([...messages, ...messageData]);

    const {
      responseFromEnquiry,
      partIndexResult,
      enquiryPhaseStageResult,
    } = enquiryPhaseFunc("input", partIndex, enquiryPhaseStage);

    const firstEnquiry = responseFromEnquiry; // this should return the first enquiry
    setMessages((prevMessages) => [...prevMessages, firstEnquiry]);
    setUserInputPhase("enquiry");
    let istate = userInputPhase;
};


  const handleEnquiryPhase = (input) => {
    let istate = userInputPhase;
    setUserInputPhase("enquiry");
    const {
      responseFromEnquiry,
      partIndexResult,
      enquiryPhaseStageResult,
    } = enquiryPhaseFunc(input, partIndex, enquiryPhaseStage);
  
    setEnquiryPhaseStage(enquiryPhaseStageResult);
    setPartIndex(partIndexResult);
  
    // Check if the enquiry phase is completed and, if so, switch to mainDialogue phase
    if (enquiryPhaseStageResult === "completed") {
      setUserInputPhase("mainDialogue");
    }
     istate = userInputPhase;

    return responseFromEnquiry;
  };

  const handleMainDialoguePhase = async (input) => {
    const response = await mainDialogue(input, context); // added context as parameter in mainDialogue function
    return response;
  };
  


  const sendMessage = async (e) => {
    e.preventDefault();
    if (input.trim().length === 0) {
      return;
    }
  
    let response;
    const messageData = { sender: "user", content: input };
    setInput("");
    let istate = userInputPhase;

    if (userName === "") {
      handleFirstInput(input);
      return; // After handleFirstInput, we stop execution because sendMessage will be called again
    } else if (userInputPhase === "enquiry" || userInputPhase === "answerEnquiry") {
      response = handleEnquiryPhase(input);
      if(userInputPhase==="answerEnquiry"){
        const enquiryData = [{
          title : parts[partIndex-1].title,
          content : input
        }]
        setEnquiryResults([...enquiryResults,...enquiryData]);
      }
    } else if (userInputPhase === "mainDialogue") {
      response = await handleMainDialoguePhase(input);
    }
  
    setMessages([...messages, messageData, response]);
  };
  

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
    const messagedata = [...bubbleMessage, responseFromEnquiry];
    setMessages([...messages, ...messagedata]);
    setInput("");
    setErrorMessage("");
  };

  const handleOptionButtonClick = (option) => {
    if (option === "Answer") {
      setPartIndex(partIndex+1);
      setUserInputPhase("answerEnquiry");
      setEnquiryPhaseStage("answerEnquiry");
    } else {
      handleBubbleClick(option);
    }
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
      {userInputPhase === "enquiry" && enquiryPhaseStage !== "completed" && (
        <div className="options-container">
          {optionButtons.map((option, i) => (
            <button
              key={i}
              className={`option-button option-button-${i}`}
              onClick={() => handleOptionButtonClick(option)}
            >
              {option}
            </button>
          ))}
        </div>
      )}
      {(userInputPhase === "mainDialogue" ||
        userInputPhase === "answerEnquiry") && (
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
      )}

      {errorMessage && <p className="error-message">{errorMessage}</p>}
    </div>
  );
}

export default ChatBot;
