#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
import random

# -----------------------------------------------------------

## Objects for colliding elastically in our system.
class Box:
  def __init__(self, length, mass, xPos, velocity):
    # Parameters of the box.
    self.length = length
    self.mass = mass
    # Initial position.
    self.x = xPos
    self.vel = velocity
    # Selecting a random colour for the box.
    self.colour = random.choice([[1,0,0],[0,1,0],[0,0,1],[1,1,0],[1,0,1],[0,1,1]])
    
  ## Right side position of the box.
  def right(self):
    return self.x + 0.5*self.length
  
  ## Left side position of the box.
  def left(self):
    return self.x - 0.5*self.length
  
  ## Right side position in the next timestep.
  def nextRight(self, dt):
    return (self.x + 0.5*self.length) + self.vel*dt
  
  ## Left side position in the next timestep.
  def nextLeft(self, dt):
    return (self.x - 0.5*self.length) + self.vel*dt
  
  ## Step the box forward by 'dt'.
  def set_nextPos(self, dt):
    self.x = self.x + self.vel*dt

# -----------------------------------------------------------

## Our system!
class Grid:
  def __init__(self, fps, wallCenter, wallWidth, box1, box2):
    # Collision counter.
    self.colCount = 0
    # Array with the two boxes.
    self.boxes = [box1, box2]
    # Size of the wall.
    self.wallCenter = wallCenter
    self.wallWidth = wallWidth
    self.wallHeight = 1.5*box1.length
    # Discretize time per frame.
    self.fps = fps
    self.dt = 1/fps
    self.time = 0.0
    self.nextTime = 0.0
    # Store positions for animation
    self.x1_history = []
    self.x2_history = []
    self.time_history = []
    self.colCount_history = []
    
  ## Left side of the wall.
  def wallLeft(self):
    return self.wallCenter - 0.5*self.wallWidth
  
  ## Detect collisions in the next timestep.
  def block_detect(self, dt):
    return self.boxes[0].nextRight(dt) > self.boxes[1].nextLeft(dt)
  def wall_detect(self, dt):
    return self.boxes[1].nextRight(dt) > self.wallLeft()
  
  ## Collision between blocks.
  def blockCollision(self):
    # Parameters of the boxes.
    m1 = self.boxes[0].mass
    m2 = self.boxes[1].mass
    v1 = self.boxes[0].vel
    v2 = self.boxes[1].vel
    # Step forward the exact time until collision.
    step = ( self.boxes[0].right() - self.boxes[1].left() ) / (self.boxes[1].vel - self.boxes[0].vel)
    self.boxes[0].set_nextPos(step)
    self.boxes[1].set_nextPos(step)
    # Final velocities for an elastic collision in one dimension.
    self.boxes[0].vel = ((m1-m2)*v1 + 2*m2*v2) / (m1 + m2)
    self.boxes[1].vel = ((m2-m1)*v2 + 2*m1*v1) / (m1 + m2)
    # Add 'step' to grid time.
    self.time += step
    # Count the collision.
    self.colCount += 1
    # Print the event.
    #print(f"Collision between blocks, t = {self.time}")
    
  ## Collision between small block and wall.
  def wallCollision(self):
    # Step forward the exact time until collision.
    step = ( self.wallLeft() - self.boxes[1].right() ) / self.boxes[1].vel
    self.boxes[0].set_nextPos(step)
    self.boxes[1].set_nextPos(step)
    # Invert velocity direction of the small box.
    self.boxes[1].vel *= -1
    # Add 'step' to grid time.
    self.time += step
    # Count the collision.
    self.colCount += 1
    # Print the event.
    # print(f"Collision with wall, t = {self.time}")
    
  ## Detect which collision will occur first.
  def selectCollision(self):
    blockStep = ( self.boxes[0].right() - self.boxes[1].left() ) / (self.boxes[1].vel - self.boxes[0].vel)
    wallStep = ( self.wallLeft() - self.boxes[1].right() ) / self.boxes[1].vel
    if blockStep < wallStep:
      self.blockCollision()
    else:
      self.wallCollision()
  ## Search for collisions over the next timestep.
  def stepSearch(self, dt):
    if self.block_detect(dt) and self.wall_detect(dt):
      self.selectCollision()
    elif self.block_detect(dt):
      self.blockCollision()
    elif self.wall_detect(dt):
      self.wallCollision()
    else:
      self.time += self.dt
      self.boxes[0].set_nextPos(self.dt)
      self.boxes[1].set_nextPos(self.dt)
  ## Generate the next frame of the animation.
  def frameGenerator(self):
    # Store the limit of the timestep.
    self.nextTime = self.time + self.dt
    # Search for collisions.
    self.stepSearch(self.dt)
    # In case of detecting a collision before the next frame, starts a loop, trying to search again until reaching 'nextTime'.
    while self.nextTime > self.time:
      auxTime = self.nextTime - self.time
      self.stepSearch(auxTime)
    # Store current state for animation
    self.x1_history.append(self.boxes[0].x)
    self.x2_history.append(self.boxes[1].x)
    self.time_history.append(self.time)
    self.colCount_history.append(self.colCount)

