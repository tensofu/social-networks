import networkx as nx
from queue import Queue
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import os
import csv
import random

# This program contains functions that will help do miscallenous things such as file checking and etc.

# Checks if the given filename is a valid .gml filename.
def is_gml(filename: str) -> bool:
  if (not filename):
    return False
  if (filename[-4:] != ".gml"):
    return False
  return True

# Performs a multi-search BFS and returns four lists: the results, paths tracked, shortest path edge color array, and 
#   source node color array.
def multi_search_bfs(graph: nx.Graph, sources: list):
  # Checks if sources exists. If not, initialize it as a list ["0"].
  if not sources:
    sources = ["0"]
  
  # To cycle through colors and map to a source
  available_colors = ['red', 'blue', 'green', 'purple', 'orange', 'cyan']
  source_to_color = {
    source: available_colors[i % len(available_colors)] 
    for i, source in enumerate(sources)
  }
  
  # Normalizes the source colors into an array
  source_node_color_array = []
  for node in graph.nodes():
    if node in source_to_color:
      source_node_color_array.append(source_to_color[node])
    else:
      source_node_color_array.append('skyblue')
  
  # Maps 
  edge_colors = {}
  bfs_map = {}
  
  for source in sources:
    bfs_map[source] = []
  
  # Multi-Search BFS
  bfs_results = []
  queue = Queue()
  visited = []
  for item in sources:
    queue.put(item)
    bfs_results.append(item)
  while (not queue.empty()):
    current_node = queue.get()
    # Gets the list of neighbors for a specified node
    try:
      neighbors_iterator = graph.neighbors(current_node)
    except nx.NetworkXError:
      neighbors_iterator = graph.neighbors(str(current_node))
    for item in neighbors_iterator:
      if (item not in bfs_results):
        queue.put(item)
        edge = (int(current_node), int(item))
        if (edge not in visited):
          visited.append(edge)
          edge_colors[tuple(sorted(edge))] = source_to_color[current_node]
          source_to_color[item] = source_to_color[current_node]
        bfs_results.append(item)
        
  # Normalizes the edge colors into an array
  edge_colors_array = []
  for u, v in graph.edges():
    edge = tuple(sorted((u, v)))
    if edge in edge_colors:
      edge_colors_array.append(edge_colors[edge])
    else:
      edge_colors_array.append('gray')
      
  return bfs_results, visited, edge_colors_array, source_node_color_array

# Identifies connected components using a recursive DFS Search
#   Iterates through each node in the graph, performs DFS search until all connected nodes & edges are visited from that node, then
#   returns the connected component that sourced from that node, edges in the connected component, and an index for edge_color.
#  Repeat through every node in the graph that has not yet been visited.
def identify_connected_components(graph: nx.Graph):
  visited = set()
  connected_components_w_edges = []
  color_index = 0

  available_colors = ['red', 'blue', 'green', 'purple', 'orange', 'cyan', 'yellow', 'brown', 'pink', 'black']
  
  # Recursive DFS function
  def dfs(node, current_component, traversed_edges,color_indx):
    visited.add(node)
    current_component.append(node)
    for neighbor in graph.neighbors(node):
      if neighbor not in visited:
        dfs(neighbor, current_component,traversed_edges,color_index)
      if (node,neighbor) not in traversed_edges or (neighbor,node) not in traversed_edges:
        traversed_edges.add((node,neighbor))
    


  for node in graph:
    if node not in visited:
      current_component = []
      trav_edges =set() 
      dfs(node, current_component,trav_edges,color_index)
      connected_components_w_edges.append((sorted(current_component), trav_edges, available_colors[(color_index%len(available_colors))]))
      color_index +=1
  return connected_components_w_edges

def identify_isolate_nodes(graph: nx.Graph):
  isolated_nodes = list(nx.isolates(graph))
  
  return isolated_nodes

