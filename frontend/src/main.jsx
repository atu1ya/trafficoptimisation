import React, { useMemo, useState } from 'react';
import { createRoot } from 'react-dom/client';

const API = import.meta.env.VITE_API_BASE || 'http://localhost:8000';

function App() {
  const [start, setStart] = useState({ lat: -31.980, lon: 115.860 });
  const [end, setEnd] = useState({ lat: -32.040, lon: 115.790 });
  const [scenario, setScenario] = useState('night');
  const [controller, setController] = useState('max_pressure');
  const [compare, setCompare] = useState(true);
  const [frames, setFrames] = useState([]);
  const [summary, setSummary] = useState(null);
  const [running, setRunning] = useState(false);

  const latest = useMemo(() => (frames.length ? frames[frames.length - 1] : null), [frames]);

  const onRun = async () => {
    setRunning(true);
    setFrames([]);
    setSummary(null);
    const ws = new WebSocket(`${API.replace('http', 'ws')}/ws/simulate`);
    ws.onopen = () => ws.send(JSON.stringify({ scenario, controller, compare, seed: 42, steps: 80 }));
    ws.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      if (msg.type === 'frame') setFrames((p) => [...p, msg.data]);
      if (msg.type === 'summary') {
        setSummary(msg.data);
        setRunning(false);
        ws.close();
      }
    };
  };

  return (
    <div style={{ fontFamily: 'Arial', margin: 20 }}>
      <h1>Perth Greenwave Optimisation Demo</h1>
      <p>BBox includes Canning Vale, Rossmoyne, Willetton, Bicton, Mosman Park, Nedlands, and Churchlands.</p>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3,1fr)', gap: 12 }}>
        <label>Start lat <input value={start.lat} onChange={(e) => setStart({ ...start, lat: Number(e.target.value) })} /></label>
        <label>Start lon <input value={start.lon} onChange={(e) => setStart({ ...start, lon: Number(e.target.value) })} /></label>
        <label>Scenario
          <select value={scenario} onChange={(e) => setScenario(e.target.value)}>
            <option value="night">Night</option><option value="off_peak_morning">Off peak morning</option>
            <option value="afternoon_medium">Afternoon medium</option><option value="peak_rush_hour">Peak rush hour</option>
            <option value="incident_mode">Incident mode</option>
          </select>
        </label>
        <label>End lat <input value={end.lat} onChange={(e) => setEnd({ ...end, lat: Number(e.target.value) })} /></label>
        <label>End lon <input value={end.lon} onChange={(e) => setEnd({ ...end, lon: Number(e.target.value) })} /></label>
        <label>Controller
          <select value={controller} onChange={(e) => setController(e.target.value)}>
            <option value="night_fixed">Night fixed</option><option value="scenario_fixed">Scenario fixed</option>
            <option value="max_pressure">Max pressure</option><option value="green_wave">Green wave</option>
          </select>
        </label>
      </div>
      <label><input type="checkbox" checked={compare} onChange={(e) => setCompare(e.target.checked)} /> Compare baseline vs optimised</label>
      <br />
      <button onClick={onRun} disabled={running} style={{ marginTop: 12 }}>Run simulation</button>
      {latest && <p>Step {latest.step} | Delay {latest.network_delay_s.toFixed(1)}s | Throughput {latest.throughput}</p>}
      {summary && (
        <div>
          <h3>Before vs After</h3>
          <pre>{JSON.stringify(summary, null, 2)}</pre>
          <h3>Why improved</h3>
          <ul>{summary.explainability.map((line, i) => <li key={i}>{line}</li>)}</ul>
        </div>
      )}
    </div>
  );
}

createRoot(document.getElementById('root')).render(<App />);
