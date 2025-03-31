# The below import are all that should be used in this assignment. Additional libraries are not allowed.
import numpy as np
import math
import scipy.sparse.csgraph
import matplotlib.pyplot as plt
import random
import argparse
import csv

'''
==============================
The code below here is for my additional classes
==============================
'''


class MapContainer:

    def __init__(self, map_data):
        self.grid_size = map_data[0]
        self.start_pos = map_data[1]
        self.goal_pos = map_data[2]
        self.obstacles = [Obstacle(ob) for ob in map_data[3]]


class Obstacle:

    def __init__(self, obstacle_data):
        self.x = obstacle_data[0]
        self.y = obstacle_data[1]
        self.radius = obstacle_data[2]

    def intersects(self, cell_x, cell_y, cell_size):

        half_cell = cell_size / 2

        # Convert array indices to grid coordinates
        x_scaled = (cell_x * cell_size) + half_cell
        y_scaled = (cell_y * cell_size) + half_cell

        # Find the absolute difference between centre of the cell and the centre of circle along each axis
        x_dif = abs(self.x - x_scaled)
        y_dif = abs(self.y - y_scaled)

        # Check if circle is horizontally or vertically too far to intersect
        if x_dif > (half_cell + self.radius):
            return False
        if y_dif > (half_cell + self.radius):
            return False

        # Check if centre of the circle is in the cell
        if x_dif <= half_cell:
            return True
        if y_dif <= half_cell:
            return True

        # If none of the above are true find the distance between the nearest corner and the centre
        corner_distance_sq = (x_dif - half_cell) ** 2 + (y_dif - half_cell) ** 2

        # If the distance is less than or equal to the radius they must intersect
        return corner_distance_sq <= self.radius ** 2


class Node:

    def __init__(self, parent, coord):
        self.parent = parent
        self.coord = coord

    def x(self):
        return self.coord[0]

    def y(self):
        return self.coord[1]

    def find_path(self, path, start):
        """
        Recursive search for path to node, base case = start
        """

        path.append(self.coord)

        if self.coord == start:
            path = path
            return path
        return self.parent.find_path(path, start)

    def __str__(self):

        if self.parent:
            return (f'Node Object: {[round(cc, 2) for cc in self.coord]}, '
                    f'Parent {[round(cc, 2) for cc in self.parent.coord]}')

        return f'Node Object: {[round(cc, 2) for cc in self.coord]}, Parent (Root)'


'''
==============================
The code below here is for my additional functions
==============================
'''


def str_list_to_int_tuple(row: list[str]) -> tuple[int, ...]:
    # Convert list of strings to list of integers
    row_ints = [int(rr) for rr in row]

    # Convert list of integers to tuple of integers
    row_tuple = tuple(row_ints)

    return row_tuple


'''
==============================


████▄ ▄█▄    ▄█▄      ▄   █ ▄▄  ██      ▄   ▄█▄  ▀▄    ▄        ▄▄▄▄▄   ████▄ █       ▄     ▄▄▄▄▀ ▄█ ████▄    ▄   
█   █ █▀ ▀▄  █▀ ▀▄     █  █   █ █ █      █  █▀ ▀▄  █  █        █     ▀▄ █   █ █        █ ▀▀▀ █    ██ █   █     █  
█   █ █   ▀  █   ▀  █   █ █▀▀▀  █▄▄█ ██   █ █   ▀   ▀█       ▄  ▀▀▀▀▄   █   █ █     █   █    █    ██ █   █ ██   █ 
▀████ █▄  ▄▀ █▄  ▄▀ █   █ █     █  █ █ █  █ █▄  ▄▀  █         ▀▄▄▄▄▀    ▀████ ███▄  █   █   █     ▐█ ▀████ █ █  █ 
      ▀███▀  ▀███▀  █▄ ▄█  █       █ █  █ █ ▀███▀ ▄▀                              ▀ █▄ ▄█  ▀       ▐       █  █ █ 
                     ▀▀▀    ▀     █  █   ██                                          ▀▀▀                   █   ██ 
                                 ▀                                                                                

==============================
'''


