import pickle


def save_particles(particles, filename="particles.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(particles, f)
    print("Particles array saved.")
