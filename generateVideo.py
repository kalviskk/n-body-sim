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
            "simulation3/step%05d.png",
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


# ir iespēja atsevišķi ģenerēt video, palaižot šo failu
generateMP4()
