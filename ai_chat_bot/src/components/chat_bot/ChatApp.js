import React, { useState } from "react";
import styled from "styled-components";

// Container for the entire chat
const ChatContainer = styled.div`
  display: flex;
  width: 100vw;
  height: 100vh;
  background-color: #f4f4f9;
`;

// Left Side: History of User Messages Only
const MessageHistory = styled.div`
  width: 20%; /* Reduced the width */
  background-color: #ffffff;
  border-right: 2px solid #ddd;
  padding: 20px;
  overflow-y: auto;
  font-family: 'Arial', sans-serif;
  font-size: 14px;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
`;

// Right Side: Chat Area
const ChatArea = styled.div`
  width: 70%; /* Increased width for chat area */
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding: 20px;
  background-color: #e9e9e9;
  border-left: 2px solid #ddd;
  font-family: 'Arial', sans-serif;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
`;

// Chat bubbles
const Message = styled.div`
  background-color: ${props => (props.isUser ? "#5c6bc0" : "#0084ff")};
  color: white;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 8px;
  width: fit-content;
  max-width: 80%;
  margin-left: ${props => (props.isUser ? "auto" : "10px")};
  margin-right: ${props => (props.isUser ? "10px" : "auto")};
  font-size: 16px;
  word-wrap: break-word;
`;

// Input box for the user
const InputContainer = styled.div`
  display: flex;
  border-top: 2px solid #ddd;
  padding: 10px;
  background-color: white;
  border-radius: 10px;
`;

const InputBox = styled.input`
  width: 90%;
  padding: 10px;
  border-radius: 20px;
  border: 1px solid #ddd;
  outline: none;
  font-size: 16px;
`;

const SendButton = styled.button`
  width: 10%;
  padding: 10px;
  border-radius: 20px;
  background-color: #0084ff;
  color: white;
  border: none;
  cursor: pointer;
  font-weight: bold;
  outline: none;
  font-size: 16px;

  &:hover {
    background-color: #0073e6;
  }
`;

function Chatbot() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  // Handle sending messages
  const handleSendMessage = () => {
    if (input.trim() !== "") {
      const newMessage = { text: input, isUser: true };
      setMessages([...messages, newMessage]);
      setInput("");

      // Simulate bot reply after 1 second
      const botReply = { text: "This is a bot reply.", isUser: false };
      setTimeout(() => setMessages(prevMessages => [...prevMessages, botReply]), 1000);
    }
  };

  return (
    <ChatContainer>
      <MessageHistory>
        <h3>Chat History</h3>
        {messages.length === 0 ? (
          <p>No messages yet.</p>
        ) : (
          messages
            .filter(msg => msg.isUser) // Only display user messages
            .map((msg, index) => (
              <Message key={index} isUser={msg.isUser}>
                {msg.text}
              </Message>
            ))
        )}
      </MessageHistory>

      <ChatArea>
        <div>
          {messages.map((msg, index) => (
            <Message key={index} isUser={msg.isUser}>
              {msg.text}
            </Message>
          ))}
        </div>

        <InputContainer>
          <InputBox
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type a message..."
          />
          <SendButton onClick={handleSendMessage}>Send</SendButton>
        </InputContainer>
      </ChatArea>
    </ChatContainer>
  );
}

export default Chatbot;
