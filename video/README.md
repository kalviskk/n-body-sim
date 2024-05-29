# Description of Videos

This collection of videos demonstrates various particle simulations with gravitational interactions. Here are the key parameters and conditions for each simulation:

- **Particle Masses**: All particles have a mass $m = 1$, with two exceptions:
  - In simulations where particles orbit a single central body, the central mass $M = 1000$.
  - In the video `2_particle_orbit.mp4`, the heavy mass is $M = 10000$.

- **Gravitational Constant (G)**: Set to 1 for all simulations.
  
- **Time Step**: Set to 1 for all simulations.

- **Playback Speed**: The videos were interpolated to increase playback speed. To determine the interpolation amount, check the "Step" values in two consecutive frames and calculate the difference.

## Video List

1. **10k_particle_ring.mp4**: 10,000 particles initialized with $v = 0$ in a ring shape.
2. **2_particle_orbit.mp4**: Two particles with one having a significantly larger mass of $M = 10000$.
3. **2k_particles_rect.mp4**: 2,000 particles initialized with $v = 0$ in a rectangle.
4. **2k_particles_rect_collisions.mp4**: 2,000 particles initialized with $v = 0$ in a rectangle with collisions. Note that this simulation is incorrect.
5. **2k_particles_ring.mp4**: 2,000 particles initialized with $v = 0$ in a ring shape.
6. **2k_particles_ring_collisions.mp4**: 2,000 particles initialized with $v = 0$ in a ring shape with collisions. Note that this simulation is incorrect.
7. **2k_particles_rotate=v.mp4**: 2,000 particles initialized with $v = \sqrt{\frac{MG}{d}}$ in a ring shape.
8. **2k_particles_rotate-v.mp4**: 2,000 particles initialized with $v < \sqrt{\frac{MG}{d}}$ in a ring shape. The velocity was randomly chosen as 0.8 to 1.0 of $\sqrt{\frac{MG}{d}}$.
