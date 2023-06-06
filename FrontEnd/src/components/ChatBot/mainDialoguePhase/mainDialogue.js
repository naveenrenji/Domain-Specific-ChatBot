import axios from "axios";

const mainDialogue = async (input, context) => {
    let response, messagedata;
    try {
        response = await axios.post("http://127.0.0.1:5000/chat", {
          message: input,
          context,
        });
      } catch (e) {
        messagedata = [{
          sender: "bot",
          content: "I am too tired right now, can we talk later?",
        }];
      }
      if (response) {
        if (response.data) {
          if (response.data.response) {
            messagedata = [
              {
                sender: "bot",
                content: response.data.response,
              },
            ];
          }
        }
      }

      return messagedata;
  }

  export {  mainDialogue };