def cycle_detection(graph: nx.Graph):
  visited = set()
  def dfs(node, prev):
    visited.add(node)
    for neighbor in graph.neighbors(node):
      if neighbor not in visited:
        if dfs(neighbor,node):
          return True
      else:
        if neighbor != prev:
          return True
    return False
  node_list = list(graph.nodes)
  if node_list:
    return dfs(node_list[0],None)
  else:
    return False
  

def graph_density(graph: nx.Graph):
  num_edges =  graph.number_of_edges()

  #compute total possible number of edges in the graph
  num_nodes = graph.number_of_nodes()
  max_possible_edges = (num_nodes*(num_nodes-1))/2

  density = num_edges/max_possible_edges
  return round(density,2)

def avg_shortest_path_lenf(graph:nx.Graph):
  #first check if graph is fully connected by using connected components function
  if len(identify_connected_components(graph)) == 1:

      #create dict to store nodes and shortest path lenf between nodes
      node_dict = {}

      #perform bfs from each node and store resulting shortest paths
      for bfs_start_node in list(graph.nodes):
        node_dict[bfs_start_node] = {}

        #preform bfs on graph and store shortest path between nodes in dict:
        queue = Queue()
        queue.put((bfs_start_node,0))
        
        visited_nodes = set()
        visited_nodes.add(bfs_start_node)

        while (not queue.empty()):
          current_node, level = queue.get()

          # Gets the list of neighbors for a specified node
          neighbors_iterator = graph.neighbors(current_node)
          for nbr_node in neighbors_iterator:
            if (nbr_node not in visited_nodes):
              queue.put((nbr_node, level +1))

              #if neighbor has not been added to dict of node we started bfs from then add it and the path lenf
              if nbr_node not in node_dict[bfs_start_node]:
                node_dict[bfs_start_node][nbr_node] = (level+1)

              #essentially do same as above but for the neighboring node
              if (nbr_node in node_dict) and (bfs_start_node not in node_dict[nbr_node]):
                node_dict[nbr_node][bfs_start_node] = (level+1)

          visited_nodes.add(current_node)

      #taking average of shortest paths between each pairs of ndoes
      num_paths = 0
      sum_shortestpaths = 0

      for node in node_dict:
        num_paths +=len(node_dict[node])
        for neighbor in node_dict[node]:
          sum_shortestpaths+=node_dict[node][neighbor]
      return round(sum_shortestpaths/num_paths,2)

  else:
    #graph is not connected
    return False



### ASSIGNMENT PART 2

# Check if signed graph is balanced using BFS-based methods.
def verify_structural_balance(G):
  if not nx.get_edge_attributes(G, 'sign'):
    print("No edge signs found in the graph. Cannot verify structural balance.")
    return False
  
  # Check for negative cycles which indicate imbalance
  # Convert to signed graph representation
  positive_edges = [(u, v) for u, v, d in G.edges(data=True) if d.get('sign', 1) > 0]
  negative_edges = [(u, v) for u, v, d in G.edges(data=True) if d.get('sign', 1) < 0]
  
  # Create graph with only positive edges
  G_pos = G.edge_subgraph(positive_edges).copy() if positive_edges else nx.Graph()
  
  # Check if we can 2-color the components
  is_balanced = True
  
  # For each connected component of the original graph
  for component in nx.connected_components(G):
    if len(component) < 3:
      continue
        
    subgraph = G.subgraph(component)
    
    # Check triangles for balance
    triangles = [cycle for cycle in nx.cycles.cycle_basis(subgraph) if len(cycle) == 3]
    
    for triangle in triangles:
      # Count negative edges in triangle
      neg_count = 0
      for i in range(3):
        u, v = triangle[i], triangle[(i+1)%3]
        if subgraph.has_edge(u, v):
          if subgraph[u][v].get('sign', 1) < 0:
            neg_count += 1
        
        # Triangle is balanced if it has 0 or 2 negative edges
        if neg_count == 1 or neg_count == 3:
          is_balanced = False
          break
    
    if not is_balanced:
      break
  
  print(f"Graph is {'balanced' if is_balanced else 'NOT balanced'}")
  return is_balanced

