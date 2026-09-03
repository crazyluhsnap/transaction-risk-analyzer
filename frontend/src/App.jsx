import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [summary, setSummary] = useState(null);
  const [alerts, setAlerts] = useState([]);
  const [transactions, setTransactions] = useState([]);
  const [transactionsLoading, setTransactionsLoading] = useState(true);
  const [searchId, setSearchId] = useState("");
  const [currentPage, setCurrentPage] = useState(1);
  const [selectedAnalysis, setSelectedAnalysis] = useState(null);
  const [hasNextPage, setHasNextPage] = useState(false);
  const [riskAnalyses, setRiskAnalyses] = useState({});
  const [selectedCountry, setSelectedCountry] = useState("");
  const [minAmount, setMinAmount] = useState("");

  const PAGE_SIZE = 5;

  const fetchTransactions = (
    page = 1,
    country = selectedCountry,
    amount = minAmount,
  ) => {
    setTransactionsLoading(true);

    const offset = (page - 1) * PAGE_SIZE;

    const params = new URLSearchParams({
      limit: String(PAGE_SIZE + 1),
      offset: String(offset),
      sort_by: "amount",
      order: "desc",
    });

    if (country) {
      params.append("country", country);
    }

    if (amount) {
      params.append("min_amount", amount);
    }

    fetch(`http://127.0.0.1:8000/transactions?${params.toString()}`)
      .then((response) => response.json())
      .then((data) => {
        const pageTransactions = data.slice(0, PAGE_SIZE);

        setHasNextPage(data.length > PAGE_SIZE);
        setTransactions(pageTransactions);
        setCurrentPage(page);
        setSelectedAnalysis(null);

        return Promise.all(
          pageTransactions.map((transaction) =>
            fetch(
              `http://127.0.0.1:8000/analyze/${transaction.transaction_id}`,
              {
                method: "POST",
              },
            ).then((response) => response.json()),
          ),
        );
      })
      .then((analyses) => {
        const analysisMap = {};

        analyses.forEach((analysis) => {
          analysisMap[analysis.transaction_id] = analysis;
        });

        setRiskAnalyses((previous) => ({
          ...previous,
          ...analysisMap,
        }));
      })
      .catch((error) => console.error("Error fetching transactions:", error))
      .finally(() => setTransactionsLoading(false));
  };

  useEffect(() => {
    fetch("http://127.0.0.1:8000/summary")
      .then((response) => response.json())
      .then((data) => setSummary(data))
      .catch((error) => console.error("Error fetching summary:", error));

    fetch("http://127.0.0.1:8000/alerts")
      .then((response) => response.json())
      .then((data) => setAlerts(data))
      .catch((error) => console.error("Error fetching alerts:", error));

    fetchTransactions(1);
  }, []);

  const searchTransactions = () => {
    if (searchId.trim()) {
      setTransactionsLoading(true);
      setCurrentPage(1);
      setSelectedAnalysis(null);

      const transactionId = searchId.trim();

      fetch(
        `http://127.0.0.1:8000/transactions?transaction_id=${transactionId}`,
      )
        .then((response) => response.json())
        .then((data) => {
          setTransactions(data);

          if (data.length === 0) {
            return null;
          }

          const foundTransactionId = data[0].transaction_id;

          return fetch(`http://127.0.0.1:8000/analyze/${foundTransactionId}`, {
            method: "POST",
          }).then((response) => response.json());
        })
        .then((analysis) => {
          if (analysis) {
            setRiskAnalyses((previous) => ({
              ...previous,
              [analysis.transaction_id]: analysis,
            }));
          }
        })
        .catch((error) => console.error("Error searching transactions:", error))
        .finally(() => setTransactionsLoading(false));

      return;
    }

    fetchTransactions(1);
  };

  const resetTransactions = () => {
    setSearchId("");
    setSelectedCountry("");
    setMinAmount("");
    fetchTransactions(1, "", "");
  };

  const analyzeTransaction = (transactionId) => {
    fetch(`http://127.0.0.1:8000/analyze/${transactionId}`, {
      method: "POST",
    })
      .then((response) => response.json())
      .then((data) => {
        setSelectedAnalysis(data);
      })
      .catch((error) => console.error("Error analyzing transaction:", error));
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

            <select
              value={selectedCountry}
              onChange={(event) => {
                setSelectedCountry(event.target.value);
                setSearchId("");
              }}
            >
              <option value="">All Countries</option>
              <option value="IN">India (IN)</option>
              <option value="US">United States (US)</option>
            </select>

            <input
              type="number"
              placeholder="Min Amount"
              value={minAmount}
              onChange={(event) => setMinAmount(event.target.value)}
              min="0"
            />

            <button onClick={searchTransactions}>Search</button>

            <button onClick={resetTransactions}>Reset</button>
          </div>

          {transactionsLoading ? (
            <p>Loading transactions...</p>
          ) : transactions.length === 0 ? (
            <p>No transactions found.</p>
          ) : (
            <>
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
                      <th>Risk Level</th>
                      <th>Action</th>
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

                        <td>
                          {riskAnalyses[transaction.transaction_id] ? (
                            <span
                              className={`table-risk-badge ${riskAnalyses[
                                transaction.transaction_id
                              ].risk_level.toLowerCase()}`}
                            >
                              {
                                riskAnalyses[transaction.transaction_id]
                                  .risk_level
                              }
                            </span>
                          ) : (
                            <span>Loading...</span>
                          )}
                        </td>

                        <td>
                          <button
                            className="risk-button"
                            onClick={() =>
                              analyzeTransaction(transaction.transaction_id)
                            }
                          >
                            View Risk
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              <div className="pagination">
                <button
                  onClick={() => fetchTransactions(currentPage - 1)}
                  disabled={currentPage === 1}
                >
                  ← Previous
                </button>

                <span>Page {currentPage}</span>

                <button
                  onClick={() => fetchTransactions(currentPage + 1)}
                  disabled={!hasNextPage}
                >
                  Next →
                </button>
              </div>

              {selectedAnalysis && (
                <div className="risk-modal-overlay">
                  <div className="risk-modal">
                    <button
                      className="close-button"
                      onClick={() => setSelectedAnalysis(null)}
                    >
                      ×
                    </button>

                    <h3>Risk Analysis - {selectedAnalysis.transaction_id}</h3>

                    <div className="risk-detail-grid">
                      <div>
                        <span>Risk Score</span>
                        <strong>{selectedAnalysis.risk_score}</strong>
                      </div>

                      <div>
                        <span>Risk Level</span>
                        <strong
                          className={`risk-level ${selectedAnalysis.risk_level.toLowerCase()}`}
                        >
                          {selectedAnalysis.risk_level}
                        </strong>
                      </div>
                    </div>

                    <div className="risk-reasons">
                      <h4>Reasons</h4>

                      {selectedAnalysis.reasons.length === 0 ? (
                        <p>No risk indicators detected.</p>
                      ) : (
                        <ul>
                          {selectedAnalysis.reasons.map((reason) => (
                            <li key={reason}>{reason}</li>
                          ))}
                        </ul>
                      )}
                    </div>

                    <button
                      className="modal-close-button"
                      onClick={() => setSelectedAnalysis(null)}
                    >
                      Close
                    </button>
                  </div>
                </div>
              )}
            </>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
