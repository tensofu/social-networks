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
    neighbors_iterator = graph.neighbors(current_node)
    for item in neighbors_iterator:
      if (item not in bfs_results):
        queue.put(item)
        edge = (current_node, item)
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
  
