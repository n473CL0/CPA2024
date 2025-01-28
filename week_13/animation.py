import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Example list of 2D numpy arrays
array_list = [
    np.random.choice([0, 1], size=(10, 10), p=[0.8, 0.2]) for _ in range(20)
]

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
