import { useState } from "react";
import Editor from "@monaco-editor/react";
import "./App.css";

export default function App() {
  const [sql, setSql] = useState("select * from users");
  const [fixedSql, setFixedSql] = useState("");
  const [violations, setViolations] = useState([]);
  const [dialect, setDialect] = useState("postgres");
  const [loading, setLoading] = useState(false);
  const SUPPORTED_DIALECTS = [
    "ansi",
    "athena",
    "bigquery",
    "clickhouse",
    "databricks",
    "db2",
    "duckdb",
    "exasol",
    "greenplum",
    "hive",
    "materialize",
    "mysql",
    "oracle",
    "postgres",
    "redshift",
    "snowflake",
    "soql",
    "sparksql",
    "sqlite",
    "teradata",
    "tsql",
    "vertica",
  ];

  const lintSql = async () => {
    setLoading(true);
    setViolations([]);
    setFixedSql("");

    try {
      const res = await fetch("http://localhost:8000/lint", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ sql, dialect, fix: true }),
      });

      const data = await res.json();
      setViolations(data.violations || []);
      setFixedSql(data.fixed_sql || "");
    } catch (err) {
      console.error("Failed to connect to backend", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <h1 className="title">SQLFluff Web Linter</h1>

      <div className="toolbar">
        <select
          value={dialect}
          onChange={(e) => setDialect(e.target.value)}
          className="select"
        >
          {SUPPORTED_DIALECTS.map((d) => (
            <option key={d} value={d}>
              {/* Capitalizes the first letter for the UI */}
              {d.charAt(0).toUpperCase() + d.slice(1)}
            </option>
          ))}
        </select>

        <button onClick={lintSql} disabled={loading} className="button">
          {loading ? "Linting…" : "Lint & Fix"}
        </button>
      </div>

      <div className="editors">
        <div className="editor-pane">
          <h2 className="subtitle">Input SQL</h2>
          <Editor
            height="300px"
            language="sql"
            theme="vs-light"
            value={sql}
            onChange={(v) => setSql(v || "")}
            options={{
              minimap: { enabled: false },
              wordWrap: "on",
              scrollBeyondLastLine: false,
            }}
          />
        </div>

        <div className="editor-pane">
          <h2 className="subtitle">Fixed SQL</h2>
          <Editor
            height="300px"
            language="sql"
            value={fixedSql}
            options={{
              readOnly: true,
              minimap: { enabled: false },
              wordWrap: "on",
              scrollBeyondLastLine: false,
            }}
          />
        </div>
      </div>

      <div className="violations-section">
        <h2 className="subtitle">Violations</h2>
        {violations.length === 0 ? (
          <p style={{ color: "#16a34a" }}>No violations 🎉</p>
        ) : (
          <ul className="violations-list">
            {violations.map((v, i) => (
              <li key={i} className="violation-item">
                <strong>{v.code}</strong> — {v.description}
                {v.line != null && (
                  <span className="violation-meta">
                    (Line {v.line}, Col {v.position})
                  </span>
                )}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
