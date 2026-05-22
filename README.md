*This project has been created as part of the 42 curriculum by guifouqu.*

# Fly In

## Description

Fly In is an algorithmic project with the goal of optimizing the movement of a fleet of drones through a network of zones (a graph) while respecting various constraints, particularly the capacity of the links between the zones. The project includes a customized map parser, a pathfinding algorithm to find the optimized routes, and a static visual representation system.

### Features
- Map parser to generate the underlying graph structure (zones and connections).
- Pathfinding algorithm to safely guide all drones from the start zone to the end zone.
- Command-line display of the initial state (`L<ID>-<Zone>`) and continuous drone movements at each "tick" (`D<ID>-<Zone>`).
- Static graphical visualization of the map at the end of the simulation.
- Various maps available with scaling difficulty levels: *easy*, *medium*, *hard*, and *challenger*.
- Built-in static type checking and linting tools.

## Instructions

### Prerequisites
- Python 3.x
- `pip` package manager or the provided `Makefile`.

### Installation
1. Clone this repository or navigate to the project folder.
2. Activate your virtual environment (recommended):
   ```bash
   source .venv/bin/activate
   ```
3. Install the necessary dependencies using the `make` command:
   ```bash
   make install
   ```
   *This will install `matplotlib`, `rich`, `flake8`, and `mypy`.*

### Execution
You can use the provided `Makefile` to easily run the project:

```bash
make run maps/easy/02_simple_fork.txt
```
*(If no argument is provided, a default map will be launched).*

**Other available Makefile commands:**
- `make debug ARGS="maps/easy/02_simple_fork.txt"` : Launch the program in debug mode with `pdb`.
- `make lint` : Run the `flake8` linter (PEP8 standard) and the `mypy` static typing tool.
- `make clean` : Clean the workspace by removing `__pycache__` and `.mypy_cache` directories.

### Example Output
```text
L1-Start L2-Start L3-Start
D1-ZoneA D2-ZoneA
D1-ZoneB D3-ZoneA
...
50 tick
----- Affichage de la map -----
```
*The program will then open a window to visualize the map's topology.*

## Algorithm Choices and Implementation Strategy

To solve the drone routing problem, our pathfinding strategy revolves around treating the zones and links as a flow network. 
- **Breadth-First Search (BFS)**: We chose BFS as the core graph traversal algorithm. BFS guarantees the discovery of the shortest path in an unweighted graph, minimizing the total ticks required for a single drone.
- **Link Capacities**: As drones navigate the graph simultaneously, we manage bottlenecks by accounting for the maximum drone capacity allowed on each connection during a given tick. If a path is fully saturated, following drones must either wait or seek alternative routes.
- **Drone Coordination**: We process drone movements sequentially per tick. Drones closest to their destination are evaluated first to prevent deadlocks and ensure a continuous flow towards the destination.

## Visual Representation

To enhance the user experience, we implemented a static graph visualization that triggers upon the completion of the pathfinding routing. 
- **Matplotlib Integration**: Generates a clean graphical plot of the network topology allowing users to visualize the actual layout of the simulated environment.
- **Nodes & Edges**: Zones are plotted as distinct nodes, while connections are drawn as connecting edges.
- **UX Enhancement**: Reading logs composed of thousands of text lines (`D1-ZoneA D2-ZoneA`) is extremely difficult. The visual topology grounds the simulation data in an intuitive diagram, making it trivial for the user to understand map complexities, bottlenecks, and the structural challenges they pose.

## Resources

- [Matplotlib - Home](https://matplotlib.org/stable/index.html)
- [Matplotlib - Pyplot Tutorials](https://matplotlib.org/stable/tutorials/pyplot.html)
- [Mypy - Getting Started](https://mypy.readthedocs.io/en/stable/getting_started.html)
- [GeeksforGeeks - Breadth First Search (BFS)](https://www.geeksforgeeks.org/dsa/breadth-first-search-or-bfs-for-a-graph/?ref=3dongcode.com)

**AI Usage**
Artificial Intelligence was used to assist in the development of this project:
- **Code Generation & Boilerplate**: Assisting in creating standard Makefile instructions, repetitive class structures, and setting up visualization syntax.
- **Documentation**: Structuring, formatting, and translating the project README to English to align with explicit requirements.
- **Refactoring & Tooling**: Explaining linting best practices and typing validation checks with mypy and flake8.
