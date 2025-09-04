# Erdos-Renyi Randomized Graph Generator

This project is done for a class assignment involving the generation and analysis of Erdos-Renyi randomized graphs. It will mainly be done in Python, and feature a GUI that displays the graphs, with terminal output which identifies cycles, connected components, and etc.

The usage will consist of running flags and arguments in for executing certain tasks. Be sure to use an environment with all of the packages listed in `requirements.txt` present.

# Setup Instructions
1. Ensure python and pip are working on your machine.
2. Download or clone the repository (make sure you have `git` installed):
```bash
git clone https://github.com/tensofu/ErdosRenyiGraphs.git
cd ErdosRenyiGraphs/
```
3. Create a new virtual environment within the project folder
```bash
# Create the virtual environment
python -m venv venv
```
4. Activate the virtual environment
```bash
# (on macOS/Linux)
source venv/bin/activate

# (on Windows via Command Prompt)
venv\Scripts\activate
```
5. Install the packages according to `requirements.txt`
```bash
pip install -r requirements.txt
```
6. Run some of the following commands to test it out:
```bash
python ./graph.py --create_random_graph 200 1.5 --multi_BFS 0 5 20 --analyze --plot --output final_graph.gml
python ./graph.py --input data.gml --analyze --plot
python ./graph.py --input graph_file.gml --create_random_graph 200 1.5 --multi_BFS 0 5 20 --analyze --plot --output final_graph.gml
python ./graph.py --input graph_file.gml --create_random_graph 200 1.5 --multi_BFS 0 5 20 --analyze --plot --output final_graph.txt
python ./graph.py --create_random_graph 6 0.4 --multi_BFS 0 2 --analyze --plot --output data.gml
```

# Usage

# Project Architecture
`graph.py` is the main entry point for the program.
### Directories
- The `data/` directory will store the `.gml` files related to graph modelling.
- The `utils/` directory will contain all of the additional `.py` modules used for the program.
  - `helper.py` includes all of the implementation for each of the analysis tests as functions (multi-BFS, connected components, cycles, etc.)
- The `attachments/` directory simply serves images for `README.txt` to display.
