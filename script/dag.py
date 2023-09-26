import networkx as nx
import matplotlib.pyplot as plt
import sqlite3
import constants as constants


def create_unit_graph():
    """ Create a directed acyclic graph (DAG) of units and their prerequisites.

    Returns:
        DiGraph:  A directed acyclic graph (DAG) of units and their prerequisites.
    """    
    conn = sqlite3.connect(constants.degree_db_address)
    cursor = conn.cursor()

    cursor.execute("SELECT unit_code, pre_requisite FROM UnitRelationship")
    relationships = cursor.fetchall()

    G = nx.DiGraph()

    for unit_code, _ in relationships:
        G.add_node(unit_code)

    for unit_code, pre_requisite in relationships:
        G.add_edge(pre_requisite, unit_code)

    conn.close()

    return G


def highlight_path(G, selected_unit):
    """ Highlight the path to prerequisites for a selected unit.

    Args:
        G (DiGraph): A directed acyclic graph (DAG) of units and their prerequisites.
        selected_unit (str):  The unit code of the selected unit.

    Returns:
        path_nodes (list(str)): list of unit codes in the path to prerequisites
    """    
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


def visualize_graph(G, selected_unit:str, path_nodes)-> None:
    """ Visualize the DAG with highlighted path.

    Args:
        G (DiGraph): A directed acyclic graph (DAG) of units and their prerequisites.  
        selected_unit (str): unit code of the selected unit
        path_nodes (list(str)): list of unit codes in the path to prerequisites
    """    
    # Draw the DAG with highlighted path
    pos = nx.drawing.layout.shell_layout(G, nlist=[list(G.nodes())])

    plt.figure(figsize=(10, 6))

    # Draw all nodes and edges with default styles
    nx.draw_networkx(
        G,
        pos,
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

    # Customize the appearance of edges pointing to the selected unit
    for node in G.nodes():
        if node in path_nodes:
            continue
        if G.has_edge(node, selected_unit):
            edge = (node, selected_unit)
            edge_color = "blue"  # Change this to the desired color
            edge_width = 2  # Change this to the desired line width
            nx.draw_networkx_edges(
                G,
                pos,
                edgelist=[edge],
                width=edge_width,
                edge_color=edge_color,
                arrowsize=20,
            )

    # Highlight the path nodes with a different color
    nx.draw_networkx_nodes(
        G,
        pos,
        nodelist=path_nodes,
        node_size=1500,
        node_color="gold",  # Change this to the desired color
    )

    plt.title(f"Prerequisite Path for Unit '{selected_unit}'")
    plt.axis("off")
    plt.tight_layout()
    plt.show()
