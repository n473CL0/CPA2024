# experimented with this but didn't get it working

def make_adjacency_matrix_from_occupancy_grid(occupancy_grid):
    '''
    This function converts an occupancy grid into an adjacency matrix. We assume that cells are connected to their neighbours unless the neighbour is occupied. 
    We also assume that the cost of moving from a cell to a neighbour is always '1' and allow only horizontal and vertical connections (i.e. no diagonals allowed).
    Inputs: occupancy_grid - a 2D (NxN) numpy array. An element with value '1' is occupied, while those with value '0' are empty.
    Outputs: A 2D (MxM where M=NxN) array. Element (i,j) contains the cost of travelling from node i to node j in the occupancy grid. 
    '''

    # Initialise adjacency matrix as numpy array of ones
    adjacency_matrix = np.zeros((occupancy_grid.size, occupancy_grid.size))

    for y in range(occupancy_grid.shape[0]):
        for x in range(occupancy_grid.shape[0]):

            cell_no = y*occupancy_grid.shape[0]+x

            if occupancy_grid[x, y] != 1:
                if x > 0:
                    if occupancy_grid[x-1, y] != 1:
                        adjacency_matrix[cell_no, cell_no-1] = 1
                if x < occupancy_grid.shape[0] - 1:
                    if occupancy_grid[x+1, y] != 1:
                        adjacency_matrix[cell_no, cell_no+1] = 1
                if y > 0:
                    if occupancy_grid[x, y-1] != 1:
                        adjacency_matrix[cell_no, cell_no-occupancy_grid.shape[0]] = 1
                if y < occupancy_grid.shape[0] - 1:
                    if occupancy_grid[x, y+1] != 1:
                        adjacency_matrix[cell_no, cell_no+occupancy_grid.shape[0]] = 1

    print(occupancy_grid)

    print(adjacency_matrix)

    return adjacency_matrix


def mod(vector):
    
    return np.linalg.norm(vector)


def line_intersect_obstacle_old(nearest: tuple[int], proposed: tuple[int], obstacle: Obstacle) -> bool:
    
    print(obstacle.radius)

    # Find vectors between points A = nearest, B = proposed, C = obstacle centre

    AB = np.array([proposed[0] - nearest[0], proposed[1] - nearest[1]])
    AC = np.array([obstacle.x - nearest[0], obstacle.y - nearest[1]])
    BC = np.array([obstacle.x - proposed[0], obstacle.y - proposed[1]])

    # Case: A is closer than any other point on the line
    if mod(AC) < mod(BC):
        cos_theta = AC.dot(AB) / (mod(AB) * mod(AC))
        if cos_theta <= 0:
            print('case A')
            return mod(AC) <= obstacle.radius
    
    # Case B is closer than any other point on the line
    cos_theta = BC.dot(AB) / (mod(AB) * mod(BC))
    if cos_theta <= 0:
        print('case B')
        return mod(BC) <= obstacle.radius
    
    # Case some point along the line is the closest point (use herons formula and area formula to find perp distance)
    S = (mod(AB) + mod(AC) + mod(BC)) / 2
    A = math.sqrt(S * (S-mod(AB)) * (S-mod(AC)) * (S-mod(BC)))
    perp_dic = A / mod(AB)

    print(obstacle.radius)

    return perp_dic <= obstacle.radius