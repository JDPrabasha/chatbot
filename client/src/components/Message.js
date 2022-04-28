import React from "react";

function Message({ message }) {
  return (
    <div className=" flex">
      <div className="mr-auto bg-blue-300 ml-3 mt-3 rounded-lg p-2 w-1/4 ">
        <p>{message}</p>
      </div>
    </div>
  );
}

export default Message;
