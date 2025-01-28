import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation
import copy

ALIVE = 1 
DEAD = 0 
GRID_WIDTH = 20
GRID_HEIGHT = 20
#ALIVE INDEX is the index of the single cell which is set to 1.
ALIVE_INDEX = 10
#ALIVE probability is the fraction of a random grid which is set to 1.
ALIVE_PROBABILITY = 0.3
NUM_STEPS = 100

def create_random_grid(height, width, alive_probability):
  '''
  Makes a 2 dimensional grid of dimensions HEIGHT x WIDTH
  with an 'alive_probability' chance of a cell being 1
  '''

  random_grid = np.random.rand(height, width)

  standard_grid = np.where(random_grid < alive_probability, ALIVE, DEAD)

  return standard_grid

def update_cell(neighbourhood):
  '''
  Calculates the new value for a cell given the neighbourhood
  '''

  element = neighbourhood[1,1]
  neighbours = np.sum(neighbourhood) - element

  if element:
    # Death rule 1 (loneliness) and death rule 2 (starvation)
    if neighbours < 2 or neighbours > 3:
      return 0
    # Survival rule
    return 1
  # Birth rule
  if neighbours == 3:
    return 1
  return 0


def update_grid(old_grid):
  '''
  Update the values within a grid according to local rules
    '''
  new_grid = np.zeros(shape=old_grid.shape)

  for i in range(1, old_grid.shape[0]-1):
    for j in range(1, old_grid.shape[1]-1):
      new_grid[i, j] = update_cell(old_grid[i-1:i+2,j-1:j+2])

  return new_grid

def animate_grids(array_list):
  
  # Set up the figure and axes
  fig, ax = plt.subplots()
  im = ax.imshow(array_list[0], cmap='gray', interpolation='none', vmin=0, vmax=1)
  ax.set_title("2D Array Animation")
  ax.axis('off')  # Turn off axis labels

  # Function to update the animation
  def update(frame):
      im.set_array(array_list[frame])
      return [im]

  # Create the animation
  ani = FuncAnimation(
      fig, update, frames=len(array_list), interval=200, blit=True
  )

  plt.show()


def test_update_cell():
    # Birth rule: A dead cell with exactly 3 live neighbors becomes alive.
    assert update_cell(np.array([[0, 1, 0], [1, 0, 1], [0, 0, 0]])) == 1

    # Loneliness rule: A live cell with fewer than 2 live neighbors dies.
    assert update_cell(np.array([[0, 0, 0], [0, 1, 0], [0, 1, 0]])) == 0

    # Overcrowding rule: A live cell with more than 3 live neighbors dies.
    assert update_cell(np.array([[1, 1, 1], [1, 1, 0], [0, 0, 0]])) == 0

    # Survival rule: A live cell with 2 or 3 live neighbors survives.
    assert update_cell(np.array([[1, 0, 0], [1, 1, 0], [0, 0, 0]])) == 1
    assert update_cell(np.array([[1, 1, 0], [1, 1, 0], [0, 0, 0]])) == 1

    # Stable state: A dead cell with fewer or more than 3 live neighbors stays dead.
    assert update_cell(np.array([[0, 0, 0], [0, 0, 0], [0, 1, 0]])) == 0
    assert update_cell(np.array([[1, 1, 1], [0, 0, 1], [0, 0, 0]])) == 0


def test_update_grid():
    # Test 1: Stable configuration (block)
    old_grid = np.array([
        [0, 0, 0, 0],
        [0, 1, 1, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0]
    ])
    new_grid = update_grid(old_grid)
    assert (new_grid == old_grid).all()

    # Test 2: Oscillator (blinker)
    old_grid = np.array([
        [0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0]
    ])
    expected_new_grid = np.array([
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ])
    new_grid = update_grid(old_grid)
    assert (new_grid == expected_new_grid).all()

    # Test 3: Empty grid remains empty
    old_grid = np.zeros((5, 5))
    new_grid = update_grid(old_grid)
    assert (new_grid == old_grid).all()

    # Test 4: Single live cell dies (loneliness)
    old_grid = np.array([
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, 0]
    ])
    expected_new_grid = np.zeros((3, 3))
    new_grid = update_grid(old_grid)
    assert (new_grid == expected_new_grid).all()

    # Test 5: Birth rule (dead cell with 3 neighbors becomes alive)
    old_grid = np.array([
        [0, 1, 0],
        [1, 0, 1],
        [0, 0, 0]
    ])
    expected_new_grid = np.array([
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, 0]
    ])
    new_grid = update_grid(old_grid)
    assert (new_grid == expected_new_grid).all()  


def run_tests():
    test_update_cell()
    test_update_grid()
    print("All tests passed!")


def main():
    
    run_tests()

    #Functions for making a grid - use commenting to choose which runs.
    grid = create_random_grid(GRID_HEIGHT, GRID_WIDTH, ALIVE_PROBABILITY)
    #grid = create_random_grid(GRID_LENGTH, ALIVE_PROBABILITY)

    grids = []

    #Use a list to store all the grids we generate
    grids = []
    #Repeatedly apply the update rule for a certain number of steps
    for t in range(NUM_STEPS):
        #Calculate the values in each position for the new grid
        new_grid = update_grid(grid)
        #Overwrite the old grid with the new grid
        grid=copy.deepcopy(new_grid)
        #Add the updated grid to our store
        grids.append(new_grid)

    #Plot all grids we've generated to observe how the CA evolves.
    animate_grids(grids)

main()