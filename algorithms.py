from collections import deque
import heapq

def bfs(grid, start, goal):
    queue = deque([start])
    visited = set()
    parent = {start: None}
    visited_cells = [start]
    yield start

    while queue:
        current = queue.popleft()
        if current == goal:
            break
        if current in visited:
            continue
        visited.add(current)

        r, c = current
        neighbors = [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
        for nr, nc in neighbors:
            if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] in ['0', 'G'] and (nr, nc) not in visited:
                queue.append((nr, nc))
                parent[(nr, nc)] = (r, c)
                visited_cells.append((nr, nc))
                yield (nr, nc)

    path = []
    step = goal
    while step:
        path.append(step)
        step = parent.get(step)
    path.reverse()
    yield path, visited_cells

def dfs(grid, start, goal):
    stack = [start]
    visited = set()
    parent = {start: None}
    visited_cells = [start]
    yield start

    while stack:
        current = stack.pop()
        if current == goal:
            break
        if current in visited:
            continue
        visited.add(current)

        r, c = current
        neighbors = [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
        for nr, nc in neighbors:
            if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] in ['0', 'G'] and (nr, nc) not in visited:
                stack.append((nr, nc))
                parent[(nr, nc)] = (r, c)
                visited_cells.append((nr, nc))
                yield (nr, nc)

    path = []
    step = goal
    while step:
        path.append(step)
        step = parent.get(step)
    path.reverse()
    yield path, visited_cells


def greedy_best_first_search(grid, start, goal):
    pq = [(heuristic(start, goal), start)]
    visited = set()
    parent = {start: None}
    visited_cells = [start]
    yield start

    while pq:
        _, current = heapq.heappop(pq)
        if current == goal:
            break
        if current in visited:
            continue
        visited.add(current)

        r, c = current
        neighbors = [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
        for nr, nc in neighbors:
            if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] in ['0', 'G'] and (nr, nc) not in visited:
                pq.append((heuristic((nr, nc), goal), (nr, nc)))
                parent[(nr, nc)] = (r, c)
                visited_cells.append((nr, nc))
                yield (nr, nc)

    path = []
    step = goal
    while step:
        path.append(step)
        step = parent.get(step)
    path.reverse()
    yield path, visited_cells

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(grid, start, goal):
    pq = [(0 + heuristic(start, goal), start)]
    visited = set()
    parent = {start: None}
    cost = {start: 0}
    visited_cells = [start]
    yield start

    while pq:
        _, current = heapq.heappop(pq)
        if current == goal:
            break
        if current in visited:
            continue
        visited.add(current)

        r, c = current
        neighbors = [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
        for nr, nc in neighbors:
            if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] in ['0', 'G'] and (nr, nc) not in visited:
                new_cost = cost[current] + 1
                if (nr, nc) not in cost or new_cost < cost[(nr, nc)]:
                    cost[(nr, nc)] = new_cost
                    total_cost = new_cost + heuristic((nr, nc), goal)
                    heapq.heappush(pq, (total_cost, (nr, nc)))
                    parent[(nr, nc)] = (r, c)
                    visited_cells.append((nr, nc))
                    yield (nr, nc)

    path = []
    step = goal
    while step:
        path.append(step)
        step = parent.get(step)
    path.reverse()
    yield path, visited_cells



def uniform_cost_search(grid, start, goal):
    pq = [(0, start)]
    visited = set()
    parent = {start: None}
    cost = {start: 0}
    tolls = {start: 0}  # Add tolls dictionary
    visited_cells = [start]
    yield start

    while pq:
        current_cost, current = heapq.heappop(pq)
        if current == goal:
            break
        if current in visited:
            continue
        visited.add(current)

        r, c = current
        neighbors = [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
        for nr, nc in neighbors:
            if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] != '-1' and (nr, nc) not in visited:
                toll = (1 + int(grid[nr][nc])) if grid[nr][nc] not in ['0', 'S', 'G'] else 1
                new_cost = current_cost + 1 + toll
                if (nr, nc) not in cost or new_cost < cost[(nr, nc)]:
                    cost[(nr, nc)] = new_cost
                    tolls[(nr, nc)] = tolls[current] + toll  # Track tolls
                    heapq.heappush(pq, (new_cost, (nr, nc)))
                    parent[(nr, nc)] = (r, c)
                    visited_cells.append((nr, nc))
                    yield (nr, nc)

    path = []
    toll_path = []
    step = goal
    while step:
        path.append(step)
        toll_path.append(tolls[step])
        step = parent.get(step)
    path.reverse()
    toll_path.reverse()
    yield path, visited_cells, toll_path


# def uniform_cost_search(grid, start, goal):
#     pq = [(0, start)]
#     visited = set()
#     parent = {start: None}
#     cost = {start: 0}
#     visited_cells = [start]
#     yield start

#     while pq:
#         current_cost, current = heapq.heappop(pq)
#         if current == goal:
#             break
#         if current in visited:
#             continue
#         visited.add(current)

#         r, c = current
#         neighbors = [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
#         for nr, nc in neighbors:
#             if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] != '-1' and (nr, nc) not in visited:
#                 toll = int(grid[nr][nc]) if grid[nr][nc] not in ['0', 'S', 'G'] else 0
#                 new_cost = current_cost + 1 + toll
#                 if (nr, nc) not in cost or new_cost < cost[(nr, nc)]:
#                     cost[(nr, nc)] = new_cost
#                     heapq.heappush(pq, (new_cost, (nr, nc)))
#                     parent[(nr, nc)] = (r, c)
#                     visited_cells.append((nr, nc))
#                     yield (nr, nc)

#     path = []
#     step = goal
#     while step:
#         path.append(step)
#         step = parent.get(step)
#     path.reverse()
#     yield path, visited_cells
# def manhattan_distance(current, goal):
    return abs(current[0] - goal[0]) + abs(current[1] - goal[1])

# def a_star(grid, start, goal, fuel_capacity):
    pq = [(0, start, fuel_capacity, 0)]  # Priority queue includes (total cost, current cell, remaining fuel, accumulated toll cost)
    visited = set()
    parent = {start: None}
    cost = {start: 0}
    toll_costs = {start: 0}
    visited_cells = [start]
    yield start

    while pq:
        current_cost, current, fuel, current_toll = heapq.heappop(pq)
        if current == goal:
            break
        if (current, fuel) in visited:
            continue
        visited.add((current, fuel))

        r, c = current
        neighbors = [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
        for nr, nc in neighbors:
            if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] != '-1':
                new_fuel = fuel - 1
                if grid[nr][nc].startswith('F'):
                    new_fuel = fuel_capacity  # Refuel at the fuel station
                if new_fuel < 0:
                    continue  # Skip this neighbor if there isn't enough fuel

                toll = int(grid[nr][nc]) if grid[nr][nc].isdigit() else 0
                new_cost = current_cost + 1 + toll
                heuristic = manhattan_distance((nr, nc), goal)
                total_cost = new_cost + heuristic
                if (nr, nc) not in cost or new_cost < cost[(nr, nc)]:
                    cost[(nr, nc)] = new_cost
                    toll_costs[(nr, nc)] = toll
                    heapq.heappush(pq, (total_cost, (nr, nc), new_fuel, toll))
                    parent[(nr, nc)] = (r, c)
                    visited_cells.append((nr, nc))
                    yield (nr, nc)

    path = []
    toll_path = []
    step = goal
    while step:
        path.append(step)
        toll_path.append(toll_costs.get(step, 0))
        step = parent.get(step)
    path.reverse()
    toll_path.reverse()
    yield path, visited_cells, toll_path
