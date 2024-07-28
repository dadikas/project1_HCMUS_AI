from heapq import heappop, heappush
from collections import deque
from variable import IMPASSABLE

def bfs(grid, start, goal, n, m):
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    queue = deque([(start, [start])])
    visited = set()
    visited.add(start)
    steps = []

    while queue:
        (x, y), path = queue.popleft()
        steps.append((x, y))

        if (x, y) == goal:
            return path, steps

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < m and (nx, ny) not in visited:
                if grid[nx][ny] != IMPASSABLE:
                    visited.add((nx, ny))
                    queue.append(((nx, ny), path + [(nx, ny)]))

    return [start], steps

def dfs(grid, start, goal, n, m):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    stack = [(start, [])]
    visited = set()
    visited.add(start)
    steps = []

    while stack:
        (current, path) = stack.pop()
        path = path + [current]
        steps.append(current)

        if current == goal:
            return path, steps

        for direction in directions:
            next_pos = (current[0] + direction[0], current[1] + direction[1])
            if 0 <= next_pos[0] < n and 0 <= next_pos[1] < m:
                if grid[next_pos[0]][next_pos[1]] != IMPASSABLE and next_pos not in visited:
                    stack.append((next_pos, path))
                    visited.add(next_pos)

    return [start], steps

def uniform_cost_search(grid, start, goal, n, m):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    heap = [(0, start, [])]
    visited = set()
    visited.add(start)
    steps = []

    while heap:
        (cost, current, path) = heappop(heap)
        path = path + [current]
        steps.append(current)

        if current == goal:
            return path, steps

        for direction in directions:
            next_pos = (current[0] + direction[0], current[1] + direction[1])
            if 0 <= next_pos[0] < n and 0 <= next_pos[1] < m:
                if grid[next_pos[0]][next_pos[1]] != IMPASSABLE and next_pos not in visited:
                    heappush(heap, (cost + 1, next_pos, path))
                    visited.add(next_pos)

    return [start], steps
def greedy_best_first_search(grid, start, goal, n, m):
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    heap = [(0, start, [])]
    visited = set()
    visited.add(start)
    path = []  # Final path to goal
    steps = []  # All nodes visited during search

    while heap:
        cost, current, current_path = heappop(heap)
        current_path = current_path + [current]
        steps.append(current)

        if current == goal:
            path = current_path
            break  # Exit while loop when goal is reached

        for direction in directions:
            next_pos = (current[0] + direction[0], current[1] + direction[1])
            if 0 <= next_pos[0] < n and 0 <= next_pos[1] < m:
                if grid[next_pos[0]][next_pos[1]] != IMPASSABLE and next_pos not in visited:
                    heappush(heap, (heuristic(next_pos, goal), next_pos, current_path))
                    visited.add(next_pos)

    return path if path else [start], steps


def a_star(grid, start, goal, n, m):
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    heap = [(0, start, [])]
    visited = set()
    visited.add(start)
    steps = []

    while heap:
        (cost, current, path) = heappop(heap)
        path = path + [current]
        steps.append(current)

        if current == goal:
            return path, steps

        for direction in directions:
            next_pos = (current[0] + direction[0], current[1] + direction[1])
            if 0 <= next_pos[0] < n and 0 <= next_pos[1] < m:
                if grid[next_pos[0]][next_pos[1]] != IMPASSABLE and next_pos not in visited:
                    heappush(heap, (cost + heuristic(next_pos, goal), next_pos, path))
                    visited.add(next_pos)

    return [start], steps


def shortest_path_with_toll_lv2(grid, start, goal, max_time, n, m):
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    heap = []
    heappush(heap, (0 + heuristic(start, goal), 0, start))  # (estimated_total_cost, current_cost, position)
    cost = {start: 0}
    path = {start: None}
    steps = []

    while heap:
        estimated_total_cost, current_cost, current = heappop(heap)
        steps.append(current)

        if current == goal:
            final_path = []
            while current is not None:
                final_path.append(current)
                current = path[current]
            final_path.reverse()
            return final_path, steps, current_cost

        for direction in directions:
            next_x, next_y = current[0] + direction[0], current[1] + direction[1]
            if 0 <= next_x < n and 0 <= next_y < m:
                cell_value = grid[next_x][next_y]

                # Skip impassable cells
                if cell_value == IMPASSABLE:
                    continue

                # Calculate move cost and wait cost
                move_cost = 1
                wait_cost = int(cell_value) if cell_value.isdigit() else 0
                total_cost = current_cost + move_cost + wait_cost

                if total_cost <= max_time:
                    next_position = (next_x, next_y)
                    if next_position not in cost or total_cost < cost[next_position]:
                        cost[next_position] = total_cost
                        path[next_position] = current
                        estimated_total_cost = total_cost + heuristic(next_position, goal)
                        heappush(heap, (estimated_total_cost, total_cost, next_position))

    # If no path is found, return the steps and a path containing only the start
    return [start], steps, float('inf')


def find_fuel_stations(grid, n, m):
    fuel_stations = set()
    toll_booths = set()
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 'F':
                fuel_stations.add((i, j))
            elif grid[i][j] == 'T':
                toll_booths.add((i, j))
    return fuel_stations, toll_booths


def shortest_path_with_toll_lv3(grid, start, goal, max_time, n, m, max_fuel):
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    fuel_stations, toll_booths = find_fuel_stations(grid, n, m)
    heap = [(0, start, max_fuel, 0, [start])]  # (heuristic, position, fuel, time, path)
    visited = set()
    steps = []

    while heap:
        _, current, current_fuel, current_time, current_path = heappop(heap)

        if current not in steps:
            steps.append(current)

        if current == goal:
            return current_path, steps, current_time

        if current_fuel <= 0 or current_time > max_time:
            continue

        visited.add((current, current_fuel))

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for direction in directions:
            next_position = (current[0] + direction[0], current[1] + direction[1])

            if 0 <= next_position[0] < n and 0 <= next_position[1] < m:
                if grid[next_position[0]][next_position[1]] != IMPASSABLE:
                    next_fuel = current_fuel - 1

                    if next_position in toll_booths:
                        next_fuel += 1  # No fuel consumption at toll booths

                    if next_position in fuel_stations:
                        next_fuel = max_fuel  # Refuel to full capacity

                    if (next_position, next_fuel) not in visited:
                        heappush(heap, (heuristic(next_position, goal), next_position, next_fuel, current_time + 1,
                                        current_path + [next_position]))

    return [start], steps, float('inf')
        

        
 