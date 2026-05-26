from graph import Graph
from zone import Zone
from typing import List, Dict, Optional


def find_path(graph: Graph) -> List[Zone]:
    # On stocke le départ et l'arrivée pour écrire moins de code
    start_node = graph.start
    end_node = graph.end

    if start_node is None or end_node is None:
        return []

    queue = [start_node]

    parent: Dict[Zone, Optional[Zone]] = {start_node: None}

    visited = {start_node}

    # Le petit pousser (BFS)
    while queue:
        current = queue.pop(0)
        if current == end_node:
            break

        for neighbors in current.neighbors:
            if neighbors not in visited:
                visited.add(neighbors)
                parent[neighbors] = current
                queue.append(neighbors)
    path = []
    cur: Optional[Zone] = end_node
    if end_node in parent:
        while cur is not None:
            path.append(cur)
            cur = parent[cur]
    path.reverse()
    return path
