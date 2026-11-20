import networkx as nx

REQUIRED_COLUMNS = {"transaction_id", "sender_id", "receiver_id", "amount", "timestamp"}

def build_transaction_graph(transactions):
    """Build a directed account graph. Each edge stores its transaction records."""
    missing = REQUIRED_COLUMNS - set(transactions.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    graph = nx.DiGraph()
    for row in transactions.itertuples(index=False):
        sender = str(row.sender_id)
        receiver = str(row.receiver_id)
        if sender == receiver:
            continue

        if not graph.has_node(sender):
            graph.add_node(sender)
        if not graph.has_node(receiver):
            graph.add_node(receiver)

        if graph.has_edge(sender, receiver):
            edge = graph[sender][receiver]
            edge["transaction_count"] += 1
            edge["total_amount"] += float(row.amount)
            edge["transactions"].append(str(row.transaction_id))
        else:
            graph.add_edge(
                sender, receiver,
                transaction_count=1,
                total_amount=float(row.amount),
                transactions=[str(row.transaction_id)]
            )
    return graph

def graph_summary(transactions, graph, patterns, scores):
    return {
        "transactions": int(len(transactions)),
        "accounts": int(graph.number_of_nodes()),
        "connections": int(graph.number_of_edges()),
        "alerts": int(len(patterns)),
        "high_risk": int(sum(1 for item in scores if item["risk_level"] == "High"))
    }

def graph_payload(graph, scores, patterns):
    score_map = {item["account_id"]: item for item in scores}
    flagged = {account for alert in patterns for account in alert["accounts"]}
    nodes = []
    for node in graph.nodes:
        item = score_map.get(node, {})
        nodes.append({
            "data": {
                "id": node,
                "label": node,
                "risk": item.get("risk_level", "Low"),
                "score": item.get("risk_score", 0),
                "flagged": node in flagged
            }
        })

    edges = []
    for source, target, attrs in graph.edges(data=True):
        edges.append({
            "data": {
                "id": f"{source}-{target}",
                "source": source,
                "target": target,
                "count": attrs["transaction_count"],
                "amount": round(attrs["total_amount"], 2)
            }
        })
    return {"nodes": nodes, "edges": edges}