# -----------------------------------------------------------



## Animation parameters.
time = 5.0 # s
fps = 60.0
n_frames = int(time * fps)
## Big box parameters. # m
x1 = -2 # m
v1 = 2.0 # m/s
## Small box parameters. *Make sure x1+0.5*l1 < x2+0.5*l2.
L2 = 1 # m
x2 = 1 # m
## Wall parameters. *Make sure x2+0.5*l2 < x3-0.5*wallWidth
L3 = 0.5 # m
x3 = 3 # m
# "n" value for mass, will approximate "n+1" digits of Pi.
N = 3


L1 = L2 * (1 + N/10)
# Generate boxes.
bigBox = Box(L1, 100**N, x1, v1)
smallBox = Box(L2, 1, x2, 0.0)
grid = Grid(fps, x3, L3, bigBox, smallBox)



# -----------------------------------------------------------

# Pre-generate all frames
for _ in range(n_frames):
    grid.frameGenerator()
    
# Create the figure and axes for the animation
fig, ax = plt.subplots()

## Function to update the animation
def update(i):
    ax.clear()
    # Set the limits of the plot.
    margin = 1.0
    min_x = min(grid.x1_history[i] - 0.5 * L1, grid.x2_history[i] - 0.5 * L2) - margin
    max_x = grid.wallCenter + grid.wallWidth + margin
    ax.set_xlim(min_x, max_x)
    ax.set_ylim(0, max(L1, L2) + margin)
    ax.set_aspect('equal')
    # Wall drawing.
    wall_left = grid.wallLeft()
    ax.add_patch(patches.Rectangle(
        (wall_left, 0),
        grid.wallWidth,
        grid.wallHeight,
        facecolor='black'
    ))
    # Block drawing.
    ax.add_patch(patches.Rectangle(
        (grid.x1_history[i] - 0.5 * L1, 0),
        L1, L1,
        color=grid.boxes[0].colour
    ))
    ax.add_patch(patches.Rectangle(
        (grid.x2_history[i] - 0.5 * L2, 0),
        L2, L2,
        color=grid.boxes[1].colour
    ))
    # Title.
    ax.set_title(f"N = {N}, t = {grid.time_history[i]:.2f} s, collisions = {grid.colCount_history[i]}")
    
# Create the animation.
ani = animation.FuncAnimation(
    fig,
    update,
    frames=n_frames,
    interval=1000/fps,
    repeat=False
)

# Save the animation
PiCol_video = f'collision_simulation_N_{N}.mp4'
print(f"Saving animation to {PiCol_video}...")
ani.save(PiCol_video, writer='ffmpeg', fps=fps)
print("Animation saved successfully!")

## Show the animation (optional)
# Uncomment the next line to show the animation
# plt.show()
