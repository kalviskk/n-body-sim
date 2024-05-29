
# Particle Simulation

## Overview
This project is a simulation of particle interactions using the Barnes-Hut algorithm for efficient computation of gravitational forces. The simulation generates particles, calculates their interactions, and produces visual output in the form of a video.

## Files Description

### 1. `main.py`
This is the main script to run the simulation. It initializes the parameters, creates particles, runs the simulation, and generates a video from the simulation steps.

### 2. `createParticles.py`
This script contains the `createParticles` function, which generates particles with initial positions and velocities based on specified distributions (e.g., ring, uniform, two bodies).

### 3. `calc_accelerations.py`
Contains the `calculate_accelerations` function, which calculates the accelerations of particles using the Barnes-Hut tree-based algorithm.

### 4. `emptyDir.py`
Contains the `empty_directory` function to clean up and prepare the simulation directory by deleting old files.

### 5. `generateVideo.py`
This script contains the `generateMP4` function, which generates a video from the simulation step images using `ffmpeg`.

### 6. `Particle.py`
Defines the `Particle` class, representing individual particles with attributes such as position, velocity, mass, radius, and color. It also includes methods to update velocity and position.

### 7. `plotting.py`
Contains the `drawStep` function, which plots the particles at each step of the simulation and saves the plot as an image.

### 8. `saving.py`
Provides the `save_particles` function to save the state of particles to a file using `pickle`.

### 9. `simulate.py`
Contains the `simulate` function, which runs the entire simulation process: updating particle velocities and positions, drawing steps, and saving the final state of particles.

### 10. `BHTree.py`
Implements the Barnes-Hut tree-based algorithm for efficient computation of gravitational forces. This file includes classes and functions for building the tree, inserting particles, and calculating forces.

## How to Run

1. **Setup**: Ensure you have Python installed along with the necessary libraries (`numpy`, `matplotlib`, `cmocean`, `ffmpeg`, `pickle`).

2. **Run Simulation**: Execute the `main.py` script.
   ```sh
   python main.py
   ```

3. **Output**: The simulation will generate images for each step in the `simulation` directory and a video in the `video` directory.

## Example
To run the simulation for different numbers of particles, you can modify the `N` value in the `main.py` script and adjust other parameters as needed.

```python
# initialize
N = 2000  # number of particles
total_steps = 100
G = 1  # gravitational constant
dt = 1  # time step
height = 500
width = 500
distribution = "ring"
ring_radius = 600  # Radius of the ring
```

## Credits
The Barnes-Hut algorithm implementation is adapted from [Gongure's GitHub repository](https://github.com/Gongure/n-body-simulation-methods).

## License
This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).

Feel free to modify the parameters and distributions to explore different simulation scenarios and improve the model.
