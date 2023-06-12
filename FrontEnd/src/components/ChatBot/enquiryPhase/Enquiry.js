const parts = [
    {
      title: "Title of Your Design Project",
      prompt: "Great! Now, let's move on to the exciting part of naming your engineering design project. Please take a moment to think about a title that accurately represents your project. You can draw inspiration from any past experiences you've had or even explore hypothetical ideas. Feel free to be creative and descriptive with your title. Once you have it, kindly share it with me",
      motivation: "Don't worry, naming your project can be a creative process. Remember, the title should capture the essence of your vision, and there's no rush. Take your time to think about it."
    },
    {
      title: "Design Project Description",
      prompt: "Next, could you describe your project to me in simple terms? I would appreciate it if you could provide a brief description of your project. The more details you can provide about the problem you're trying to solve and your specific goals, the better I can understand your needs. To help you break it down, you can start by telling me what problem you're aiming to address with your project and what you hope to achieve. ",
      fallback: "If you're unsure where to start, you could begin by talking about the purpose of your project, its target audience, or any unique attributes it may have. For instance, if your project is about a washing machine, you could discuss its capacity, energy sources, cost-efficiency, and so on.",
      motivation: "I understand that summarizing your project can be challenging, but don't worry. Even small details can be very helpful in making your project more clear. Take your time, and remember that each bit of information brings us closer to understanding your vision better."
    },
    {
      title: "Initial Ideas and Concepts",
      prompt: "How would you implement your project? Could you tell me about the technologies or methods you're considering using? Sharing your initial ideas or concepts related to the project will help me understand your thought process better.",
      fallback: "If you're finding it difficult to express your ideas at this point, don't worry! You might start by explaining the core technology or method you're considering for your project. For a smart washing machine, you could discuss how you plan to integrate smart technologies, or any innovative features you want to include, such as AI-based fabric care.",
      motivation: "Don't worry if you're finding it challenging to articulate your ideas. All big projects start with small ideas. Feel free to share any thoughts, however preliminary they may be. Remember, creativity knows no bounds!"
    },
    {
      title: "Design Objectives",
      prompt: "To better align my guidance with your needs, could you please provide more details about how you envision implementing your project and the specific technologies you plan to use? Understanding your goals and implementation approach will allow me to provide tailored recommendations and suggestions.",
      fallback: "If you're unsure, try thinking about the impact you want your project to have. If your project is a smart washing machine, do you aim to make it affordable, highly efficient, user-friendly, or something else?",
      motivation: "I understand that setting objectives can sometimes be challenging, but it's an essential step in shaping your project. These goals will serve as a roadmap for your design process. Remember, no goal is too big or small, and I'm here to help you achieve it!"
    }
  ];

  const enquiryPhaseFunc = (message, partIndex, EnquiryPhaseStage) => {
    const part = parts[partIndex];
    if (!part) {
      return;
    }

    let nextBotMessage = null;
    if (message === "I am not sure...") {
      nextBotMessage = [{
        sender: "bot",
        content: part.fallback,
      }];
      EnquiryPhaseStage = "fallback";
    } else if (message === "I need some motivation") {
      nextBotMessage = [{
        sender: "bot",
        content: part.motivation,
      }];
      EnquiryPhaseStage = "motivation";
    } else {
      // Implement validation for each part here
      // if (!validateUserInput(message, part)) {
      //   nextBotMessage = {
      //     sender: "bot",
      //     content: "Your input was not valid, please try again.",
      //   };
      //   setUserInputPhase("prompt");
      // } else {
      nextBotMessage = {
        sender: "bot",
        content: parts[partIndex + 1]?.prompt,
      };
      partIndex = partIndex +1;
      EnquiryPhaseStage = "prompt";
      // }
    }

    if (partIndex === parts.length) {
      const finalMessage = [{
        sender: "bot",
        content:
          "Thank you again for sharing all this valuable information! Let's continue shaping your idea into a successful project!",
      }];
      nextBotMessage = [...nextBotMessage,...finalMessage];
    }

    const messages = nextBotMessage;

    const result = {
      responseFromEnquiry: nextBotMessage,
      partIndexResult: partIndex,
      enquiryPhaseStageResult: EnquiryPhaseStage
    }

    // Convert the messages to JSON and store it.
    const enquiryPhaseResults = JSON.stringify(messages);
    localStorage.setItem("enquiryPhaseResults", enquiryPhaseResults);


    return result;
  };

  module.exports = {
    parts,
    enquiryPhaseFunc
  };
