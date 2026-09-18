import os
from PIL import Image
from pathlib import Path

def image_to_bg(name):
    orig = Image.open(name)

    resized = orig.resize((256 * 15, 256 * 7))

    output = []

    for i in range(15):
        for j in range(7):
            cropped = resized.crop((256 * i, 256 * j, 256 * i + 256, 256 * j + 256))

            print(f"Processing {i + 1}x{j + 1} ({(i*7+j) + 1} / {15 * 7})...")

            output.append({"name": f"resource/background/21_9_{j+1}_{chr(97+i)}_loading.tga", "img": cropped})

    return output

def image_to_skybox(name, outname=None):
    orig = Image.open(name)

    resized = orig.resize((256, 256))

    if outname:
        return [{"name": f"gfx/env/{outname}.tga", "img": resized}, {"name": f"gfx/env/{outname}.bmp", "img": resized}]
    else:
        return resized

def locate_game():
    home = Path.home()
    hl = home / ".steam" / "steam" / "steamapps" / "common" / "Half-Life"

    if os.path.exists(hl) and os.path.isdir(hl):
        return hl
    return None
