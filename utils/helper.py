import networkx as nx
from queue import Queue

# This program contains functions that will help do miscallenous things such as file checking and etc.


# Checks if the given filename is a valid .gml filename.
def is_gml(filename: str) -> bool:
  if (not filename):
    return False
  if (filename[-4:] != ".gml"):
    return False
  return True

# Performs a multi-search BFS and returns two lists: the results and paths tracked.
def multi_search_bfs(graph: nx.Graph, sources: list):
  # Checks if sources exists. If not, initialize it as a list ["0"].
  if not sources:
    sources = ["0"]
  
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
    neighbors_iterator = graph.neighbors(current_node)
    for item in neighbors_iterator:
      if (item not in bfs_results):
        queue.put(item)
        edge = (current_node, item)
        if (edge not in visited):
          visited.append(edge)
        bfs_results.append(item)
  return bfs_results, visited

# Identifies connected components using a recursive DFS Search
#   Iterates through each node in the graph, performs DFS search until all connected nodes are visited, then
#   returns the connected component that sourced from that node. Repeat through every node in the graph that has
#   not yet been visited.
def identify_connected_components(graph: nx.Graph):
  visited = set()
  connected_components = []
  
  # Recursive DFS function
  def dfs(node, current_component):
    visited.add(node)
    current_component.append(node)
    for neighbor in graph.neighbors(node):
      if neighbor not in visited:
        dfs(neighbor, current_component)

  for node in graph:
    if node not in visited:
      current_component = []
      dfs(node, current_component)
      connected_components.append(sorted(current_component))
      
  return connected_components

def identify_isolate_nodes(graph: nx.Graph):
  isolated_nodes = []
  for node in graph:
    if (not any(graph.neighbors(node))):
      isolated_nodes.append(node)
  
  return isolated_nodes
