import React, { useState } from 'react';
import './Home.css'; // For styling

const Home = () => {
  const [messages, setMessages] = useState([]);
  const [userInput, setUserInput] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [activeChat, setActiveChat] = useState(null);

  // Handle input change
  const handleInputChange = (e) => {
    setUserInput(e.target.value);
  };

  // Send message and simulate bot response
  const handleSendMessage = () => {
    if (userInput.trim() === '') return;

    const newMessage = { sender: 'user', text: userInput };
    const botResponse = { sender: 'bot', text: `You said: ${userInput}` };

    // Add the new message to the current active chat
    setMessages((prevMessages) => [...prevMessages, newMessage, botResponse]);

    // Simulate bot response
    setTimeout(() => {
      setMessages((prevMessages) => [...prevMessages, botResponse]);
    }, 1000);

    // Clear input field
    setUserInput('');

    // Save the current chat session
    const newChat = { id: Date.now(), messages: [...messages, newMessage, botResponse] };
    setChatHistory((prevHistory) => [newChat, ...prevHistory]);
    setActiveChat(newChat); // Set active chat to the newly created one
  };

  // Load selected chat from history
  const handleChatClick = (chat) => {
    setMessages(chat.messages);
    setActiveChat(chat);
  };

  return (
    <div className="chat-container">
      <div className="sidebar">
        <h3>Chat History</h3>
        <div className="history-list">
          {chatHistory.map((chat) => (
            <div
              key={chat.id}
              className={`history-item ${activeChat?.id === chat.id ? 'active' : ''}`}
              onClick={() => handleChatClick(chat)}
            >
              Chat {new Date(chat.id).toLocaleString()}
            </div>
          ))}
        </div>
      </div>
      <div className="chat-box">
        <div className="chat-history">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`message ${message.sender === 'bot' ? 'bot' : 'user'}`}
            >
              <span>{message.text}</span>
            </div>
          ))}
        </div>
        <div className="chat-input">
          <input
            type="text"
            value={userInput}
            onChange={handleInputChange}
            onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
            placeholder="Type a message..."
          />
          <button onClick={handleSendMessage}>Send</button>
        </div>
      </div>
    </div>
  );
};

export default Home;
