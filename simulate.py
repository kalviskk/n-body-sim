import matplotlib.pyplot as plt
from calc_accelerations import calculate_accelerations
from plotting import drawStep
from BHTree import BHTree


def simulate(particles, G, dt, steps, height, width):
    fig, ax = plt.subplots()
    for step in range(int(steps)):
        # saglabāsim tikai katru piekto, lai paātrinātu darbību, bet turētu dt mazu
        if not step % 10:
            drawStep(particles, step, fig, ax, height, width)
        accelerations = calculate_accelerations(particles, G)
        for i, particle in enumerate(particles):
            particle.update_velocity(accelerations[i], dt)

        # collisions?

        # detect_and_handle_collisions(particles, height, width)

        for particle in particles:
            particle.update_position(dt)
        if step != 0 and step % (steps // 10) == 0:
            print(f"{(step / steps) * 100:.1f}%")
