from collections import defaultdict

def score_accounts(graph, patterns):
    """Transparent heuristic score; not a trained machine-learning probability."""
    points = defaultdict(int)
    reasons = defaultdict(list)

    for alert in patterns:
        weight = 35 if alert["severity"] == "High" else 20
        for account in alert["accounts"]:
            points[account] += weight
            reasons[account].append(alert["pattern"])

    results = []
    for account in graph.nodes:
        score = min(points[account], 100)
        level = "High" if score >= 60 else "Medium" if score >= 20 else "Low"
        results.append({
            "account_id": account,
            "risk_score": score,
            "risk_level": level,
            "signals": sorted(set(reasons[account]))
        })

    return sorted(results, key=lambda item: item["risk_score"], reverse=True)