def read_map_from_file(filename):
    """
    This functions reads a csv file describing a map and returns the map data
    Inputs:
        - filename (string): name of the file to read
    Outputs:
        - map (tuple): A map is a tuple of the form (grid_size, start_pos, goal_pos, [obstacles])
            grid_size is a tuple (length, height) representing the size of the map
            start_pos is a tuple (x, y) representing the x,y coordinates of the start position
            goal_pos is a tuple (x, y) representing the x,y coordinate of the goal position
            obstacles is a list of tuples. Each tuple represents a single  circular obstacle and
            is of the form (x, y, radius).
                x is an integer representing the x coordinate of the obstacle
                y is an integer representing the y coordinate of the obstacle
                radius is an integer representing the radius of the obstacle
    """

    with open(filename, mode='r') as file:
        reader = csv.reader(file)

        grid_size = str_list_to_int_tuple(next(reader))

        start_pos = str_list_to_int_tuple(next(reader))
        goal_pos = str_list_to_int_tuple(next(reader))

        obstacles = [str_list_to_int_tuple(row) for row in reader]

    return grid_size, start_pos, goal_pos, obstacles


def make_occupancy_grid_from_map(map_data, cell_size=5):
    """
    This function takes a map and a cell size (the physical size of one "cell" in the grid) and returns a 2D numpy
    array, with each cell containing a '1' if it is occupied and '0' if it is empty Inputs: map (tuple) - see
    read_map_from_file for description. Outputs: occupancy_grid - 2D numpy array
    """

    grid_map = MapContainer(map_data)

    length = int(grid_map.grid_size[0] / cell_size)
    height = int(grid_map.grid_size[1] / cell_size)

    # Initialise occupancy grid as a numpy array of zeroes
    ocpy_grid = np.zeros((length, height))

    for y in range(height):
        for x in range(length):

            for obstacle in grid_map.obstacles:

                # If obstacle intersects with cell x,y change value at x,y to 1
                if obstacle.intersects(x, y, cell_size):
                    ocpy_grid[x, y] = 1
                    break

    return ocpy_grid


def make_adjacency_matrix_from_occupancy_grid(ocpy_grid):
    """
    This function converts an occupancy grid into an adjacency matrix. We assume that cells are connected to their
    neighbours unless the neighbour is occupied. We also assume that the cost of moving from a cell to a neighbour is
    always '1' and allow only horizontal and vertical connections (i.e. no diagonals allowed). Inputs: occupancy_grid
    - a 2D (NxN) numpy array. An element with value '1' is occupied, while those with value '0' are empty. Outputs: A
    2D (MxM where M=NxN) array. Element (i,j) contains the cost of travelling from node i to node j in the occupancy
    grid.
    """

    # Initialise adjacency matrix as numpy array of ones
    adjacency_matrix = np.zeros((ocpy_grid.size, ocpy_grid.size))

    for y in range(ocpy_grid.size):
        for x in range(ocpy_grid.size):

            # Determine the coordinates in the occupancy grid from the coordinates in the adjacency matrix
            cell_i = divmod(x, ocpy_grid.shape[0])
            cell_j = divmod(y, ocpy_grid.shape[0])

            # If cells are adjacent and both are unoccupied record a travelling cost of 1
            if abs(cell_i[0] - cell_j[0]) + abs(cell_i[1] - cell_j[1]) == 1:
                if ocpy_grid[cell_i[0], cell_i[1]] != 1 and ocpy_grid[cell_j[0], cell_j[1]] != 1:
                    adjacency_matrix[x, y] = 1

    return adjacency_matrix


