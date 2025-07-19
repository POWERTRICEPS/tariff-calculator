import React, { useState } from "react";
import axios from "axios";
import 'bootstrap/dist/css/bootstrap.min.css';



function App() {

  const [description, setDescription] = useState("");
  const [country, setCountry] = useState("");
  const [value, setValue] = useState("");

  const [topMatches, setTopMatches] = useState([]);
  const [selectedHTS, setSelectedHTS] = useState('');
  const [matchUpdated, setMatchUpdated] = useState(false);
  const [result, setResult] = useState(null);


   const handleMatch = async () => {
    try {
      const res = await axios.post('http://127.0.0.1:8000/match', {
        description,
        country,
        value: parseFloat(value),
      });
      setTopMatches(res.data.top_matches);
      setMatchUpdated(true);
      setTimeout(() => setMatchUpdated(false), 3000);
    } catch (error) {
      console.error(error);
      alert('Failed to retrieve HTS matches.');
    }
  };



  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const res = await axios.post("http://127.0.0.1:8000/calculate", {
        description,
        country,
        value: parseFloat(value),
        hts_code: selectedHTS,
      });
      setResult(res.data);
    } catch (error) {
      console.error(error);
      alert("Failed to calculate tariff.");
    }
  };




   return (
    <div className="container mt-4">
      <h2>Tariff Calculator</h2>
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label className="form-label">Product Description</label>
          <input
            type="text"
            className="form-control"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />
        </div>
        <div className="mb-3">
          <label className="form-label">Country of Origin</label>
          <input
            type="text"
            className="form-control"
            value={country}
            onChange={(e) => setCountry(e.target.value)}
          />
        </div>
        <div className="mb-3">
          <label className="form-label">Declared Value (USD)</label>
          <input
            type="number"
            className="form-control"
            value={value}
            onChange={(e) => setValue(e.target.value)}
          />
        </div>

        <button type="button" className="btn btn-secondary me-2" onClick={handleMatch}>
          Find HTS Matches
        </button>

        {matchUpdated && (
        <div className="alert alert-success mt-2" role="alert">
          HTS matches updated.
          </div>
        )}

        {topMatches.length > 0 && (
          <div className="mt-3">
            <label className="form-label">Select HTS Code</label>
            <select
              className="form-select"
              value={selectedHTS}
              onChange={(e) => setSelectedHTS(e.target.value)}
            >
              <option value="">-- Choose a code --</option>
              {topMatches.map((match, index) => (
                <option key={index} value={match.hts_code}>
                  {match.hts_code} - {match.description}
                </option>
              ))}
            </select>
          </div>
        )}

        <button type="submit" className="btn btn-primary mt-3">
          Calculate Tariff
        </button>
      </form>

      {result && (
        <div className="mt-4">
          <h4>Results:</h4>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
