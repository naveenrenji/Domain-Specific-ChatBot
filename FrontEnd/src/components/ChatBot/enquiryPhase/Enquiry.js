const parts = [
  {
    title: "Title of Your Design Project",
    prompt:
      "Let's start by naming your project. Could you please tell me what your engineering design project is titled?",
    fallback:
      "If you're finding it challenging, think of something that describes your project's main idea or objective. For example, if your project is about creating a more efficient washing machine, you could call it 'Smart Water-Efficient Washing Machine'.",
    motivation:
      "Don't worry, naming your project can be a creative process. Remember, the title should capture the essence of your vision, and there's no rush. Take your time to think about it.",
  },
  {
    title: "Design Project Description",
    prompt:
      "Next, could you please give me a detailed description of your project? The more you can tell me about the problem you're trying to solve and your specific goals, the better I can understand your needs.",
    fallback:
      "If you're unsure where to start, you could begin by talking about the purpose of your project, its target audience, or any unique attributes it may have. For instance, if your project is about a washing machine, you could discuss its capacity, energy sources, cost-efficiency, and so on.",
    motivation:
      "I understand that summarizing your project can be challenging, but don't worry. Even small details can be very helpful in making your project more clear. Take your time, and remember that each bit of information brings us closer to understanding your vision better.",
  },
  {
    title: "Initial Ideas and Concepts",
    prompt:
      "Could you share your initial ideas or concepts related to the project? These insights would help me understand your thought process better.",
    fallback:
      "If you're finding it difficult to express your ideas at this point, don't worry! You might start by explaining the core technology or method you're considering for your project. For a smart washing machine, you could discuss how you plan to integrate smart technologies, or any innovative features you want to include, such as AI-based fabric care.",
    motivation:
      "Don't worry if you're finding it challenging to articulate your ideas. All big projects start with small ideas. Feel free to share any thoughts, however preliminary they may be. Remember, creativity knows no bounds!",
  },
  {
    title: "Design Objectives",
    prompt:
      "Finally, could you tell me about the objectives of your design project? Understanding your goals would help me tailor my recommendations and suggestions to your specific needs.",
    fallback:
      "If you're unsure, try thinking about the impact you want your project to have. If your project is a smart washing machine, do you aim to make it affordable, highly efficient, user-friendly, or something else?",
    motivation:
      "I understand that setting objectives can sometimes be challenging, but it's an essential step in shaping your project. These goals will serve as a roadmap for your design process. Remember, no goal is too big or small, and I'm here to help you achieve it!",
  },
];

function validateUserInput(message, part) {
  if (message.length < 5) {
    return false;
  } else {
    return true;
  }
}

const enquiryPhaseFunc = (message, partIndex, EnquiryPhaseStage) => {
  const part = parts[partIndex];
  let nextBotMessage = null;

  if (message === "I'm not sure...") {
    nextBotMessage = {
      sender: "bot",
      content: part.fallback,
    };
    EnquiryPhaseStage = "fallback";
  } else if (message === "I need some motivation") {
    nextBotMessage = {
      sender: "bot",
      content: part.motivation,
    };
    EnquiryPhaseStage = "motivation";
  } else {
    if (EnquiryPhaseStage === "answerEnquiry" && partIndex < parts.length) {
      nextBotMessage = {
        sender: "bot",
        content: parts[partIndex]?.prompt,
      };
      // partIndex = partIndex + 1;
      EnquiryPhaseStage = "prompt";
    } else if (partIndex === 0) {
      nextBotMessage = {
        sender: "bot",
        content: parts[partIndex]?.prompt,
      };
      EnquiryPhaseStage = "prompt";
    }
    // Implement validation for each part here
    else if (!validateUserInput(message, part)) {
      nextBotMessage = {
        sender: "bot",
        content: "Your input was not valid, please try again.",
      };
      EnquiryPhaseStage = "prompt";
    }
  }

  if (partIndex === parts.length) {
    const finalMessage = 
      {
        sender: "bot",
        content:
          "Thank you again for sharing all this valuable information! Let's continue shaping your idea into a successful project!",
      }
    ;
    nextBotMessage = finalMessage;
    EnquiryPhaseStage = "completed";
  }

  const messages = nextBotMessage;

  const result = {
    responseFromEnquiry: nextBotMessage,
    partIndexResult: partIndex,
    enquiryPhaseStageResult: EnquiryPhaseStage,
  };

  // Convert the messages to JSON and store it.
  const enquiryPhaseResults = JSON.stringify(messages);
  localStorage.setItem("enquiryPhaseResults", enquiryPhaseResults);

  return result;
};

module.exports = {
  parts,
  enquiryPhaseFunc,
};
