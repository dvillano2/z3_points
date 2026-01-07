import glob
from PIL import Image

if __name__ == "__main__":
    frames = [Image.open(f) for f in sorted(glob.glob("images/*.png"))]
    frames_resized = [
        f.resize((f.width // 2, f.height // 2), Image.Resampling.LANCZOS)
        for f in frames
    ]

    frames_resized[0].save(
        "animation/animation.gif",
        save_all=True,
        append_images=frames[1:],
        duration=1000,
        loop=0,
    )
