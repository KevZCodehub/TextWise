import React, { useState, useEffect } from "react";

function App() {
  const [text, setText] = useState("");
  const [predictedText, setPredictedText] = useState("");
  const [backendStatus, setBackendStatus] = useState("Connecting...");

  useEffect(() => {
    // Check backend connection status
    fetch("/predict")
      .then(() => setBackendStatus("Connected"))
      .catch(() => setBackendStatus("Disconnected"));
  }, []);

  const handleInputChange = (event) => {
    const newText = event.target.value;
    setText(newText);

    // Send text to the C service
    fetch("/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text: newText }),
    })
      .then((response) => response.json())
      .then((data) => {
        setPredictedText(data.predictedText);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  return (
    <div>
      <h1>Predictive Text App</h1>
      <div>
        <strong>Backend Status:</strong> {backendStatus}
      </div>
      <textarea
        value={text}
        onChange={handleInputChange}
        rows="5"
        cols="50"
      ></textarea>
      <br />
      <div>
        <h2>Predicted Text:</h2>
        <p>{predictedText}</p>
      </div>
    </div>
  );
}

export default App;
