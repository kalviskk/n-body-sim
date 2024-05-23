import os


# Izveidojam mapi, ja tāadas nav un sākumā izdzēšam visus attēlus, lai netraucē vecie, ja izvēlamies mazāku simulācijas ilgumu
def empty_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    else:
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)


empty_directory("simulation")
