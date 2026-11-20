# GraphSentinel

GraphSentinel is a learning-focused financial transaction network analysis project. It models accounts as nodes and transfers as directed edges, then highlights graph patterns that may warrant further review.

> **Important:** A graph pattern or risk score is not proof of fraud. This starter version uses transparent heuristics, not a trained fraud classifier or a production payment-monitoring system.

## Current features

- Builds a directed account-to-account transaction graph.
- Aggregates repeated transfers between the same pair of accounts.
- Detects short directed cycles (2–4 accounts).
- Identifies high fan-in and fan-out accounts.
- Flags rapid pass-through behaviour using a configurable time window.
- Produces explainable heuristic risk scores.
- Displays summary metrics, alerts and an interactive account network.

## Tech stack

Python, Flask, Pandas, NetworkX, HTML, CSS, JavaScript and Cytoscape.js.

## Run locally

1. Install Python 3.10 or newer.
2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   # Windows PowerShell
   .venv\\Scripts\\Activate.ps1
   # macOS/Linux
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the application:

   ```bash
   python app.py
   ```

5. Open http://127.0.0.1:5000

## Dataset

The included `data/sample_transactions.csv` is a small, hand-crafted synthetic dataset for demonstrating the application. It is not real customer or payment data and should not be used to claim model accuracy.

CSV columns:

| Column | Description |
|---|---|
| transaction_id | Unique transfer identifier |
| sender_id | Source account |
| receiver_id | Destination account |
| amount | Transfer amount |
| timestamp | ISO-8601 timestamp |
| is_suspicious | Synthetic label for future evaluation |

## Project structure

```text
GraphSentinel/
├── app.py
├── graph_engine.py
├── detectors.py
├── scoring.py
├── requirements.txt
├── README.md
├── data/
│   └── sample_transactions.csv
├── templates/
│   └── index.html
└── static/
    ├── css/style.css
    └── js/graph.js
```

## How the risk score works

The current score is a rule-based prioritisation score. Pattern matches add points to involved accounts, capped at 100. It is **not** a calibrated probability. The thresholds and weights are starter heuristics and should be validated against labelled data before making performance claims.

## Planned extensions

- Import a larger synthetic AML dataset such as IBM AMLSim.
- Add time-window-aware cycle and amount-flow analysis.
- Add a PostgreSQL persistence layer and REST endpoints.
- Evaluate detection against labelled data using precision, recall, F1-score and a confusion matrix.
- Add tests and temporal train/test evaluation before introducing machine learning.

## Responsible use

Use synthetic or properly authorised data only. Alerts should support human investigation and should never be treated as automatic evidence of wrongdoing.
