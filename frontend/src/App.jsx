import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [summary, setSummary] = useState(null);
  const [alerts, setAlerts] = useState([]);
  const [transactions, setTransactions] = useState([]);
  const [transactionsLoading, setTransactionsLoading] = useState(true);
  const [searchId, setSearchId] = useState("");

  useEffect(() => {
    fetch("http://127.0.0.1:8000/summary")
      .then((response) => response.json())
      .then((data) => setSummary(data))
      .catch((error) => console.error("Error fetching summary:", error));

    fetch("http://127.0.0.1:8000/alerts")
      .then((response) => response.json())
      .then((data) => setAlerts(data))
      .catch((error) => console.error("Error fetching alerts:", error));

    fetch("http://127.0.0.1:8000/transactions?limit=5&offset=0&sort_by=amount&order=desc")
      .then((response) => response.json())
      .then((data) => setTransactions(data))
      .catch((error) =>
      console.error("Error fetching transactions:", error))
      .finally(() => setTransactionsLoading(false));
  }, []);


  const searchTransactions = () => {
  setTransactionsLoading(true);

  const url = searchId.trim()
    ? `http://127.0.0.1:8000/transactions?transaction_id=${searchId.trim()}`
    : "http://127.0.0.1:8000/transactions?limit=5&offset=0&sort_by=amount&order=desc";

  fetch(url)
    .then((response) => response.json())
    .then((data) => setTransactions(data))
    .catch((error) =>
      console.error("Error searching transactions:", error)
    )
    .finally(() => setTransactionsLoading(false));
};

  return (
    <div className="app">
      <header className="header">
        <div>
          <h1>Transaction Risk Analyzer</h1>
          <p>Monitor and analyze transaction risk</p>
        </div>

        <div className="status">
          <span className="status-dot"></span>
          API Connected
        </div>
      </header>

      <main>
        <section className="risk-cards">
          <div className="risk-card high">
            <span>HIGH RISK</span>
            <strong>{summary ? summary.high_risk : "..."}</strong>
          </div>

          <div className="risk-card medium">
            <span>MEDIUM RISK</span>
            <strong>{summary ? summary.medium_risk : "..."}</strong>
          </div>

          <div className="risk-card low">
            <span>LOW RISK</span>
            <strong>{summary ? summary.low_risk : "..."}</strong>
          </div>
        </section>

        <section className="dashboard-section">
          <h2>High Risk Transactions</h2>

          {alerts.length === 0 ? (
          <p>No high-risk transactions found.</p>
          ) : (
          <div className="alerts">
            {alerts.map((alert) => (
              <div className="alert-card" key={alert.transaction_id}>
                <div>
                  <strong>{alert.transaction_id}</strong>
                  <span>Risk Score: {alert.risk_score}</span>
                </div>

              <div>
                <strong>{alert.risk_level}</strong>
              </div>

              <div>
                {alert.reasons.map((reason) => (
                  <span className="reason" key={reason}>
                  {reason}
                  </span>
                ))}
              </div>
            </div>
           ))}
          </div>
           )}
        </section>

        <section className="dashboard-section">
  <h2>Transactions</h2>

  <div className="search-box">
    <input
      type="text"
      placeholder="Search Transaction ID (e.g. T007)"
      value={searchId}
      onChange={(event) => setSearchId(event.target.value)}
    />

    <button onClick={searchTransactions}>
      Search
    </button>
  </div>

  {transactionsLoading ? (
    <p>Loading transactions...</p>
  ) : transactions.length === 0 ? (
    <p>No transactions found.</p>
  ) : (
    <div className="table-container">
      <table>
        <thead>
          <tr>
            <th>Transaction ID</th>
            <th>Sender</th>
            <th>Receiver</th>
            <th>Amount</th>
            <th>Country</th>
            <th>Timestamp</th>
          </tr>
        </thead>

        <tbody>
          {transactions.map((transaction) => (
            <tr key={transaction.transaction_id}>
              <td>{transaction.transaction_id}</td>
              <td>{transaction.sender}</td>
              <td>{transaction.receiver}</td>
              <td>₹{transaction.amount.toLocaleString()}</td>
              <td>{transaction.country}</td>
              <td>{transaction.timestamp}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )}
</section>
      </main>
    </div>
  );
}

export default App;