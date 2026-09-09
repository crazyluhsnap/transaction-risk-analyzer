# Transaction Risk Analyzer

A full-stack transaction monitoring and risk analysis application that analyzes financial transactions, identifies suspicious patterns, and presents risk information through an interactive dashboard.

## Problem

Financial transaction datasets can contain suspicious activity such as unusually large transactions, high transaction frequency, high transaction velocity, and circular transaction patterns.

Manually identifying these patterns across a transaction dataset is difficult and time-consuming.

## Solution

Transaction Risk Analyzer provides:

- Transaction-level risk analysis
- Account behavior analysis
- Network-based transaction analysis
- Risk score and risk level calculation
- High-risk transaction alerts
- Transaction search and filtering
- Pagination and sorting
- Interactive risk-analysis details
- Responsive dashboard for desktop and mobile

The backend performs the analysis and exposes it through a FastAPI REST API, while the React frontend provides the dashboard.

---

## Features

### Transaction Monitoring

- View transactions in a tabular dashboard
- Search transactions by Transaction ID
- Filter by country
- Filter by minimum transaction amount
- Filter by risk level
- Filter by minimum risk score
- Sort transactions by supported fields
- Paginate transaction results

### Risk Analysis

Each transaction can be analyzed using multiple signals:

- Transaction-level indicators
- Account-level behavior
- Network-level transaction relationships

The final analysis provides:

- Risk score
- Risk level
- Risk reasons

Risk levels currently include:

- LOW
- MEDIUM
- HIGH

### Network Analysis

The backend uses NetworkX to analyze relationships between transaction participants and detect suspicious network patterns such as rapid circular transaction activity.

### Dashboard

The dashboard provides:

- Risk summary cards
- High-risk transaction alerts
- Transaction table
- Risk level indicators
- Interactive risk-analysis modal
- Loading and error states
- Responsive mobile layout

---

## Architecture

React Frontend
        |
        | HTTP / REST API
        v
FastAPI Backend
        |
        v
Risk Analysis
        |
        +-----------------------+
        |                       |
        v                       v
Transaction Analysis      Account Analysis
        |                       |
        +-----------+-----------+
                    |
                    v
             Network Analysis
                    |
                    v
             Risk Aggregation
                    |
                    v
          Final Risk Score
                    |
                    v
          Risk Level + Reasons


---

## Risk Analysis Flow

Transaction
    |
    v
Transaction-level analysis
    |
    v
Account-level analysis
    |
    v
Network analysis
    |
    v
Risk aggregation
    |
    v
Final risk score
    |
    v
Risk level + reasons

The backend combines transaction, account, and network analysis before producing the final risk result.

---

## Example

For example, a transaction may be identified as high risk because of multiple indicators:

Transaction: T007

Risk Score: 70
Risk Level: HIGH

Reasons:
- Large transaction
- Rapid circular transaction pattern

The dashboard exposes these details through the View Risk action.

---

## Tech Stack

### Backend

- Python
- FastAPI
- Pandas
- NetworkX
- Pydantic
- Uvicorn
- Pytest

### Frontend

- React
- Vite
- JavaScript
- CSS
- Native Fetch API

### Data

- CSV transaction dataset

### Development

- Git
- GitHub
- Python virtual environment (venv)

---


## Backend Setup

### 1. Clone the repository

git clone <repository-url>
cd transaction-risk-analyzer

### 2. Create a virtual environment

For Windows PowerShell:

python -m venv venv

Activate it:

.\venv\Scripts\Activate.ps1

### 3. Install backend dependencies

pip install -r requirements.txt

### 4. Start the backend

uvicorn app.main:app --reload

The API will be available at:

http://127.0.0.1:8000

FastAPI's interactive API documentation is available at:

http://127.0.0.1:8000/docs

---

## Frontend Setup

Open another terminal.

cd frontend
npm install

Create the environment file from the example:

Copy-Item .env.example .env

The default configuration is:

VITE_API_URL=http://127.0.0.1:8000

Start the frontend:

npm run dev

The dashboard will be available at:

http://localhost:5173

---

## Running Tests

Backend tests are written using Pytest.

From the project root:

pytest

The test suite covers areas including:

- API endpoints
- Transaction filtering
- Pagination
- Sorting
- Parameter validation
- Error handling
- Risk analysis
- Risk filtering
- API response models
- OpenAPI documentation

---

## API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | / | API information |
| GET | /health | Health check |
| GET | /transactions | Retrieve and filter transactions |
| GET | /transactions/{transaction_id} | Retrieve a specific transaction |
| GET | /alerts | Retrieve high-risk alerts |
| GET | /summary | Retrieve risk summary |
| POST | /analyze/{transaction_id} | Analyze transaction risk |

### Transaction Filtering

The /transactions endpoint supports parameters including:

- country
- sender
- min_amount
- risk_level
- min_risk_score
- limit
- offset
- sort_by
- order
- transaction_id

Example:

GET /transactions?risk_level=HIGH

Another example:

GET /transactions?min_risk_score=50

---

## Current Dataset Summary

The current transaction dataset contains:

- 15 transactions
- 3 high-risk transactions
- 5 medium-risk transactions
- 7 low-risk transactions

---

## Testing Philosophy

Development followed a test-first, incremental workflow:

Write test
    |
    v
Run test and observe failure
    |
    v
Implement smallest change
    |
    v
Run full test suite
    |
    v
Commit working change

This helped keep backend functionality stable while features were added incrementally.

---

## Future Improvements

Potential future improvements include:

- Persistent database storage
- Authentication and authorization
- Larger transaction datasets
- Real-time transaction monitoring
- Configurable risk rules
- Advanced graph visualizations
- Production deployment
- More advanced anomaly detection
- Automated alert notifications

---

## Status

The project currently includes a functional FastAPI backend and React dashboard with:

- Transaction monitoring
- Risk analysis
- Account analysis
- Network analysis
- Risk scoring
- High-risk alerts
- Transaction filtering
- Search
- Pagination
- Sorting
- Interactive risk-analysis modal
- Loading and error states
- Responsive desktop and mobile UI
``