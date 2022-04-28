import React from "react";

function Reply({ message }) {
  return (
    <div className=" flex">
      <div className="ml-auto bg-red-300 mr-3 mt-3 rounded-lg p-2 w-1/4 ">
        <p>{message}</p>
      </div>
    </div>
  );
}

export default Reply;
