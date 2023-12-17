from BFSDemo import BFS
from DFSDemo import DFS
from pyamaze import maze, agent, COLOR, textLabel
from timeit import timeit
from PIL import Image, ImageDraw
import datetime
import csv


class MyMaze(maze):
    def savepng(self, maze_map, fwdBFSPath, fwdDFSPath):
        dt_image = datetime.datetime.now().strftime("%d--%H-%M")
        # Create an image
        image_size = (450, 650)  # Adjust the size as needed
        maze_image = Image.new("RGB", image_size, "white")
        draw = ImageDraw.Draw(maze_image)

        # Draw your maze on the image
        # Modify this part based on your maze representation
        cell_size = 20  # Adjust the cell size as needed
        for k, v in maze_map.items():
            # Modify the drawing logic based on your maze structure
            y, x = k  # Assuming k is a tuple (x, y) representing coordinates
            if v['W'] == 0:  # Assuming 'W' represents a wall in the west direction
                draw.rectangle([(x * cell_size, y * cell_size), (x * cell_size, (y + 1) * cell_size)],
                               fill="black")
            if v['E'] == 0:  # Assuming 'E' represents a wall in the east direction
                draw.rectangle([((x + 1) * cell_size, y * cell_size), ((x + 1) * cell_size, (y + 1) * cell_size)],
                               fill="black")
            if v['N'] == 0:  # Assuming 'N' represents a wall in the north direction
                draw.rectangle([(x * cell_size, y * cell_size), ((x + 1) * cell_size, y * cell_size)],
                               fill="black")
            if v['S'] == 0:  # Assuming 'S' represents a wall in the south direction
                draw.rectangle([(x * cell_size, (y + 1) * cell_size), ((x + 1) * cell_size, (y + 1) * cell_size)],
                               fill="black")
            if (y,x) == (ym,xm):
                cell_center_x = (x + 0.5) * cell_size
                cell_center_y = (y + 0.5) * cell_size
                footprint_size = cell_size * 0.8  # Adjust the size as needed
                outline_thickness = 1  # Adjust the thickness of the outline as needed
                draw.rectangle([(cell_center_x - footprint_size / 2 + outline_thickness,
                                 cell_center_y - footprint_size / 2 + outline_thickness),
                                (cell_center_x + footprint_size / 2 - outline_thickness,
                                 cell_center_y + footprint_size / 2 - outline_thickness)],
                               fill="red")

            if (y,x) == (my,mx):
                cell_center_x = (x + 0.5) * cell_size
                cell_center_y = (y + 0.5) * cell_size
                footprint_size = cell_size * 0.8  # Adjust the size as needed
                outline_thickness = 1  # Adjust the thickness of the outline as needed
                draw.rectangle([(cell_center_x - footprint_size / 2 + outline_thickness,
                                 cell_center_y - footprint_size / 2 + outline_thickness),
                                (cell_center_x + footprint_size / 2 - outline_thickness,
                                 cell_center_y + footprint_size / 2 - outline_thickness)],
                               fill="green")
            # Draw footprints for agent a
            if (y, x) in fwdBFSPath.values():
                cell_center_x = (x + 0.5) * cell_size
                cell_center_y = (y + 0.5) * cell_size
                footprint_size = cell_size * 0.8  # Adjust the size as needed
                outline_thickness = 1  # Adjust the thickness of the outline as needed
                draw.rectangle([(cell_center_x - footprint_size / 3 + outline_thickness,
                                 cell_center_y - footprint_size / 3 + outline_thickness),
                                (cell_center_x + footprint_size / 3 - outline_thickness,
                                 cell_center_y + footprint_size / 3 - outline_thickness)],
                               fill="cyan")

            # Draw footprints for agent b
            if (y, x) in fwdDFSPath.values():
                cell_center_x = (x + 0.5) * cell_size
                cell_center_y = (y + 0.5) * cell_size
                footprint_size = cell_size * 0.8  # Adjust the size as needed
                outline_thickness = 1  # Adjust the thickness of the outline as needed
                draw.rectangle([(cell_center_x - footprint_size / 4 + outline_thickness,
                                 cell_center_y - footprint_size / 4 + outline_thickness),
                                (cell_center_x + footprint_size / 4 - outline_thickness,
                                 cell_center_y + footprint_size / 4 - outline_thickness)],
                               fill="yellow")

        # Save the image
        maze_image.save(f'maze--{dt_image}.png')

    def read_maze_from_csv(self, csv_file):
        maze_map = {}
        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            for row in reader:
                k = eval(row[0])  # Assuming the first column is the coordinate tuple
                v = {direction: int(value) for direction, value in zip(['E', 'W', 'N', 'S'], row[1:])}
                maze_map[k] = v
        return maze_map

ym = 1
xm = 1
xx = 9
yy = 9
mx = 10
my = 10
m = MyMaze(mx, my)
m.CreateMaze(ym, xm, loopPercent=100)

searchPath, dfsPath, fwdDFSPath = DFS(m)
bSearch, bfsPath, fwdBFSPath = BFS(m)

textLabel(m, 'DFS Path Length', len(fwdDFSPath) + 1)
textLabel(m, 'BFS Path Length', len(fwdBFSPath) + 1)
textLabel(m, 'DFS Search Length', len(searchPath) + 1)
textLabel(m, 'BFS Search Length', len(bSearch) + 1)

a = agent(m, footprints=True, color=COLOR.cyan, filled=True)
b = agent(m, footprints=True, color=COLOR.yellow)
m.tracePath({a: fwdBFSPath}, delay=100)
m.tracePath({b: fwdDFSPath}, delay=100)


t1 = timeit(stmt='DFS(m)', number=1000, globals=globals())
t2 = timeit(stmt='BFS(m)', number=1000, globals=globals())

textLabel(m, 'DFS Time', t1)
textLabel(m, 'BFS Time', t2)

maze_map_from_csv = m.read_maze_from_csv(f'maze--{datetime.datetime.now().strftime("%d--%H-%M")}.csv')
m.savepng(maze_map_from_csv, fwdBFSPath, fwdDFSPath)
m.run()