# Computing
def compute_clustering_coefficients(G):
  """Compute clustering coefficient for each node."""
  clustering = nx.clustering(G)
  avg_clustering = nx.average_clustering(G)
  print(f"Average clustering coefficient: {avg_clustering:.4f}")
  return clustering


def compute_neighborhood_overlap(G):
  """Compute neighborhood overlap for each edge."""
  overlap = {}
  for u, v in G.edges():
    neighbors_u = set(G.neighbors(u))
    neighbors_v = set(G.neighbors(v))
    
    # Remove the endpoints from each other's neighbor sets
    neighbors_u.discard(v)
    neighbors_v.discard(u)
    
    # Calculate overlap
    if len(neighbors_u) + len(neighbors_v) > 0:
      overlap[(u, v)] = len(neighbors_u & neighbors_v) / len(neighbors_u | neighbors_v)
    else:
      overlap[(u, v)] = 0
  
  if overlap:
    avg_overlap = sum(overlap.values()) / len(overlap)
    print(f"Average neighborhood overlap: {avg_overlap:.4f}")
  
  return overlap


# Statistical test for homophily using node attributes.
def verify_homophily(G):
  # Try different common attribute names (excluding gender)
  attr_names = ['color', 'group', 'type', 'community', 'cluster']
  attr_found = None
  
  for attr in attr_names:
    if nx.get_node_attributes(G, attr):
      attr_found = attr
      break
  
  if not attr_found:
    print("No suitable node attributes found for homophily test.")
    print("Consider adding node attributes like 'group' or 'community' for homophily analysis.")
    return
  
  # Calculate assortativity coefficient
  assortativity = nx.attribute_assortativity_coefficient(G, attr_found)
  print(f"Assortativity coefficient for '{attr_found}': {assortativity:.4f}")
  
  # Perform statistical test (permutation test)
  n_permutations = 1000
  random_assortativities = []
  
  node_attrs = nx.get_node_attributes(G, attr_found)
  nodes = list(G.nodes())
  values = list(node_attrs.values())
  
  for _ in range(n_permutations):
    random.shuffle(values)
    random_attrs = dict(zip(nodes, values))
    nx.set_node_attributes(G, random_attrs, attr_found)
    random_assortativities.append(nx.attribute_assortativity_coefficient(G, attr_found))
  
  # Restore original attributes
  nx.set_node_attributes(G, node_attrs, attr_found)
  
  # Calculate p-value
  p_value = sum(1 for r in random_assortativities if abs(r) >= abs(assortativity)) / n_permutations
  
  print(f"Homophily test (p-value): {p_value:.4f}")
  if p_value < 0.05:
    print("Significant homophily detected (p < 0.05)")
  else:
    print("No significant homophily detected")
    
    
# PLOTTING FUNCTIONS
def plot_clustering_coefficient(G, clustering):
  """Plot graph with node size based on clustering coefficient."""
  pos = nx.spring_layout(G, seed=42, k=1/np.sqrt(len(G.nodes())))
  
  # Node sizes based on clustering coefficient
  node_sizes = [500 * (clustering[node] + 0.1) for node in G.nodes()]
  
  # Node colors based on degree
  node_colors = [G.degree(node) for node in G.nodes()]
  
  plt.figure(figsize=(12, 8))
  nx.draw_networkx_nodes(G, pos, node_size=node_sizes, 
                        node_color=node_colors, cmap='viridis',
                        alpha=0.7)
  nx.draw_networkx_edges(G, pos, alpha=0.3)
  nx.draw_networkx_labels(G, pos, font_size=8)
  
  plt.title("Graph Visualization: Node Size = Clustering Coefficient, Color = Degree")
  sm = plt.cm.ScalarMappable(cmap='viridis', 
                              norm=plt.Normalize(vmin=min(node_colors), vmax=max(node_colors)))
  sm.set_array([])
  plt.axis('off')
  plt.tight_layout()
  plt.show()


