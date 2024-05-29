import matplotlib.pyplot as plt


def drawStep(particles, step, fig, ax, height, width):
    fig.clf()  # Clear the figure
    ax = fig.add_subplot(111)
    ax.set_xlim(-width * 5, width * 6)
    ax.set_ylim(-height * 5, height * 6)

    # Plot particles
    for particle in particles:
        ax.scatter(
            particle.position[0],
            particle.position[1],
            color=particle.color,
            ec="none",
            s=0.5,
        )

    # Turn off the axis
    ax.axis("off")

    # Remove padding around the plot
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

    ax.set_facecolor("black")
    fig.patch.set_facecolor("black")
    ax.set_aspect("equal", "box")
    ax.set_title(
        f"Step {step}", pad=-10, color="white"
    )  # Optional: set title color to white and move closer to the plot

    # Save the figure
    fig.savefig(
        f"simulation/step{int(step/2):05d}.png",
        dpi=300,
        bbox_inches="tight",
        pad_inches=0,
    )
