# %%
import subprocess


def generateMP4():
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
            "15",
            "-pix_fmt",
            "yuv420p",
            "video/sim6.mp4",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


# ir iespēja atsevišķi ģenerēt video, palaižot šo failu
generateMP4()
