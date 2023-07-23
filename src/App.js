import React, { useState, useEffect } from "react";

function App() {
  const [text, setText] = useState("");
  const [predictedText, setPredictedText] = useState("");
  const [backendStatus, setBackendStatus] = useState("Connecting...");

  useEffect(() => {
    // Check backend connection status
    fetch("/")
      .then(() => setBackendStatus("Connected"))
      .catch(() => setBackendStatus("Disconnected"));
  }, []);

  const handleInputChange = (event) => {
    const newText = event.target.value;
    setText(newText);
  };

  const handleNextWordPrediction = () => {
    // Send text to the backend for next word prediction
    fetch("http://127.0.0.1:8000/next-word-predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text: text }),
    })
      .then((response) => response.json())
      .then((data) => {
        const predictedText = data.predictedText;
        setPredictedText(predictedText);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  const handleNextSentencePrediction = () => {
    // Send text to the backend for next sentence prediction
    fetch("http://127.0.0.1:8000/next-sentence-predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text: text }),
    })
      .then((response) => response.json())
      .then((data) => {
        const predictedText = data.predictedText;
        setPredictedText(predictedText);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  return (
    <div className="container">
      <h1 className="title">Predictive Text App</h1>
      <div className="status">
        <strong>Backend Status:</strong> {backendStatus}
      </div>
      <textarea
        className="input"
        value={text}
        onChange={handleInputChange}
        rows="5"
        cols="50"
      ></textarea>
      <br />
      <button onClick={handleNextWordPrediction}>Next Word Prediction</button>
      <button onClick={handleNextSentencePrediction}>Next Sentence Prediction</button>
      <br />
      <div className="predicted-text">
        <h2>Predicted Text:</h2>
        <p>{predictedText}</p>
      </div>
    </div>
  );
}

export default App;