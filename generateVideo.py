import subprocess


def generateMP4():
    # Generate a video from simulation images using ffmpeg
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-framerate",
            "30",
            "-i",
            "simulation/step%05d.png",
            "-c:v",
            "libx264",
            "-r",
            "30",
            "-pix_fmt",
            "yuv420p",
            "video/sim.mp4",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


# Generate the video when the script is run
generateMP4()
