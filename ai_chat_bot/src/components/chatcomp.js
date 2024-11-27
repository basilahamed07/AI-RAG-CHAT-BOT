import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './ChatComponent.css';  // Custom CSS for styling

const ChatComponent = () => {
  // State for chat messages
  const [messages, setMessages] = useState([]);
  // State for input field
  const [userInput, setUserInput] = useState('');
  // State for chat history
  const [history, setHistory] = useState([]);
  // State for file upload
  const [file, setFile] = useState(null);

  // Retrieve the token and file_id from sessionStorage
  const token = sessionStorage.getItem('access_token'); 
  const fileId = sessionStorage.getItem('file_id');  // Get the file_id from sessionStorage

  // Function to handle sending a message
  const sendMessage = async () => {
    if (!userInput.trim() && !file) return; // Don't send if there's no input or file

    const formData = new FormData();
    formData.append('question', userInput);
    if (file) formData.append('file', file);  // Append file if it's selected
    formData.append('file_id', fileId); // Use file_id from sessionStorage

    try {
      const response = await axios.post(
        'http://localhost:5000/chat', // API endpoint
        formData,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'multipart/form-data' // Set the content type to handle file uploads
          }
        }
      );

      const newMessage = {
        question: userInput,
        answer: response.data.response
      };

      // Add the new message to the messages list
      setMessages([...messages, newMessage]);

      // Clear the input field and reset file selection
      setUserInput('');
      setFile(null);
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  // Function to load chat history (initial load)
  const loadHistory = async () => {
    try {
      const url = fileId 
        ? `http://localhost:5000/chat/history?file_id=${fileId}`
        : 'http://localhost:5000/chat/history';

      const response = await axios.get(url, {
        headers: {
          Authorization: `Bearer ${token}` // Send token for authorization
        }
      });

      // Set the history state with the response data
      setHistory(response.data.history);
    } catch (error) {
      console.error('Error loading history:', error);
    }
  };

  // Load history on initial component mount
  useEffect(() => {
    loadHistory();
  }, []);

  return (
    <div className='chat-container'>
      <div className='chat-wrapper'>
        {/* Left Side: Chat History */}
        <div className='chat-history'>
          <h3>Chat History</h3>
          <ul>
            {history.map((item, index) => (
              <li key={index} className="chat-history-item">
                <strong>Q:</strong> {item.question} <br />
                <strong>A:</strong> {item.answer}
              </li>
            ))}
          </ul>
        </div>

        {/* Right Side: Chat Section */}
        <div className='chat-section'>
          <h2>Chat with AI</h2>

          <div className='chat-box'>
            <div className='messages'>
              {/* Display chat messages */}
              {messages.map((msg, index) => (
                <div key={index} className="message-item">
                  <p><strong>Q:</strong> {msg.question}</p>
                  <p><strong>A:</strong> {msg.answer}</p>
                </div>
              ))}
            </div>

            <div className='input-container'>
              {/* Input Field for new question */}
              <input
                type="text"
                value={userInput}
                onChange={(e) => setUserInput(e.target.value)}
                placeholder="Ask a question..."
                className="user-input"
              />

              {/* Conditional rendering of file input */}
              {!fileId && (
                <input
                  type="file"
                  onChange={(e) => setFile(e.target.files[0])}
                  className="file-input"
                />
              )}

              <button onClick={sendMessage} className="send-button">Send</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatComponent;
