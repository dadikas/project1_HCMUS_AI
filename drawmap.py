from tkinter import *
from variable import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import time
import algorithms

class Program:
    def __init__(self):
        self.root = Tk()
        self.root.withdraw()  # Start with the root window hidden
        self.file = None
        self.input_path = StringVar()
        self.output_path = StringVar()
        self.time_limit = StringVar()
        self.fuel_limit = StringVar()
        self.vehical_image = None
        self.vehical_photo = None
        self.vehical_id = None
        self.algorithm = StringVar(value="BFS")

    def select_input_file(self):
        """Open file dialog to select an input file."""
        file_path = filedialog.askopenfilename()
        self.input_path.set(file_path)

    def select_output_file(self):
        """Open file dialog to select an output file."""
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                               filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        self.output_path.set(file_path)

    def read_input(self, file_path):
        """Read grid configuration from input file."""
        try:
            with open(file_path, 'r') as file:
                n, m, max_time, max_fuel = map(int, file.readline().strip().split())
                grid = []
                starts = []
                goals = []
                for i in range(n):
                    row = file.readline().strip().split()
                    for j in range(m):
                        if START in row[j]:
                            starts.append((i, j))
                        elif GOAL in row[j]:
                            goals.append((i, j))
                    grid.append(row)
            return grid, starts, goals, n, m
        except Exception as e:
            raise ValueError(f"Failed to read input file: {e}")

    def select_file(self):
        """Display file selection dialog and setup the UI."""
        self.root.deiconify()
        Label(self.root, text="Input File:").grid(row=0, column=0, sticky=W, padx=10, pady=5)
        Entry(self.root, textvariable=self.input_path, width=50).grid(row=0, column=1, padx=10, pady=5)
        Button(self.root, text="Browse", command=self.select_input_file).grid(row=0, column=2, padx=10, pady=5)

        Label(self.root, text="Output File:").grid(row=1, column=0, sticky=W, padx=10, pady=5)
        Entry(self.root, textvariable=self.output_path, width=50).grid(row=1, column=1, padx=10, pady=5)
        Button(self.root, text="Browse", command=self.select_output_file).grid(row=1, column=2, padx=10, pady=5)

        Label(self.root, text="Time limit:").grid(row=2, column=0, sticky=W, padx=10, pady=5)
        Entry(self.root, textvariable=self.time_limit, width=50).grid(row=2, column=1, padx=10, pady=5)
        Label(self.root, text="Fuel limit:").grid(row=3, column=0, sticky=W, padx=10, pady=5)
        Entry(self.root, textvariable=self.fuel_limit, width=50).grid(row=3, column=1, padx=10, pady=5)

        Label(self.root, text="Algorithm:").grid(row=4, column=0, sticky=W, padx=10, pady=5)
        OptionMenu(self.root, self.algorithm, "BFS", "DFS", "UCS", "Greedy Best-First Search", "A*").grid(row=4, column=1, padx=10, pady=5)

        Button(self.root, text="Run Algorithm", command=self.run_algorithm).grid(row=5, column=1, pady=20)
        Button(self.root, text="Draw", command=self.visualize_paths).grid(row=6, column=1, pady=10)
        Button(self.root, text="Run level 2", command=self.run_algorithm_level2).grid(row=7, column=1, pady=20)
        Button(self.root, text="Run level 3", command=self.run_algorithm_level3).grid(row=8, column=1, pady=20)

        self.root.mainloop()

    def draw_grid(self, canvas, grid, paths, n, m):
        """Draw the grid and paths on the canvas."""
        cell_size = 40
        for i in range(n):
            for j in range(m):
                color = {
                    IMPASSABLE: "black",
                    START: "green",
                    GOAL: "red",
                    FUEL_STATION: "yellow"
                }.get(grid[i][j], "white")
                canvas.create_rectangle(j * cell_size, i * cell_size,
                                        (j + 1) * cell_size, (i + 1) * cell_size,
                                        fill=color, outline="black")
                if grid[i][j].isdigit() and grid[i][j] != '0':
                    canvas.create_text((j * cell_size + (j + 1) * cell_size) // 2,
                                       (i * cell_size + (i + 1) * cell_size) // 2,
                                       text=grid[i][j], fill="black")

    def animate_steps(self, canvas, steps, cell_size):
        """Animate the steps on the canvas."""
        for step in steps:
            x, y = step
            canvas.create_oval(y * cell_size + cell_size // 4,
                               x * cell_size + cell_size // 4,
                               y * cell_size + 3 * cell_size // 4,
                               x * cell_size + 3 * cell_size // 4,
                               fill="grey", outline="black")
            canvas.update()
            time.sleep(0.5)

    def animate_car(self, canvas, path, cell_size):
        """Animate the car image along the path."""
        for step in path:
            canvas.coords(self.vehical_id, step[1] * cell_size, step[0] * cell_size)
            canvas.update()
            time.sleep(0.5)

    def draw(self, grid, paths, steps, n, m):
        """Draw and animate the grid, paths, and steps."""
        cell_size = 40
        top = Toplevel(self.root)
        top.title("Paths and Steps Visualization")
        canvas = Canvas(top, width=m * cell_size, height=n * cell_size)
        canvas.pack()
        self.draw_grid(canvas, grid, paths, n, m)

        if steps:
            self.animate_steps(canvas, steps, cell_size)
        for path in paths:
            if path:
                for k in range(len(path) - 1):
                    start_x = path[k][1] * cell_size + cell_size // 2
                    start_y = path[k][0] * cell_size + cell_size // 2
                    end_x = path[k + 1][1] * cell_size + cell_size // 2
                    end_y = path[k + 1][0] * cell_size + cell_size // 2
                    canvas.create_line(start_x, start_y, end_x, end_y, fill="blue", width=2)

        if paths:
            self.vehical_image = Image.open("shipper.png")
            self.vehical_image = self.vehical_image.resize((cell_size, cell_size), Image.Resampling.LANCZOS)
            self.vehical_photo = ImageTk.PhotoImage(self.vehical_image)
            start_position = paths[0][0]
            self.vehical_id = canvas.create_image(start_position[1] * cell_size, start_position[0] * cell_size, anchor=NW, image=self.vehical_photo)
            self.animate_car(canvas, paths[0], cell_size)

    def visualize_paths(self):
        """Read output file and visualize paths."""
        try:
            grid, starts, goals, n, m = self.read_input(self.input_path.get())
            paths = []
            steps = []

            with open(self.output_path.get(), 'r') as file:
                for line in file:
                    line = line.strip()
                    if line.startswith("Path:"):
                        path = [tuple(map(int, pos.strip('()').split(','))) for pos in line.strip('Path: []').split('), (')]
                        paths.append(path)
                    elif line.startswith("Steps:"):
                        steps = [tuple(map(int, pos.strip('()').split(','))) for pos in line.strip('Steps: []').split('), (')]

            self.draw(grid, paths, steps, n, m)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def run_algorithm(self):
        """Run the selected algorithm and save results to output file."""
        try:
            grid, starts, goals, n, m = self.read_input(self.input_path.get())
            algorithm = self.algorithm.get()
            all_paths = []
            all_steps = []

            algorithm_mapping = {
                "BFS": algorithms.bfs,
                "DFS": algorithms.dfs,
                "UCS": algorithms.uniform_cost_search,
                "Greedy Best-First Search": algorithms.greedy_best_first_search,
                "A*": algorithms.a_star
            }

            if algorithm in algorithm_mapping:
                func = algorithm_mapping[algorithm]
                for start in starts:
                    for goal in goals:
                        path, steps = func(grid, start, goal, n, m)
                        all_paths.append(path)
                        all_steps.append(steps)
            else:
                raise ValueError(f"Unsupported algorithm: {algorithm}")

            with open(self.output_path.get(), 'w') as file:
                for path, steps in zip(all_paths, all_steps):
                    file.write(f"Path: {path}\n")
                    file.write(f"Steps: {steps}\n")
            messagebox.showinfo("Success", "Algorithm completed successfully and output saved.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def run_algorithm_level2(self):
        """Run the level 2 algorithm considering toll costs and save results to the output file."""
        try:
            grid, starts, goals, n, m = self.read_input(self.input_path.get())
            time_limit = int(self.time_limit.get())
            all_paths = []
            all_steps = []

            for start in starts:
                for goal in goals:
                    path, steps, total_cost = algorithms.shortest_path_with_toll_lv2(grid, start, goal,time_limit,n,m )
                    all_paths.append(path)
                    all_steps.append(steps)

            with open(self.output_path.get(), 'w') as file:
                for path, steps in zip(all_paths, all_steps):
                    file.write(f"Path: {path}\n")
                    file.write(f"Steps: {steps}\n")
            messagebox.showinfo("Success", "Level 2 algorithm completed successfully and output saved.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    def run_algorithm_level3(self):
        """Run the level 3 algorithm considering toll costs and fuel constraints and save results to the output file."""
        try:
            grid, starts, goals, n, m = self.read_input(self.input_path.get())
            time_limit = int(self.time_limit.get())
            fuel_limit = int(self.fuel_limit.get())
            all_paths = []
            all_steps = []

            for start in starts:
                for goal in goals:
                    path, steps, total_cost = algorithms.shortest_path_with_toll_lv3(grid, start, goal, time_limit, n, m, fuel_limit)
                    all_paths.append(path)
                    all_steps.append(steps)

            with open(self.output_path.get(), 'w') as file:
                for path, steps in zip(all_paths, all_steps):
                    file.write(f"Path: {path}\n")
                    file.write(f"Steps: {steps}\n")
            messagebox.showinfo("Success", "Level 3 algorithm completed successfully and output saved.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

