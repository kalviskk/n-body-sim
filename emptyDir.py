import os


# Empty the specified directory by deleting all files within it
def empty_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    else:
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)


# Clear the simulation directory
empty_directory("simulation")
