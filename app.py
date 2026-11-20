from flask import Flask, render_template, jsonify, request
from pathlib import Path
import pandas as pd

from graph_engine import build_transaction_graph, graph_summary, graph_payload
from detectors import detect_patterns
from scoring import score_accounts

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "sample_transactions.csv"

app = Flask(__name__)

def load_data():
    df = pd.read_csv(DATA_PATH)
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    return df

def analyse():
    transactions = load_data()
    graph = build_transaction_graph(transactions)
    patterns = detect_patterns(transactions, graph)
    scores = score_accounts(graph, patterns)
    return transactions, graph, patterns, scores

@app.route("/")
def index():
    transactions, graph, patterns, scores = analyse()
    summary = graph_summary(transactions, graph, patterns, scores)
    return render_template(
        "index.html",
        summary=summary,
        alerts=patterns[:20],
        scores=scores[:15]
    )

@app.route("/api/graph")
def api_graph():
    transactions, graph, patterns, scores = analyse()
    return jsonify(graph_payload(graph, scores, patterns))

@app.route("/api/alerts")
def api_alerts():
    _, _, patterns, _ = analyse()
    return jsonify(patterns)

@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "GraphSentinel"})

if __name__ == "__main__":
    app.run(debug=True)