def plot_neighborhood_overlap(G, overlap):
    """Plot graph with edge thickness based on neighborhood overlap."""
    pos = nx.spring_layout(G, seed=42, k=1/np.sqrt(len(G.nodes())))
    
    # Edge widths based on neighborhood overlap
    edge_widths = [5 * overlap.get((u, v), overlap.get((v, u), 0)) + 0.5 
                  for u, v in G.edges()]
    
    # Edge colors based on sum of endpoint degrees
    edge_colors = [G.degree(u) + G.degree(v) for u, v in G.edges()]
    
    plt.figure(figsize=(12, 8))
    nx.draw_networkx_nodes(G, pos, node_size=300, node_color='lightblue', alpha=0.7)
    edges = nx.draw_networkx_edges(G, pos, width=edge_widths, 
                                   edge_color=edge_colors, edge_cmap=plt.cm.RdYlBu,
                                   edge_vmin=min(edge_colors) if edge_colors else 0,
                                   edge_vmax=max(edge_colors) if edge_colors else 1)
    nx.draw_networkx_labels(G, pos, font_size=8)
    
    plt.title("Graph Visualization: Edge Thickness = Neighborhood Overlap, Color = Sum of Degrees")
    if edges:
        plt.colorbar(edges, label='Sum of Endpoint Degrees', orientation='horizontal', pad=0.1)
    plt.axis('off')
    plt.tight_layout()
    plt.show()


def plot_attributes(G):
  """Plot graph with node colors and edge signs visualization."""
  pos = nx.spring_layout(G, seed=42, k=1/np.sqrt(len(G.nodes())))
  
  # Get node attributes for coloring
  node_attrs = None
  attr_name = 'default'
  for attr in ['color', 'group', 'type', 'community', 'cluster']:
    if nx.get_node_attributes(G, attr):
      node_attrs = nx.get_node_attributes(G, attr)
      attr_name = attr
      break
  
  if node_attrs:
    # Convert attributes to numeric values for coloring
    unique_attrs = list(set(node_attrs.values()))
    attr_to_num = {attr: i for i, attr in enumerate(unique_attrs)}
    node_colors = [attr_to_num[node_attrs[node]] for node in G.nodes()]
  else:
    # Use degree centrality as default coloring
    node_colors = [G.degree(node) for node in G.nodes()]
    attr_name = 'degree'
  
  plt.figure(figsize=(12, 8))
  
  # Draw nodes
  nx.draw_networkx_nodes(G, pos, node_size=300, node_color=node_colors, 
                        cmap='tab10' if node_attrs else 'viridis', alpha=1.0)
  
  # Draw edges with different styles for positive/negative signs
  edge_signs = nx.get_edge_attributes(G, 'sign')
  if edge_signs:
    pos_edges = [(u, v) for u, v in G.edges() if edge_signs.get((u, v), edge_signs.get((v, u), 1)) > 0]
    neg_edges = [(u, v) for u, v in G.edges() if edge_signs.get((u, v), edge_signs.get((v, u), 1)) <= 0]
    
    nx.draw_networkx_edges(G, pos, edgelist=pos_edges, edge_color='green', 
                          width=2, alpha=0.6, label='Positive')
    nx.draw_networkx_edges(G, pos, edgelist=neg_edges, edge_color='red', 
                          width=2, style='dashed', alpha=0.6, label='Negative')
    plt.legend()
  else:
    nx.draw_networkx_edges(G, pos, alpha=0.4)
  
  nx.draw_networkx_labels(G, pos, font_size=8)
  
  plt.title(f"Graph Attributes: Node Color = {attr_name}, Edge Style = Sign")
  plt.axis('off')
  plt.tight_layout()
  plt.show()


