import argparse
from utils import helper


def main():
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

  # Prints out all of the arguments passed (or not) for debugging purposes.
  args = parser.parse_args()
  print(args.input, args.create_random_graph, args.multi_BFS, args.analyze, args.plot, args.output)
  
  # OVERRIDES ARGUMENT --input IF --create_random_graph ARGUMENTS ARE PRESENT (sets --input arguments to None)
  if (args.create_random_graph and args.input):
    print(f"The arguments for flags [--input] & [--create_random_graph] both coexist. Proceeding to override and nullify the [--input] argument.")
    args.input = None


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

