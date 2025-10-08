import argparse
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from itertools import islice
from utils import helper
import os


# MAIN FUNCTION
def main():
  # PARSER SECTION
  # Creates the parser object in order to read in the passed in arguments and flags.
  #   Utilizes the argparse library to ease the implementation for a working CL structure.
  parser = argparse.ArgumentParser(
    prog="Social Networks and Structural Balance",
    description="This program will help generate randomized graphs and analyze them."
  )

  # Adds additional options and arguments to the parser, accoring to this CL structure:
  #   python ./graph.py ..
  parser.add_argument("--input", type=str)
  parser.add_argument("--plot", choices=['C', 'N', 'P', 'T'])
  parser.add_argument("--output", type=str)

  # Adds additional options and arguments to the parser:
  parser.add_argument("--components", type=int)
  parser.add_argument("--split_output_dir", action="store_true")
  parser.add_argument("--verify_homophily", action="store_true")
  parser.add_argument("--verify_balanced_graph", action="store_true")
  parser.add_argument("--temporal_simulation", type=str)

  parser.add_argument("--simulate_failures", type=int)
  parser.add_argument("--robustness_check", type=int)

  # Parses and gathers the arguments
  args = parser.parse_args()
    
  # Handles if there are not sufficient parameters
  if not args.plot:
    print("--plot is not present. The graph will not be shown.")
  print()
    
  # GRAPH CONSTRUCTION SECTION
  graph = None
    
  if (args.input):
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
    print("No --input No graph has been loaded.")
    
  # Compute metrics
  clustering = helper.compute_clustering_coefficients(graph)
  overlap = helper.compute_neighborhood_overlap(graph)
  print()
    
  # Partition components with the Girvan Newman method
  if args.components:
    print(f"Partitioning graph into {args.components} components...")
    communities_generator = nx.community.girvan_newman(graph)
    
    # Get the desired number of communities
    for i, communities in enumerate(communities_generator):
      if len(communities) >= args.components:
        break
    
    print(f"Found {len(communities)} communities:")
    
    # Assign community labels to nodes
    for i, community in enumerate(communities):
      for node in community:
        graph.nodes[node]['community'] = i + 1
        graph.nodes[node]['community_label'] = f"Community {i + 1}"
      
      print(f"  Community {i+1}: {len(community)} nodes - {sorted(list(community))[:10]}{'...' if len(community) > 10 else ''}")
    
    # Export components separately if requested
    if args.split_output_dir:
      output_dir = "data/components"
      os.makedirs(output_dir, exist_ok=True)
      for i, community in enumerate(communities):
        subgraph = graph.subgraph(community).copy()
        output_file = f"{output_dir}/component_{i+1}.gml"
        nx.write_gml(subgraph, output_file)
        print(f"  Saved component {i+1} to {output_file}")
    print()


  # Verify homophily
  if args.verify_homophily:
    print("---VERIFY HOMOPHILY TEST---")
    helper.verify_homophily(graph)
    print()
  
  # Verify balanced graph
  if args.verify_balanced_graph:
    print("---VERIFY BALANCED GRAPH TEST---")
    helper.verify_structural_balance(graph)
    print()
    
  # Simulate failures
  if args.simulate_failures:
    graph = helper.simulate_failures(graph, args.simulate_failures)
    print()
    
  # Handle robustness check
  if args.robustness_check:
    graph = helper.robustness_check(graph, args.robustness_check)
    
  # Saves the graph to the designated output file
  if args.output:
    nx.write_gml(graph, f"data/{args.output}")
    print(f"Graph saved to data/{args.output}")
    print()
  
  # GRAPH PLOTTING SECTION
  if args.plot == 'C':
    helper.plot_clustering_coefficient(graph, clustering)
  elif args.plot == 'N':
    helper.plot_neighborhood_overlap(graph, overlap)
  elif args.plot == 'P':
    helper.plot_attributes(graph)
  elif args.plot == 'T' and args.temporal_simulation:
    path = "data/" + args.temporal_simulation
    helper.temporal_simulation(graph, path)
    
  else:
    print("There was no graph to be displayed...")



# Runs the program
if __name__ == "__main__":
  main()
  

'''
CLI Tests:
  python3 ./graph_analysis.py --input graph.gml --components 3 --plot C --simulate_failures 5 --output output.gml
'''

