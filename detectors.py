from collections import defaultdict
import networkx as nx
import pandas as pd

def detect_patterns(transactions, graph, rapid_window_minutes=60):
    """
    Heuristic indicators:
    - directed cycles of length 2-4
    - fan-in / fan-out accounts
    - rapid pass-through (inflow followed by outflow within a time window)

    These are investigation leads, not proof of fraud.
    """
    alerts = []
    seen_cycles = set()

    # Bounded cycle search keeps the starter project understandable.
    for cycle in nx.simple_cycles(graph):
        if 2 <= len(cycle) <= 4:
            canonical = tuple(sorted(cycle))
            if canonical in seen_cycles:
                continue
            seen_cycles.add(canonical)
            alerts.append({
                "pattern": "Transaction cycle",
                "severity": "Medium",
                "accounts": cycle,
                "explanation": f"Funds can circulate through a directed cycle involving {len(cycle)} accounts."
            })

    # Fan-in and fan-out based on distinct counterparties.
    for account in graph.nodes:
        indegree = graph.in_degree(account)
        outdegree = graph.out_degree(account)
        if indegree >= 4:
            alerts.append({
                "pattern": "Fan-in",
                "severity": "Medium",
                "accounts": [account] + list(graph.predecessors(account)),
                "explanation": f"{account} receives transfers from {indegree} distinct accounts."
            })
        if outdegree >= 4:
            alerts.append({
                "pattern": "Fan-out",
                "severity": "Medium",
                "accounts": [account] + list(graph.successors(account)),
                "explanation": f"{account} sends transfers to {outdegree} distinct accounts."
            })

    # Rapid pass-through: an account receives and sends funds close in time.
    ordered = transactions.sort_values("timestamp")
    grouped_in = defaultdict(list)
    grouped_out = defaultdict(list)
    for row in ordered.itertuples(index=False):
        grouped_in[str(row.receiver_id)].append(row.timestamp)
        grouped_out[str(row.sender_id)].append(row.timestamp)

    window = pd.Timedelta(minutes=rapid_window_minutes)
    for account in graph.nodes:
        inflows = grouped_in[account]
        outflows = grouped_out[account]
        if not inflows or not outflows:
            continue
        rapid = False
        for incoming in inflows:
            if any(pd.Timedelta(0) <= outgoing - incoming <= window for outgoing in outflows):
                rapid = True
                break
        if rapid:
            alerts.append({
                "pattern": "Rapid pass-through",
                "severity": "High",
                "accounts": [account],
                "explanation": f"{account} receives funds and sends funds within {rapid_window_minutes} minutes."
            })

    # Stable IDs make the API output easier to inspect.
    for index, alert in enumerate(alerts, start=1):
        alert["alert_id"] = f"GS-{index:04d}"
        alert["accounts"] = list(dict.fromkeys(alert["accounts"]))
    return alerts
