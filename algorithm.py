def find_path(graph):
    # On stocke le départ et l'arrivée pour écrire moins de code
    start_node = graph.start
    end_node = graph.end

    queue = [start_node]

    parent = {start_node: None}

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
    cur = end_node
    if end_node in parent:
        while cur is not None:
            path.append(cur)
            cur = parent[cur]
    path.reverse()
    return path
