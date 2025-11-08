import { useEffect, useState } from "react";
import "./App.css";

export default function App() {
  const [host, setHost] = useState("");
  const [blocked, setBlocked] = useState([]);

  const refresh = async () => {
    const res = await chrome.runtime.sendMessage({ type: "LIST_BLOCKED" });
    setBlocked(res.blocked ?? []);
  };

  const add = async () => {
    const clean = host
      .trim()
      .replace(/^https?:\/\//, "")
      .replace(/^www\./, "")
      .replace(/\/.*$/, "")
      .toLowerCase();
    if (!clean) return;
    await chrome.runtime.sendMessage({ type: "ADD_BLOCKED", host: clean });
    setHost("");
    refresh();
  };

  const removeHost = async (h) => {
    await chrome.runtime.sendMessage({ type: "REMOVE_BLOCKED", host: h });
    refresh();
  };

  useEffect(() => {
    refresh();
  }, []);

  return (
    <div style={{ width: 340, padding: 12 }}>
      <h3>Touch Grass List</h3>
      <div style={{ display: "flex", gap: 8 }}>
        <input
          placeholder="e.g. youtube.com"
          value={host}
          onChange={(e) => setHost(e.target.value)}
          style={{ flex: 1 }}
        />
        <button onClick={add}>Add</button>
      </div>

      <ul style={{ marginTop: 12, paddingLeft: 16 }}>
        {blocked.map((h) => (
          <li
            key={h}
            style={{ display: "flex", justifyContent: "space-between" }}
          >
            <span>{h}</span>
            <button onClick={() => removeHost(h)}>Remove</button>
          </li>
        ))}
      </ul>
      <p style={{ fontSize: 12, opacity: 0.7 }}>
        The content script will show a centered popup on these domains.
      </p>
    </div>
  );
}