"""Animate graph evolution based on temporal edge changes."""
def temporal_simulation(G, temporal_file):
  if not os.path.exists(temporal_file):
    print(f"Temporal simulation file {temporal_file} not found.")
    return
  
  # Read temporal data
  edge_changes = []
  with open(temporal_file, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
      edge_changes.append({
        'source': str(row['source']),
        'target': str(row['target']),
        'timestamp': float(row['timestamp']),
        'action': row['action']
      })
  
  # Sort by timestamp
  edge_changes.sort(key=lambda x: x['timestamp'])
  
  # Create animation
  fig, ax = plt.subplots(figsize=(10, 8))
  pos = nx.spring_layout(G, seed=42, k=1/np.sqrt(len(G.nodes())))
  
  G_temp = nx.Graph()
  G_temp.add_nodes_from(G.nodes())
  
  def update(frame):
    ax.clear()
    
    if frame < len(edge_changes):
      change = edge_changes[frame]
      if change['action'] == 'add':
        G_temp.add_edge(change['source'], change['target'])
      elif change['action'] == 'remove' and G_temp.has_edge(change['source'], change['target']):
        G_temp.remove_edge(change['source'], change['target'])
    
    nx.draw(G_temp, pos, ax=ax, with_labels=True, node_size=300, 
            node_color='lightblue', edge_color='gray')
    ax.set_title(f"Temporal Evolution - Step {frame}/{len(edge_changes)}")
  
  ani = animation.FuncAnimation(fig, update, frames=len(edge_changes)+1, 
                                interval=500, repeat=False)
  plt.show()
  
  return ani


# Simulate random edge failures and analyze robustness.
def robustness_check(G, k, n_simulations=100):
  print(f"\nSimulating {n_simulations} rounds of {k} random edge failures...")
  
  results = {
    'num_components': [],
    'max_component_size': [],
    'min_component_size': []
  }
  
  original_components = list(nx.connected_components(G))
  original_num_components = len(original_components)
  
  for sim in range(n_simulations):
    G_temp = G.copy()
    edges = list(G_temp.edges())
    
    if k > len(edges):
      print(f"Warning: k ({k}) is larger than number of edges ({len(edges)})")
      k = min(k, len(edges))
    
    # Remove k random edges
    edges_to_remove = random.sample(edges, k)
    G_temp.remove_edges_from(edges_to_remove)
    
    # Analyze components
    components = list(nx.connected_components(G_temp))
    component_sizes = [len(c) for c in components]
    
    results['num_components'].append(len(components))
    results['max_component_size'].append(max(component_sizes) if component_sizes else 0)
    results['min_component_size'].append(min(component_sizes) if component_sizes else 0)
  
  # Report statistics
  print(f"Original number of components: {original_num_components}")
  print(f"After {k} edge failures:")
  print(f"  Average number of components: {np.mean(results['num_components']):.2f}")
  print(f"  Max component size (avg): {np.mean(results['max_component_size']):.2f}")
  print(f"  Min component size (avg): {np.mean(results['min_component_size']):.2f}")
  
  # Check if original clusters persist (simplified check)
  cluster_persistence = sum(1 for n in results['num_components'] 
                          if n <= original_num_components * 1.5) / n_simulations
  print(f"  Cluster persistence rate: {cluster_persistence:.2%}")


# Remove k random edges before partitioning.
def simulate_failures(G, k):
  print(f"---SIMULATING FAILURES (k={k})---")
  
  # Obtains the average shortest path before
  avg_short_before = avg_shortest_path_lenf(G)
  
  G_failures = G.copy()
  edges = list(G_failures.edges())
  
  if k > len(edges):
    print(f"Warning: k ({k}) is larger than number of edges ({len(edges)})")
    k = min(k, len(edges))
  
  edges_to_remove = random.sample(edges, k)
  G_failures.remove_edges_from(edges_to_remove)
  print(f"Removed {k} random edges for simulating failures")
  
  # Finds the average shortest path after
  avg_short_after = avg_shortest_path_lenf(G_failures) 
  print(f"  Change in average shortest path: {avg_short_before} -> {avg_short_after if avg_short_after else "None (graph is disconnected)"}")
  
  return G_failures
