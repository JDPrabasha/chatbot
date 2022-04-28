import axios from "axios";

export function getReply(input) {
  return axios("http://localhost:5001?input=" + input);
}
