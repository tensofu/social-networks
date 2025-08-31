import argparse
import random
import time
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from queue import Queue
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

  # Parses and gathers the arguments
  args = parser.parse_args()
  
  # Converts the `n` to an integer.
  if (args.create_random_graph):
    args.create_random_graph[0] = int(args.create_random_graph[0]) 

  # Prints out all of the arguments passed (or not) for debugging purposes.
  print(args.input, args.create_random_graph, args.multi_BFS, args.analyze, args.plot, args.output)
  
  # OVERRIDES ARGUMENT --input IF --create_random_graph ARGUMENTS ARE PRESENT (sets --input arguments to None)
  if (args.create_random_graph and args.input):
    print(f"The arguments for flags [--input] & [--create_random_graph] both coexist. Proceeding to override and nullify the [--input] argument.")
    args.input = None
    
    
  # GRAPH CONSTRUCTION SECTION
  graph = None

  # Generates an Erdos-Renyi Graph using a high level implementation (only create if the arguments for --create_random_graph are present)
  if (args.create_random_graph):
    # Sets a random seed for reproducibility
    seed = 42
    
    # Generates the graph with the number of nodes, constant, and probability, then saves it.
    num_nodes = args.create_random_graph[0]
    constant = args.create_random_graph[1]
    edge_probability = ( constant*np.log(num_nodes) ) / num_nodes
    
    print(f"""Creating an Erdos-Renyi Randomized Graph with these parameters:
        seed = {seed}
        n = {num_nodes}
        c = {constant}
        p = {edge_probability}""")

    graph = nx.erdos_renyi_graph(n=num_nodes, p=edge_probability, seed=seed)
    
    # Saves the graph to the designated output file
    nx.write_gml(graph, f"data/{args.output}")
    print(f"Graph saved to data/{args.output}")
    print()
  elif (args.input):
    graph = nx.read_gml(f"data/{args.input}")
  else:
    print("No --input or --create_random_graph arguments detected. No graph has been loaded.")

  # GRAPH ANALYSIS SECTION
  if (graph and args.analyze):
    # Multi BFS Traversal
    sources = args.multi_BFS
    bfs_results, visited = helper.multi_search_bfs(graph, sources)
    print(f"Multi-BFS Traversal using source(s) {sources}: {bfs_results}")
    print(f"Path tracking: {visited}")
    
    # Identifying connected components
    connected_components = helper.identify_connected_components(graph)
    print(f"List of connected components: {connected_components}")
    
    # Identifying isolated nodes
    isolated_nodes = helper.identify_isolate_nodes(graph)
    print(f"List of isolated nodes: {isolated_nodes}")
        
  # Stops timer
  end_time = time.perf_counter()
  elapsed_time = end_time - start_time
  print(f"Code executed in: {elapsed_time:.4f} seconds")
  
  # GRAPH PLOTTING SECTION
  if (graph and args.plot):
    # Specifies layout and displays the graph
    layout = nx.kamada_kawai_layout(graph)
    nx.draw(graph, layout, with_labels=True, width=1, node_size=25)
    plt.show()
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
'''

