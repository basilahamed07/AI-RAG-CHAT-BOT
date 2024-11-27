import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';  // Add useNavigate hook for navigation
import './BotForm.css';

const BotForm = () => {
  const [selectedOption, setSelectedOption] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [botName, setBotName] = useState('');
  const [file, setFile] = useState(null);
  const [responseMessage, setResponseMessage] = useState('');
  const [bots, setBots] = useState([]); // To store existing bots
  const navigate = useNavigate();  // Hook for navigation

  // Fetch the list of bots from the backend when the "Select the Bot" option is clicked
  useEffect(() => {
    if (selectedOption === 'select') {
      // Fetch the available bots
      axios
        .get('http://localhost:5000/bots', {
          headers: {
            'Authorization': `Bearer ${sessionStorage.getItem('access_token')}`,
          },
        })
        .then((response) => {
          setBots(response.data.history); // Assuming response contains a list of bots under 'history'
        })
        .catch((error) => {
          console.error('Error fetching bots:', error);
        });
    }
  }, [selectedOption]);

  // Handle option change (Select the Bot or Create the Bot)
  const handleOptionChange = (option) => {
    setSelectedOption(option);
    setShowModal(true); // Show modal when either option is selected
  };

  // Handle bot name change
  const handleBotNameChange = (e) => {
    setBotName(e.target.value);
  };

  // Handle file change
  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  // Handle form submission for creating a new bot
  const handleFormSubmit = (e) => {
    e.preventDefault();

    if (!botName || !file) {
      setResponseMessage('Please provide both a bot name and a file.');
      return;
    }

    const formData = new FormData();
    formData.append('bot_name', botName);  // Send bot_name
    formData.append('file', file);  // Send the file

    axios
      .post('http://localhost:5000/bot-create', formData, {
        headers: {
          'Authorization': `Bearer ${sessionStorage.getItem('access_token')}`,
        },
      })
      .then((response) => {
        setResponseMessage('Bot created successfully!');
        setShowModal(false); // Close modal on success
        setBots((prevBots) => [...prevBots, response.data]); // Optionally, add the new bot to the list of bots
      })
      .catch((error) => {
        setResponseMessage('Error creating bot: ' + error.response?.data || error.message);
        console.error('Error:', error);
      });
  };

  // Handle selecting a bot (if applicable)
  const handleSelectBot = (botId, botName) => {
    // Set the selected bot details in sessionStorage
    const userId = sessionStorage.getItem('user_id');  // Assuming user_id is saved in sessionStorage
    sessionStorage.setItem('chatbot_name', botName);
    sessionStorage.setItem('file_id', botId);
    sessionStorage.setItem('user_id', userId);  // Store user_id in sessionStorage

    // Navigate to the ChatComp page
    navigate('/chatcomp');  // Make sure '/chatcomp' is the correct path for the chat component
  };

  // Close modal by clicking outside the modal content
  const handleCloseModal = (e) => {
    if (e.target.className === 'modal-overlay') {
      setShowModal(false);
    }
  };

  return (
    <div className="bot-form-container">
      <div className="options-container">
        <button onClick={() => handleOptionChange('select')}>Select the Bot</button>
        <button onClick={() => handleOptionChange('create')}>Create the Bot</button>
      </div>

      {/* Conditionally render modal */}
      {showModal && (
        <div className="modal-overlay" onClick={handleCloseModal}>
          <div className="modal-content">
            <div className="bot-options">
              {/* Option to select an existing bot */}
              <div className={`bot-option ${selectedOption === 'select' ? 'active' : ''}`}>
                {selectedOption === 'select' && (
                  <div>
                    <h3>Select an Existing Bot</h3>
                    {bots.length === 0 ? (
                      <div>
                        <p>You don't have any chatbots. Create one!</p>
                        <button onClick={() => handleOptionChange('create')}>Create a Bot</button>
                      </div>
                    ) : (
                      <div>
                        <p>Select a bot from the list:</p>
                        <ul>
                          {bots.map((bot, index) => (
                            <li key={index}>
                              <button
                                className="bot-select-button"
                                onClick={() => handleSelectBot(bot.file_id, bot.bot_name)}
                              >
                                {bot.bot_name}
                              </button>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                )}
              </div>

              {/* Option to create a new bot */}
              <div className={`bot-option ${selectedOption === 'create' ? 'active' : ''}`}>
                {selectedOption === 'create' && (
                  <div>
                    <h3>Create a New Bot</h3>
                    <form onSubmit={handleFormSubmit}>
                      <div>
                        <label>Chatbot Name:</label>
                        <input
                          type="text"
                          value={botName}
                          onChange={handleBotNameChange}
                          placeholder="Enter bot name"
                          required
                        />
                      </div>
                      <div>
                        <label>Choose Bot File:</label>
                        <input
                          type="file"
                          onChange={handleFileChange}
                          required
                        />
                      </div>
                      <button type="submit">Create Bot</button>
                    </form>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Display the response message */}
      {responseMessage && <div className="response-message">{responseMessage}</div>}
    </div>
  );
};

export default BotForm;
