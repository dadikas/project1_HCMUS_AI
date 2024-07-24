from tkinter import *
from variable import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import time


class Program:
    def __init__(self):
        self.root = Tk()
        self.root.withdraw()
        self.file = None
        self.input_path = StringVar()
        self.output_path = StringVar()
        self.car_image = None
        self.car_photo = None
        self.car_id = None

    def select_input_file(self):
        file_path = filedialog.askopenfilename()
        self.input_path.set(file_path)

    def select_output_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        self.output_path.set(file_path)

    def read_input(self, file_path):
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
        return grid, starts, goals, n, m, max_time, max_fuel

    def select_file(self):
        self.root.deiconify()

        Label(self.root, text="Input File:").grid(row=0, column=0, sticky=W, padx=10, pady=5)
        Entry(self.root, textvariable=self.input_path, width=50).grid(row=0, column=1, padx=10, pady=5)
        Button(self.root, text="Browse", command=self.select_input_file).grid(row=0, column=2, padx=10, pady=5)

        Label(self.root, text="Output File:").grid(row=1, column=0, sticky=W, padx=10, pady=5)
        Entry(self.root, textvariable=self.output_path, width=50).grid(row=1, column=1, padx=10, pady=5)
        Button(self.root, text="Browse", command=self.select_output_file).grid(row=1, column=2, padx=10, pady=5)

        Button(self.root, text="Run Algorithm", command=self.run_algorithm).grid(row=2, column=1, pady=20)
        Button(self.root, text="Draw", command=self.visualize_paths).grid(row=3, column=1, pady=10)

        self.root.mainloop()

    def draw(self, grid, paths, n, m):
        def draw_grid(canvas, grid, paths):
            cell_size = 40  # Increase cell size for better visibility
            for i in range(n):
                for j in range(m):
                    if grid[i][j] == IMPASSABLE:
                        color = "black"
                    elif START in grid[i][j]:
                        color = "green"
                    elif GOAL in grid[i][j]:
                        color = "red"
                    elif grid[i][j] == FUEL_STATION:
                        color = "yellow"
                    else:
                        color = "white"
                    canvas.create_rectangle(j * cell_size, i * cell_size, (j + 1) * cell_size, (i + 1) * cell_size,
                                            fill=color, outline="black")
            for path in paths:
                if path:
                    for step in path:
                        canvas.create_rectangle(step[1] * cell_size, step[0] * cell_size, (step[1] + 1) * cell_size,
                                                (step[0] + 1) * cell_size, fill="blue")

            if paths:
                # Load car image
                self.car_image = Image.open("shipper.png")  # Path to your car image
                self.car_image = self.car_image.resize((cell_size, cell_size), Image.ANTIALIAS)
                self.car_photo = ImageTk.PhotoImage(self.car_image)

                # Place car at the start
                start_position = paths[0][0]
                self.car_id = canvas.create_image(start_position[1] * cell_size, start_position[0] * cell_size, anchor=NW, image=self.car_photo)

        def animate_car(canvas, path, cell_size):
            for step in path:
                canvas.coords(self.car_id, step[1] * cell_size, step[0] * cell_size)
                canvas.update()
                time.sleep(0.5)  # Adjust speed as needed

        top = Toplevel(self.root)
        top.title("Paths Visualization")
        canvas = Canvas(top, width=m * 40, height=n * 40)  # Adjust size based on cell size
        canvas.pack()
        draw_grid(canvas, grid, paths)

        if paths:
            animate_car(canvas, paths[0], 40)  # Animate the car along the first path

    def visualize_paths(self):
        try:
            grid, starts, goals, n, m, max_time, max_fuel = self.read_input(self.input_path.get())
            # Example path for demonstration
            paths = [[(1, 1), (1, 2), (1, 3), (2, 3), (3, 3)]]
            self.draw(grid, paths, n, m)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def run_algorithm(self):
        # Implement the algorithm here
        pass