def get_path_from_predecessors(predecessors, map_data, cell_size=5):
    """
    This function takes a predecessors matrix, map_data and cell_size as input and returns the path from start to
    goal position. We take the mid-point of each cell as the (x, y) coordinate for the path. Inputs: predecessors - a
    2D numpy array (size = M = NxN, where N is the length of an occupancy grid) produced by scipy's implementation of
    Dijkstra's algorithm. Each element i tells us the index of the node we should travel to if we are in node j.
    map_data -  (tuple) see read_map_from_file for description. cell_size - (integer) the physical size corresponding
    to a single cell in the grid. Outputs: path - A list of tuples (x, y), where (x, y) are the coordinates of a
    position we can travel to in the map.
    """

    grid_map = MapContainer(map_data)
    half_cell = cell_size / 2

    # Move start and goal positions to middle of cells
    start = (grid_map.start_pos[0] - half_cell, grid_map.start_pos[1] - half_cell)
    goal = (grid_map.goal_pos[0] - half_cell, grid_map.goal_pos[1] - half_cell)

    # Convert grid coordinates to cell positions
    start_i = (int(start[0] // cell_size), int(start[1] // cell_size))
    goal_i = (int(goal[0] // cell_size), int(goal[1] // cell_size))

    # Determine size of cell grid
    grid_size = grid_map.grid_size[0] // cell_size

    # Determine cell number of start and goal positions
    start_no = start_i[0] + (start_i[1] * grid_size)
    current_no = goal_i[0] + (goal_i[1] * grid_size)

    path = []

    while current_no != start_no:
        path.append(divmod(current_no, grid_size))
        # Determine next position
        if current_no == -9999:
            return
        current_no = predecessors[start_no, current_no]

    # Convert cell positions to grid coordinates
    path = [((node[0] * cell_size) + half_cell, (node[1] * cell_size) + half_cell) for node in reversed(path)]

    # Add start and end nodes
    path.insert(0, grid_map.start_pos)
    path.append(grid_map.goal_pos)

    return path


def occupancy_grid(file, cell_size=5):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    # ax.set_axis_off()

    map_data = read_map_from_file(file)
    plot_map(ax, map_data)
    grid = make_occupancy_grid_from_map(map_data, cell_size)
    adjacency_matrix = make_adjacency_matrix_from_occupancy_grid(grid)
    # You'll need to edit the line below to use Scipy's shortest graph function to find the path for us
    predecessors = scipy.sparse.csgraph.shortest_path(adjacency_matrix, return_predecessors=True)[1]
    path = get_path_from_predecessors(predecessors, map_data, cell_size)

    if path:
        plot_path(ax, path)
    else:
        print('No path found')
    ax.set_aspect('equal')
    plt.show()


def plot_map(ax, map_data):
    """
    This function plots a map given a description of the map
    Inputs:
    ax (matplotlib axis) - the axis the map should be drawn on
    map_data - a tuple describing the map. See definition in read_map_from_file function for details.
    """
    if map_data:
        start_pos = map_data[1]
        goal_pos = map_data[2] 
        obstacles = map_data[3]

        ax.plot(goal_pos[0], goal_pos[1], 'r*')
        ax.plot(start_pos[0], start_pos[1], 'b*')

        for obstacle in obstacles:
            # Obstacle[0] is x position, [1] is y position and [2] is radius
            c_patch = plt.Circle((obstacle[0], obstacle[1]), obstacle[2], color='red')
            ax.add_patch(c_patch)
    else:
        print("No map data provided- have you implemented read_map_from_file?")


def plot_path(ax, path):
    """
    This function plots the path found by your occupancy grid solution.
    Inputs: ax (matplotlib axis) - the axis object where the path will be drawn
            path (list of tuples) - a list of points (x, y) representing the spatial co-ordinates of a path.
    """
    ax.plot(*zip(*path))


'''
==============================
The code below here is for testing my occupancy solution
==============================
'''


def test_make_occupancy_grid():
    map0 = ((10, 10), (1, 1), (9, 9), [])
    assert np.array_equal(make_occupancy_grid_from_map(map0, cell_size=1),
                          np.zeros((10, 10))), "1 - checking map 0 with cell size 10"

    map1 = ((10, 10), (1, 1), (9, 9), [(5, 5, 2)])
    assert np.array_equal(make_occupancy_grid_from_map(map1, cell_size=10),
                          np.array([[1]])), "1 - checking map 1 with cell size 10"
    assert np.array_equal(make_occupancy_grid_from_map(map1, cell_size=5),
                          np.array([[1, 1], [1, 1]])), "2 - checking map 1 with cell size 5"

    map1_cell_size_2_answer = np.array([[0, 0, 0, 0, 0],
                                        [0, 1, 1, 1, 0],
                                        [0, 1, 1, 1, 0],
                                        [0, 1, 1, 1, 0],
                                        [0, 0, 0, 0, 0]])
    assert np.array_equal(make_occupancy_grid_from_map(map1, cell_size=2),
                          map1_cell_size_2_answer), "Test 3 - checking map 1 with cell size 2"

    map2 = ((100, 100), (1, 1), (9, 9), [(10, 10, 5), (90, 90, 5)])
    map2_answer = np.array([[1, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 1]])
    assert np.array_equal(make_occupancy_grid_from_map(map2, cell_size=20),
                          map2_answer), "Test 4 - checking map 2 with cell size 20"


def test_make_adjacency_grid():
    occupancy_grid1 = np.array([
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]])

    adjacency_matrix1 = np.array([
        [0., 1., 0., 1., 0., 0., 0., 0., 0.],
        [1., 0., 1., 0., 1., 0., 0., 0., 0.],
        [0., 1., 0., 0., 0., 1., 0., 0., 0.],
        [1., 0., 0., 0., 1., 0., 1., 0., 0.],
        [0., 1., 0., 1., 0., 1., 0., 1., 0.],
        [0., 0., 1., 0., 1., 0., 0., 0., 1.],
        [0., 0., 0., 1., 0., 0., 0., 1., 0.],
        [0., 0., 0., 0., 1., 0., 1., 0., 1.],
        [0., 0., 0., 0., 0., 1., 0., 1., 0.]])

    assert np.array_equal(make_adjacency_matrix_from_occupancy_grid(occupancy_grid1),
                          adjacency_matrix1), '1 - checking occupancy grid 1 (empty grid)'

    occupancy_grid2 = np.array([[1, 1, 1],
                                [1, 1, 1],
                                [1, 1, 1]])

    adjacency_matrix2 = np.zeros((occupancy_grid2.size, occupancy_grid2.size))

    assert np.array_equal(make_adjacency_matrix_from_occupancy_grid(occupancy_grid2),
                          adjacency_matrix2), '2 - checking occupancy grid 2 (full grid)'

    occupancy_grid3 = np.array([[0, 1, 0],
                                [0, 1, 0],
                                [0, 1, 0]])

    adjacency_matrix3 = np.array([[0., 0., 0., 1., 0., 0., 0., 0., 0.],
                                  [0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                  [0., 0., 0., 0., 0., 1., 0., 0., 0.],
                                  [1., 0., 0., 0., 0., 0., 1., 0., 0.],
                                  [0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                  [0., 0., 1., 0., 0., 0., 0., 0., 1.],
                                  [0., 0., 0., 1., 0., 0., 0., 0., 0.],
                                  [0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                  [0., 0., 0., 0., 0., 1., 0., 0., 0.]])

    assert np.array_equal(make_adjacency_matrix_from_occupancy_grid(occupancy_grid3),
                          adjacency_matrix3), '3 - checking occupancy grid 3 (centre column occupied)'


def test_get_path():
    adjacency_matrix1 = np.array([
        [0., 1., 0., 1., 0., 0., 0., 0., 0.],
        [1., 0., 1., 0., 1., 0., 0., 0., 0.],
        [0., 1., 0., 0., 0., 1., 0., 0., 0.],
        [1., 0., 0., 0., 1., 0., 1., 0., 0.],
        [0., 1., 0., 1., 0., 1., 0., 1., 0.],
        [0., 0., 1., 0., 1., 0., 0., 0., 1.],
        [0., 0., 0., 1., 0., 0., 0., 1., 0.],
        [0., 0., 0., 0., 1., 0., 1., 0., 1.],
        [0., 0., 0., 0., 0., 1., 0., 1., 0.]])
    predecessors1 = scipy.sparse.csgraph.shortest_path(adjacency_matrix1, return_predecessors=True)[1]

    assert len(get_path_from_predecessors(predecessors1, ((90, 90), (30, 30), (90, 90), []),
                                          cell_size=30)) == 6, '1 - length of path = horizontal + vertical displacement'

    adjacency_matrix2 = np.zeros((9, 9))
    predecessors2 = scipy.sparse.csgraph.shortest_path(adjacency_matrix2, return_predecessors=True)[1]

    assert get_path_from_predecessors(predecessors2, ((90, 90), (30, 30), (90, 90), []),
                                      cell_size=30) is None, '2 - Testing full grid for no path returned'


def test_occupancy_grid():
    tests = [test_make_occupancy_grid, test_make_adjacency_grid, test_get_path]

    for i in range(len(tests)):
        print(f'Test {i + 1}:  ', end='')
        try:
            tests[i]()
            print('Pass')
        except Exception as e:
            print(f'FAIL Test {i + 1}.{e}')


'''
==============================pt

█▄▄▄▄ █▄▄▄▄    ▄▄▄▄▀        ▄▄▄▄▄   ████▄ █       ▄     ▄▄▄▄▀ ▄█ ████▄    ▄   
█  ▄▀ █  ▄▀ ▀▀▀ █          █     ▀▄ █   █ █        █ ▀▀▀ █    ██ █   █     █  
█▀▀▌  █▀▀▌      █        ▄  ▀▀▀▀▄   █   █ █     █   █    █    ██ █   █ ██   █ 
█  █  █  █     █          ▀▄▄▄▄▀    ▀████ ███▄  █   █   █     ▐█ ▀████ █ █  █ 
  █     █     ▀                               ▀ █▄ ▄█  ▀       ▐       █  █ █ 
 ▀     ▀                                         ▀▀▀                   █   ██ 

==============================
'''


def generate_random_point(_map: MapContainer) -> tuple[int, int]:
    x = random.randint(0, _map.grid_size[0])
    y = random.randint(0, _map.grid_size[0])

    return x, y


def find_nearest_node(random_pos: tuple[int, int], nodes: list[Node]) -> Node:
    shortest_distance_sq = math.inf
    nearest_node = nodes[0]

    for node in nodes:

        distance_sq = ((random_pos[0] - node.x()) ** 2) + ((random_pos[1] - node.y()) ** 2)
        if distance_sq < shortest_distance_sq and distance_sq != 0:
            shortest_distance_sq = distance_sq
            nearest_node = node

    return nearest_node


def find_new_node_coord(random_pos: tuple[int, int], nearest_coord: tuple[int, int], step_size: int) -> tuple[float, float]:
    """
    Using similar triangles find the point in the direction of the point step_size away
    """

    dx = random_pos[0] - nearest_coord[0]
    dy = random_pos[1] - nearest_coord[1]
    dd = math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))

    new_x = ((dx / dd) * step_size) + nearest_coord[0]
    new_y = ((dy / dd) * step_size) + nearest_coord[1]

    return new_x, new_y


def line_intersect_obstacle(point_a: tuple[float, float], point_b: tuple[float, float], obstacle: Obstacle) -> bool:
    # If line is vertical then skip
    if point_b[0] - point_a[0] == 0:
        return False

    # Find coefficients of the equation of the line
    gradient = (point_b[1] - point_a[1]) / (point_b[0] - point_a[0])
    y_intercept = point_b[1] - gradient * point_b[0]

    # Find the coefficients of the rearranged equation for the intercepts
    a = 1 + math.pow(gradient, 2)
    b = (2 * gradient * (y_intercept - obstacle.y)) - (2 * obstacle.x)
    c = math.pow(obstacle.x, 2) + math.pow((y_intercept - obstacle.y), 2) - math.pow(obstacle.radius, 2)

    # Check discriminant and use the quadratic formula to determine roots (intercepts)
    discriminant = math.pow(b, 2) - (4 * a * c)
    if discriminant < 0:  # No real roots
        return False
    elif discriminant == 0:  # Repeated root
        x_possibilities = [-b / (2 * a)]
    else:  # 2 distinct roots
        x_possibilities = [(-b + math.sqrt(discriminant)) / (2 * a), (-b - math.sqrt(discriminant)) / (2 * a)]

    for x in x_possibilities:

        # Check if intersection is on the line segment
        if x < point_a[0] and x > point_b[0]:
            return True
        if x < point_b[0] and x > point_a[0]:
            return True

    return False


def rrt(map_file, step_size=10, num_points=100):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    # ax.set_axis_off()

    map_data = read_map_from_file(map_file)
    plot_map(ax, map_data)

    map = MapContainer(map_data)

    starting_node = Node(
        None,
        map.start_pos
    )
    nodes = [starting_node]

    for i in range(num_points):
        # Generate a random point
        random_pos = generate_random_point(map)

        # Find the nearest point in the tree
        nearest = find_nearest_node(random_pos, nodes)

        # Determine where new node would be
        proposed_coord = find_new_node_coord(random_pos, nearest.coord, step_size)

        # If the proposed line segment does not interest with any of the obstacles then create it
        if not any([line_intersect_obstacle(nearest.coord, proposed_coord, obstacle) for obstacle in map.obstacles]):
            # Create this new node and add it to the tree
            new_node = Node(
                nearest,
                proposed_coord
            )
            nodes.append(new_node)

    nearest_to_goal = find_nearest_node(map.goal_pos, nodes)

    path = None

    # Check if nearest to goal can reach the goal without crossing an obstacle
    if not any([line_intersect_obstacle(nearest_to_goal.coord, map.goal_pos, obstacle) for obstacle in map.obstacles]):
        goal_node = Node(
            nearest_to_goal,
            map.goal_pos
        )

        path = goal_node.find_path([], map.start_pos)

    # Add all line segments to a list
    segments = []
    for node in nodes:
        if node.parent:
            segments.append([node.coord, node.parent.coord])

    if segments:
        plot_segments(ax, segments)
    if path:
        plot_path(ax, path)
    else:
        print('No path found')
    ax.set_aspect('equal')
    plt.show()


def plot_segments(ax, segments):
    """
    Plot segments as dashed lines
    """
    for seg in segments:
        ax.plot(*zip(*seg), linestyle='dashed')


'''
==============================
The code below here is for testing my RRT solution
==============================
'''


def test_nearest_node():
    na = Node(None, (1, 1))
    nb = Node(None, (3, 3))
    nc = Node(None, (10, 4))
    nodes = [na, nb, nc]

    test_coord1 = (11, 3)
    assert find_nearest_node(test_coord1, nodes) == nc, '1 - test coord 1 is closest to node c'

    test_coord2 = (0, 2)
    assert find_nearest_node(test_coord2, nodes) == na, '2 - test coord 2 is closet to node a'

    test_coord2 = (2, 2)
    assert find_nearest_node(test_coord2,
                             nodes) == na, '3 - test coord 3 is equidistant from a and b but first (a) is selected'


def test_find_new_node_coord():
    random_pos1 = (6, 8)
    nearest_node1 = (0, 0)

    assert find_new_node_coord(random_pos1, nearest_node1, step_size=5) == (3, 4), '1 - 3,4,5 triangle test'

    random_pos2 = (40, 17)
    nearest_node2 = (4, 2)

    assert find_new_node_coord(random_pos2, nearest_node2, step_size=13) == (16, 7), '2 - 5,12,13 triangle test'


def test_line_intersect_obstacle():
    point_a1 = (0, 0)
    point_b1 = (5, 5)

    obstacle1 = Obstacle((6, 6, 3))
    assert line_intersect_obstacle(point_a1, point_b1, obstacle1), '1 - intersects with B'

    obstacle2 = Obstacle((-1, -6, 5))
    assert not line_intersect_obstacle(point_a1, point_b1, obstacle2), '2 - Test 2: does not intersect but close to A'

    obstacle3 = Obstacle((3, 4, 1))
    assert line_intersect_obstacle(point_a1, point_b1, obstacle3), '3 - closest to a point on the line'

    assert not line_intersect_obstacle((3, 3), (3, 6), Obstacle((3, 8, 4))), '4 - vertical line then skip'


def test_rrt():
    tests = [test_find_new_node_coord, test_line_intersect_obstacle, test_nearest_node]

    for i in range(len(tests)):
        print(f'Test {i + 1}:  ', end='')
        try:
            tests[i]()
            print('Passed')
        except Exception as e:
            print(f'FAILED Test {i + 1}.{e}')


'''
==============================
The code below here is used to read arguments from the terminal, allowing us to run different parts of your code.
You should not need to modify this
==============================
'''


def main():
    parser = argparse.ArgumentParser(description=" Path planning Assignment for CPA 2024/25")
    parser.add_argument('--rrt', action='store_true')
    parser.add_argument('-test_rrt', action='store_true')
    parser.add_argument('--occupancy', action='store_true')
    parser.add_argument('-test_occupancy', action='store_true')
    parser.add_argument('-file')
    parser.add_argument('-cell_size', type=int)

    args = parser.parse_args()

    if args.occupancy:
        if args.file is None:
            print("Error - Occupancy grid requires a map file to be provided as input with -file <filename>")
            exit()
        else:
            if args.cell_size:
                occupancy_grid(args.file, args.cell_size)
            else:
                occupancy_grid(args.file)

    if args.test_occupancy:
        print("Testing occupancy_grid")
        test_occupancy_grid()

    if args.test_rrt:
        print("Testing RRT")
        test_rrt()

    if args.rrt:
        if args.file is None:
            print("Error - RRT requires a map file to be provided as input with -file <filename>")
            exit()
        else:
            rrt(args.file)


if __name__ == "__main__":
    main()
