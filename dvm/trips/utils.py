from collections import deque
from network.models import Edge

def get_shortest_path(start_node, end_node):
    """
    Finds the shortest path between two nodes using Breadth-First Search (BFS).
    Returns a list of node IDs (e.g., [1, 4, 7, 9]) or None if no path exists.
    """
    if start_node == end_node:
        return [start_node.id]

    queue = deque([(start_node.id, [start_node.id])])
    
    # We use a 'set' to remember where we've been so we don't drive in endless circles
    visited = set([start_node.id])

    while queue:
        # 1. Grab the next location to check from our queue
        current_node_id, path = queue.popleft()

        # 2. Look at the database to find ALL roads leaving this exact spot
        outgoing_edges = Edge.objects.filter(from_node_id=current_node_id)
        
        # 3. Check every single place we can drive to from here
        for edge in outgoing_edges:
            neighbor_id = edge.to_node_id

            # Did we just find the destination? 
            if neighbor_id == end_node.id:
                return path + [neighbor_id] # Return the winning route!

            # If it's a new place we haven't checked yet, add it to the queue
            if neighbor_id not in visited:
                visited.add(neighbor_id)
                queue.append((neighbor_id, path + [neighbor_id]))

    # If the queue empties out and we never found the end node, there is no road connecting them
    return None