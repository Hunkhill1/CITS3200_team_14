import networkx as nx
import matplotlib.pyplot as plt
import sqlite3

def highlight_path(G, selected_unit):
    # Perform a BFS from the selected_unit to find the path to prerequisites
    visited = set()
    queue = [selected_unit]
    path_nodes = []

    while queue:
        current_unit = queue.pop(0)
        if current_unit not in visited:
            visited.add(current_unit)
            path_nodes.append(current_unit)
            queue.extend(G.predecessors(current_unit))

    return path_nodes

# Connect to the SQLite database
conn = sqlite3.connect('CITS3200_team_14/database/degree_database.db')
cursor = conn.cursor()

# Query the database to get unit relationships
cursor.execute("SELECT unit_code, pre_requisite FROM UnitRelationship")
relationships = cursor.fetchall()

# Create a directed graph
G = nx.DiGraph()

# Add nodes (units) and their semester information to the graph
for unit_code, _, semester in cursor.execute("SELECT code, name, semester FROM Unit"):
    G.add_node(unit_code, label=f"{unit_code}\n {semester}")

# Add edges (prerequisites) to the graph
for unit_code, pre_requisite in relationships:
    G.add_edge(pre_requisite, unit_code)

# Close the database connection
conn.close()

# Choose a unit to highlight its path
selected_unit = 'ENSC2003'
path_nodes = highlight_path(G, selected_unit)

# Draw the DAG with highlighted path
pos = nx.drawing.layout.shell_layout(G, nlist=[list(G.nodes())])

plt.figure(figsize=(10, 6))

# Draw all nodes and edges
nx.draw_networkx(
    G,
    pos,
    labels=nx.get_node_attributes(G, "label"),
    with_labels=True,
    node_size=1500,
    font_size=10,
    font_color="black",
    font_weight="bold",
    arrowsize=20,
    linewidths=1,
    edge_color="gray",
    edgecolors="black",
)

# Highlight the path nodes with a different color
nx.draw_networkx_nodes(
    G,
    pos,
    nodelist=path_nodes,
    node_size=1500,
    node_color="gold",
)

plt.title(f"Prerequisite Path for Unit '{selected_unit}'")
plt.axis("off")
plt.tight_layout()
plt.show()
