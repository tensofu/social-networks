import argparse
import time
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from utils import helper


def main():
  # PROGRAM TIMER
  start_time = time.perf_counter()
  
  # PARSER SECTION
  # Creates the parser object in order to read in the passed in arguments and flags.
  #   Utilizes the argparse library to ease the implementation for a working CL structure.
  parser = argparse.ArgumentParser(
    prog="Erdos-Renyi Randomized Graph Program",
    description="This program will help generate randomized graphs and analyze them."
  )

  # Adds all valid flags and arguments to the parser, according to this CL structure:
  #   python ./graph.py [--input graph_file.gml] [--create_random_graph n c] [--multi_BFS a1 a2 ...] 
  #                     [--analyze] [--plot] [--output out_graph_file.gml]
  parser.add_argument("--input", type=str)
  parser.add_argument("--create_random_graph", nargs=2, type=float)
  parser.add_argument("--multi_BFS", nargs="+", type=int)
  parser.add_argument("--analyze", action="store_true")
  parser.add_argument("--plot", action="store_true")
  parser.add_argument("--output", type=str)
  parser.add_argument("--seed", type=int)

  # Parses and gathers the arguments
  args = parser.parse_args()
  
  # Converts the `n` to an integer.
  if (args.create_random_graph):
    args.create_random_graph[0] = int(args.create_random_graph[0]) 

  # Prints out all of the arguments passed (or not) for debugging purposes.
  print("Arguments:")
  print(args.input, args.create_random_graph, args.multi_BFS, args.analyze, args.plot, args.output)
  print() 
  
  # OVERRIDES ARGUMENT --input IF --create_random_graph ARGUMENTS ARE PRESENT (sets --input arguments to None)
  if (args.create_random_graph and args.input):
    print(f"The arguments for flags [--input] & [--create_random_graph] both coexist. Proceeding to override and nullify the [--input] argument.")
    args.input = None
    
  # Handles if there are not sufficient parameters
  if not args.plot:
    print("--plot is not present. The graph will not be shown.")
  if not args.analyze:
    print("--analyze is not present. There will be no analysis present in the terminal.")
  print()
    
  # GRAPH CONSTRUCTION SECTION
  graph = None

  # Generates an Erdos-Renyi Graph using a high level implementation (only create if the arguments for --create_random_graph are present)
  if (args.create_random_graph):
    # Sets a seed for reproducibility
    seed = 42
    if (args.seed):
      seed = args.seed
    
    # Generates the graph with the number of nodes, constant, and probability, then saves it.
    num_nodes = args.create_random_graph[0]
    constant = args.create_random_graph[1]
    edge_probability = ( constant*np.log(num_nodes) ) / num_nodes
    connected_components = []
    
    print(f"""Creating an Erdos-Renyi Randomized Graph with these parameters:
        seed = {seed}
        n = {num_nodes}
        c = {constant}
        p = {edge_probability}""")

    graph = nx.erdos_renyi_graph(n=num_nodes, p=edge_probability, seed=seed)
    
  elif (args.input):
    try:
      graph = nx.read_gml(f"data/{args.input}")
    except nx.NetworkXError as e:
      print(f"Error: Could not read the file as a GML graph: {e}")
      print("Please ensure the file is a valid GML format.")
      return
    except FileNotFoundError:
      print(f"File `data/{args.input}` was not found. Please specify an existing .gml file inside the `data/` directory.")
      return
  else:
    print("No --input or --create_random_graph arguments detected. No graph has been loaded.")
    
  if (graph and args.output):
    # Saves the graph to the designated output file
    nx.write_gml(graph, f"data/{args.output}")
    print(f"Graph saved to data/{args.output}")
    print()

  #variable declarations
  sources = []
  isolated_nodes = []
  
  # GRAPH ANALYSIS SECTION
  if (graph and args.analyze):
    print("Graph Analysis:")
    # Multi BFS Traversal
    sources = args.multi_BFS
    bfs_results, visited, edge_colors, node_colors = helper.multi_search_bfs(graph, sources)
    print(f"Multi-BFS Traversal using source(s) {sources}: {bfs_results}")
    print(f"Path tracking: {visited}")
    print()
    
    # Identifying connected components
    connected_components = helper.identify_connected_components(graph)
    print(f"List of connected components:")
    for cc,_,_ in connected_components:
      print(cc, end = "")
    print('\n')
    
    #Identify if cycles exist in graph
    cycle_bool = helper.cycle_detection(graph)
    print("A cycle exists in the graph") if cycle_bool else print("No cycle exists in the graph")
    print()

    # Identifying isolated nodes
    isolated_nodes = helper.identify_isolate_nodes(graph)
    print(f"List of isolated nodes: {isolated_nodes}")
    print()

    
    #Compute density of graph
    density_graph = helper.graph_density(graph)
    print(f"The Graph's measured density is: {density_graph}")
    print()


    #Compute Average Shortest Path Length
    avg_spl = helper.avg_shortest_path_lenf(graph)
    if avg_spl:
      print(f"Average Shortest Path Length: {avg_spl}")    
    else:
      print("The graph is not connected, therefore we cannot compute the average shortest path length")
    print()
  
  # Stops timer
  end_time = time.perf_counter()
  elapsed_time = end_time - start_time
  print(f"Code executed in: {elapsed_time:.4f} seconds")
  
  # GRAPH PLOTTING SECTION
  if (graph and args.plot):
    # Options for the graph
    layout = nx.kamada_kawai_layout(graph)
    options = {
      "with_labels": True, 
      "font_size": 10,
      "verticalalignment": 'top',
      "width": 1, 
      "node_size": 25,
    }
    
    # Colors each isolated node in 'red', others in 'blue'
    if (graph and isolated_nodes):
      for node in isolated_nodes:
        node_colors[int(node)] = 'peru'
      
    # Checks if edge_colors or node_colors maps exists. If they do, apply it.
    if 'edge_colors' in locals():
      options["edge_color"] = edge_colors
    if 'node_colors' in locals():
      options['node_color'] = node_colors
      
    # Displays the graph
    nx.draw(graph, layout, **options,)
    
    plt.show()
    

  #option to visualize connected components
    if 'connected_components' not in locals():
      return
  #iterates over each connected component and plots/displays them seperately
    user_resp = input("Would you like to visually see each connected component of the graph (Y/n)? ")
    if user_resp in {"Y","yes","Yes", "y"}:
      for cc,cc_edges,color in connected_components:
        options_cc = {
        "with_labels": True, 
        "font_size": 10,
        "verticalalignment": 'top',
        "width": 1, 
        "node_size": 25,
        "edge_color": color,
        "nodelist":cc,
        "edgelist":cc_edges
        }
        nx.draw(graph, layout, **options_cc)
        plt.title("Connected Component")
        plt.show()
      
    # Displays the graph
    
  else:
    print("There was no graph to be displayed...")



# Runs the program
if __name__ == "__main__":
  main()
  

'''
CLI Tests (generating a graph, reading a graph, input & output present, filename is not .gml):
  python ./graph.py --create_random_graph 200 1.5 --multi_BFS 0 5 20 --analyze --plot --output final_graph.gml
  python ./graph.py --input data.gml --analyze --plot
  python ./graph.py --input graph_file.gml --create_random_graph 200 1.5 --multi_BFS 0 5 20 --analyze --plot --output final_graph.gml
  python ./graph.py --input graph_file.gml --create_random_graph 200 1.5 --multi_BFS 0 5 20 --analyze --plot --output final_graph.txt
  python ./graph.py --create_random_graph 25 0.7 --multi_BFS 0 5 20 --analyze --plot --output data1.gml
'''

