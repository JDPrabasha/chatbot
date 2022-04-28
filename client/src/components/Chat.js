import { React, useState } from "react";
import Message from "./Message";
import Reply from "./Reply";
import { getReply } from "../services/api";

function Chat() {
  const [messages, setMessages] = useState([]);
  const handleKeyDown = (event) => {
    if (event.key === "Enter") {
      const newMessage = event.target.value;

      setMessages([
        ...messages,
        { type: "message", value: event.target.value },
      ]);
      event.target.value = "";

      getReply(newMessage).then((res) => {
        setMessages((messages) => [
          ...messages,
          { type: "reply", value: res.data.message },
        ]);
      });
    }
  };

  return (
    <div className="w-1/2 mx-auto bg-slate-100   bg-grey-lighter min-h-screen">
      <h1 className="mx-auto text-center text-2xl font-semibold ">
        🤖 chatbot
      </h1>
      {messages.map((message) =>
        message.type == "message" ? (
          <Message message={message.value} />
        ) : (
          <Reply message={message.value} />
        )
      )}

      <div className="flex justify-center">
        <div className="fixed bottom-4 xl:w-96">
          <label
            for="exampleFormControlTextarea1"
            className="form-label inline-block mb-2 text-gray-700 font-semibold"
          >
            Your Message
          </label>
          <textarea
            className="
        form-control
        block
        w-full
        px-3
        py-1.5
        text-base
        font-normal
        text-gray-700
        bg-white bg-clip-padding
        border border-solid border-gray-300
        rounded
        transition
        ease-in-out
        m-0
        focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none
      "
            id="exampleFormControlTextarea1"
            rows="3"
            placeholder="Your message"
            onKeyDown={handleKeyDown}
          ></textarea>
        </div>
      </div>
    </div>
  );
}

export default Chat;
