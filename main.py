import pygame
import sys
import argparse
from drawmap import draw_grid
from algorithms import bfs, dfs, uniform_cost_search, greedy_best_first_search, a_star
from variable import *

def read_file(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            # Parse the first line for metadata
            n, m, t, f = map(int, lines[0].strip().split())
            # Parse the rest of the lines for the grid
            grid = [line.strip().split() for line in lines[1:]]
        return n, m, t, f, grid
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit()
    except ValueError as e:
        print(f"Error: Invalid data format. {e}")
        sys.exit()

def find_start_goal(grid):
    start = None
    goal = None
    for row_idx, row in enumerate(grid):
        for col_idx, cell in enumerate(row):
            if cell == 'S':
                start = (row_idx, col_idx)
            elif cell == 'G':
                goal = (row_idx, col_idx)
    return start, goal

def main(level: str, algo: str, file: str):
    # Read the input file
    n, m, t, f, grid = read_file(file)
    
    # Find start and goal positions
    start, goal = find_start_goal(grid)
    if not start or not goal:
        print("Error: Start or goal not found in the grid.")
        sys.exit()
    
    # Set up Pygame
    pygame.init()
    cell_size = 50
    width = m * cell_size
    height = n * cell_size
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Grid Display")

    # Select the algorithm based on command-line argument
    algorithm_map = {
        'bfs': bfs,
        'dfs': dfs,
        'ucs': uniform_cost_search,
        'greedy': greedy_best_first_search,
        'a_star': a_star
    }
    if algo not in algorithm_map:
        print(f"Error: Algorithm '{algo}' is not recognized.")
        sys.exit()

    path = None
    visited_cells = []
    toll_path = []
    # Check level and adjust behavior if needed
    if level == 'level_1':
        print('Using level_1 settings.')
        selected_algorithm = algorithm_map[algo]
        algorithm_generator = selected_algorithm(grid, start, goal)
    elif level == 'level_2':
        # For level_2, using UCS algorithm
        if algo == 'ucs':
            print("Warning: For level_2, UCS algorithm is used.")
            selected_algorithm = uniform_cost_search
            algorithm_generator = selected_algorithm(grid, start, goal)
    elif level == 'level_3':
        selected_algorithm = a_star
        algorithm_generator = selected_algorithm(grid, start, goal)
        print('Using level_3 settings.')
    else:
        print('Using default level_1 settings.')

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        screen.fill(WHITE)
        
        try:
            current = next(algorithm_generator)
            if isinstance(current, tuple) and isinstance(current[0], list):
                path = current[0]
                visited_cells = current[1]
                toll_path = current[2] if algo == 'ucs' else 0
                current = None
            elif isinstance(current, tuple):
                visited_cells.append(current)
        except StopIteration:
            # running = False
            # print("To Completed")
            current = None

        draw_grid(screen, grid, cell_size, visited_cells, path)
        pygame.display.flip()
        pygame.time.delay(10)  # Adjust the delay for visualization speed

    # Print the tolls at the end of the sea`rch
    if path and toll_path:
        print("Path found:")
        for idx, step in enumerate(path):
            print(f"Step: {step}, Toll: {toll_path[idx]}")

if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Choose search algorithm, level, and input file.")
    parser.add_argument('--level', help='Specify the level', type=str, default='level_1')
    parser.add_argument('--algorithm', help='Search algorithm to use', default='bfs', type=str)
    parser.add_argument('--file', help='Input file name', default='input_level1.txt', type=str)
    args = parser.parse_args()
    
    # Call the main function with the command-line arguments
    main(args.level, args.algorithm, args.file)
