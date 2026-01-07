import glob
from PIL import Image

if __name__ == "__main__":
    frames = [Image.open(f) for f in sorted(glob.glob("images/*.png"))]

    frames[0].save(
        "animation/animation.gif",
        save_all=True,
        append_images=frames[1:],
        duration=1000,
        loop=0,
    )
