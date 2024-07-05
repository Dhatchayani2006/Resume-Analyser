import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [file, setFile] = useState(null);
  const [response, setResponse] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const formData = new FormData();
    formData.append('file', file);
    formData.append('user_prompt', 'Your user prompt here');  // Add any necessary user prompt

    try {
      const res = await axios.post('http://127.0.0.1:8000/api/upload/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      setResponse(res.data);
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  };

  return (
    <div className="App">
      <h1>Resume Analyzer</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" accept="application/pdf" onChange={handleFileChange} />
        <button type="submit">Upload</button>
      </form>
      {response && (
        <div>
          <h2>Generated Text:</h2>
          <p>{response.generated_text}</p>
          <h2>Parsed Resume Data:</h2>
          <p>Name: {response.name}</p>
          <p>Experience: {response.experience}</p>
          <p>Education: {response.education}</p>
        </div>
      )}
    </div>
  );
}

export default App;
