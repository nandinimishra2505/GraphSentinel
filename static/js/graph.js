async function loadGraph() {
  const response = await fetch("/api/graph");
  const elements = await response.json();

  const cy = cytoscape({
    container: document.getElementById("network"),
    elements: [...elements.nodes, ...elements.edges],
    layout: { name: "cose", animate: false, padding: 35 },
    style: [
      { selector: "node", style: {
        "label": "data(label)", "font-size": 10, "color": "#26354b",
        "text-valign": "bottom", "text-margin-y": 7,
        "width": 24, "height": 24, "border-width": 2, "border-color": "#ffffff",
        "background-color": "#8da3bd"
      }},
      { selector: 'node[risk = "Medium"]', style: { "background-color": "#e5a63b" }},
      { selector: 'node[risk = "High"]', style: { "background-color": "#d65b62" }},
      { selector: "edge", style: {
        "width": 1.5, "line-color": "#b9c4d2", "target-arrow-color": "#8b9bb0",
        "target-arrow-shape": "triangle", "curve-style": "bezier",
        "arrow-scale": 0.8, "label": "data(count)", "font-size": 8,
        "color": "#7b8798", "text-rotation": "autorotate"
      }},
      { selector: ":selected", style: { "border-width": 4, "border-color": "#284e80" }}
    ]
  });

  cy.on("tap", "node", event => {
    const node = event.target.data();
    document.getElementById("node-info").textContent =
      `Account ${node.id} · Heuristic risk score: ${node.score}/100 · Risk level: ${node.risk}`;
  });
}
loadGraph().catch(error => {
  document.getElementById("node-info").textContent = "Could not load graph data: " + error.message;
});
