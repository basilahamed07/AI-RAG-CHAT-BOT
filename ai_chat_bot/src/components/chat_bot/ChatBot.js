import React, { useState } from "react";
import axios from "axios";

const Chatbot = () => {
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);
  const [fileId, setFileId] = useState(""); // Add state to hold file_id

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!question.trim()) {
      return;
    }

    setLoading(true);
    try {
      const token = localStorage.getItem("jwt_token"); // Assuming JWT is stored in localStorage

      const formData = new FormData();
      formData.append("question", question);
      if (fileId) {
        formData.append("file_id", fileId);  // Add file_id if available
      }

      const res = await axios.post(
        "http://localhost:5000/chat",
        formData,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "multipart/form-data",
          },
        }
      );

      setResponse(res.data.response);
    } catch (error) {
      console.error("Error:", error);
      setResponse("Sorry, there was an error. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>Chat with our Bot</h2>
      <form onSubmit={handleSubmit}>
        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask a question..."
          rows="4"
          cols="50"
        />
        <br />
        
        {/* Input for file_id */}
        <input
          type="text"
          value={fileId}
          onChange={(e) => setFileId(e.target.value)}
          placeholder="Enter file ID (optional)"
        />
        <br />
        
        <button type="submit" disabled={loading}>
          {loading ? "Sending..." : "Send"}
        </button>
      </form>

      {response && (
        <div>
          <h3>Response:</h3>
          <p>{response}</p>
        </div>
      )}
    </div>
  );
};

export default Chatbot;
