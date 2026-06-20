import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000/api",
});

export const sendChatMessage = async (message) => {
  const res = await API.post("/ai/chat/", { message });
  return res.data.reply;
};
