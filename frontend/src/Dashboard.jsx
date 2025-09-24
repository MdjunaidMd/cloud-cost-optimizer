import React, { useState, useEffect } from "react";
import { getInstances, getRecommendations, getAudit } from "./api";
import API_BASE from "./config";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  BarChart,
  Bar,
  ResponsiveContainer,
  LabelList,
  Cell,
} from "recharts";

export default function Dashboard() {
  const [instances, setInstances] = useState([]);
  const [recs, setRecs] = useState([]);
  const [audit, setAudit] = useState([]);

  const palette = {
    coral: "#F09B93",
    rose: "#EBD6D7",
    cream: "#F9EBD9",
    yellow: "#E9DD8A",
    teal: "#439093",
    textDark: "#1e293b",
  };

  // Card style
  const cardStyle = {
    background: "#ffffffd9",
    padding: 20,
    borderRadius: "12px",
    boxShadow: "0 4px 15px rgba(0,0,0,0.15)",
    width: "100%",
    marginBottom: "20px",
  };

  // 🔹 Instances
  useEffect(() => {
    getInstances().then(setInstances);
    const id = setInterval(() => getInstances().then(setInstances), 3000);
    return () => clearInterval(id);
  }, []);

  // 🔹 Recommendations
  useEffect(() => {
    getRecommendations().then(setRecs);
    const id = setInterval(() => getRecommendations().then(setRecs), 3000);
    return () => clearInterval(id);
  }, []);

  // 🔹 Audit
  useEffect(() => {
    getAudit().then(setAudit);
    const id = setInterval(() => getAudit().then(setAudit), 3000);
    return () => clearInterval(id);
  }, []);

  // 🔹 Button Actions → Call backend
  const makeIdle = async (id) => {
    await fetch(`${API_BASE}/make_idle/${id}`, { method: "POST" });
    getInstances().then(setInstances);
  };

  const makeBusy = async (id) => {
    await fetch(`${API_BASE}/make_busy/${id}`, { method: "POST" });
    getInstances().then(setInstances);
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        width: "100vw",
        background: `linear-gradient(135deg, ${palette.cream}, ${palette.yellow}, ${palette.teal})`,
        fontFamily: "Segoe UI, Arial",
        padding: "20px",
        boxSizing: "border-box",
      }}
    >
      <h1 style={{ color: palette.teal, marginBottom: 20 }}>
        ☁️ Smart Cloud Cost Optimizer
      </h1>

      {/* Instances */}
      <div style={cardStyle}>
        <h2 style={{ color: palette.teal }}>Instances</h2>
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead style={{ background: palette.teal, color: "white" }}>
            <tr>
              <th style={{ padding: 10 }}>ID</th>
              <th style={{ padding: 10 }}>Name</th>
              <th style={{ padding: 10 }}>CPU %</th>
              <th style={{ padding: 10 }}>Status</th>
              <th style={{ padding: 10 }}>Cost</th>
              <th style={{ padding: 10 }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {instances.map((i, idx) => (
              <tr
                key={idx}
                style={{
                  background: idx % 2 === 0 ? palette.rose : palette.cream,
                  textAlign: "center",
                }}
              >
                <td style={{ padding: "10px", color: palette.textDark }}>{i.id}</td>
                <td style={{ padding: "10px", color: palette.textDark }}>{i.name}</td>
                <td style={{ padding: "10px", color: palette.textDark }}>{i.cpu}</td>
                <td
                  style={{
                    padding: "10px",
                    color: i.status === "idle" ? "red" : "green",
                    fontWeight: "bold",
                  }}
                >
                  {i.status}
                </td>
                <td style={{ padding: 10, color: palette.textDark }}>${i.cost}</td>
                <td>
                  <button
                    style={{
                      margin: "0 5px",
                      padding: "5px 12px",
                      background: palette.teal,
                      color: "white",
                      border: "none",
                      borderRadius: "6px",
                      cursor: "pointer",
                    }}
                    onClick={() => makeIdle(i.id)}
                  >
                    Make Idle
                  </button>
                  <button
                    style={{
                      margin: "0 5px",
                      padding: "5px 12px",
                      background: palette.teal,
                      color: "white",
                      border: "none",
                      borderRadius: "6px",
                      cursor: "pointer",
                    }}
                    onClick={() => makeBusy(i.id)}
                  >
                    Make Busy
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Recommendations */}
      <div style={cardStyle}>
        <h2 style={{ color: palette.teal }}>💡 Recommendations</h2>
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead style={{ background: palette.teal, color: "white" }}>
            <tr>
              <th style={{ padding: 10 }}>Instance</th>
              <th style={{ padding: 10 }}>Recommendation</th>
              <th style={{ padding: 10 }}>Potential Saving</th>
            </tr>
          </thead>
          <tbody>
            {recs.map((r, idx) => (
              <tr
                key={idx}
                style={{
                  background: idx % 2 === 0 ? palette.rose : palette.cream,
                  textAlign: "center",
                }}
              >
                <td style={{ padding: 10, color: palette.textDark }}>{r.name}</td>
                <td style={{ padding: 10, color: palette.textDark }}>{r.recommendation}</td>
                <td style={{ padding: 10, color: "green", fontWeight: "bold" }}>
                  ${r.saving}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Audit Log */}
      <div style={{ ...cardStyle }}>
        <h2 style={{ color: palette.teal }}>📝 Action Audit (recent)</h2>
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead style={{ background: palette.teal, color: "white" }}>
            <tr>
              <th style={{ padding: 8 }}>When</th>
              <th>Instance</th>
              <th>Action</th>
              <th>Old → New</th>
            </tr>
          </thead>
          <tbody>
            {audit.map((a, idx) => (
              <tr
                key={idx}
                style={{
                  background: idx % 2 === 0 ? palette.rose : palette.cream,
                }}
              >
                <td style={{ padding: 8, color: "#1e293b" }}>
                  {new Date(a.timestamp).toLocaleString()}
                </td>
                <td style={{ padding: 8, color: "#1e293b" }}>{a.instance_id}</td>
                <td style={{ padding: 8, color: "#1e293b" }}>{a.action}</td>
                <td style={{ padding: 8, color: "#1e293b" }}>
                  {`${a.old_cpu}/${a.old_status} → ${a.new_cpu}/${a.new_status}`}
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {/* ✅ Download Audit Log */}
        <button
          onClick={() => window.open(`${API_BASE}/export/audit`, "_blank")}
          style={{
            marginTop: 12,
            padding: "6px 10px",
            borderRadius: 6,
            background: palette.teal,
            color: "#fff",
            border: "none",
            cursor: "pointer",
          }}
        >
          Export Audit CSV
        </button>
      </div>

      {/* Charts */}
      <div style={{ display: "flex", gap: "20px", flexWrap: "wrap" }}>
        {/* CPU Usage */}
        <div style={{ ...cardStyle, flex: 1 }}>
          <h2 style={{ color: palette.teal }}>📈 CPU Usage Trend</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={instances}>
              <CartesianGrid strokeDasharray="3 3" stroke="#ccc" />
              <XAxis dataKey="name" stroke={palette.teal} />
              <YAxis stroke={palette.teal} />
              <Tooltip
                contentStyle={{
                  backgroundColor: "#ffffff",
                  border: "1px solid #439093",
                  borderRadius: "6px",
                  color: "#000000",
                }}
                itemStyle={{ color: "#000000", fontWeight: "bold" }}
                labelStyle={{ color: "#439093", fontWeight: "bold" }}
              />
              <Legend />
              <Line
                type="monotone"
                dataKey="cpu"
                stroke={palette.coral}
                strokeWidth={3}
                dot={{ r: 6, fill: palette.teal, stroke: palette.coral }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Cost Analysis */}
        <div style={{ ...cardStyle, flex: 1 }}>
          <h2 style={{ color: palette.teal }}>💰 Server Cost Analysis</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={instances}>
              <CartesianGrid strokeDasharray="3 3" stroke="#ccc" />
              <XAxis dataKey="name" stroke={palette.teal} />
              <YAxis stroke={palette.teal} />
              <Tooltip
                contentStyle={{
                  backgroundColor: "#ffffff",
                  border: "1px solid #439093",
                  borderRadius: "6px",
                  color: "#000000",
                }}
                itemStyle={{ color: "#000000", fontWeight: "bold" }}
                labelStyle={{ color: "#439093", fontWeight: "bold" }}
              />
              <Legend />
              <Bar dataKey="cost">
                <LabelList
                  dataKey="cost"
                  position="top"
                  formatter={(val) => `$${val}`}
                  fill="#000"
                  fontSize={14}
                />
                {instances.map((entry, index) => {
                  const colors = [palette.coral, palette.rose, palette.teal];
                  return (
                    <Cell
                      key={`cell-${index}`}
                      fill={colors[index % colors.length]}
                    />
                  );
                })}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
