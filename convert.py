import os
from PIL import Image

def to_bg(name):
    orig = Image.open(name)

    resized = orig.resize((256 * 15, 256 * 7))

    for i in range(15):
        for j in range(7):
            cropped = resized.crop((256 * i, 256 * j, 256 * i + 256, 256 * j + 256))
            cropped.save(f"21_9_{j+1}_{chr(97+i)}_loading.tga")

def to_skybox(name, outname):
    orig = Image.open(name)

    resized = orig.resize((256, 256))

    resized.save(f"{outname}.tga")
    resized.save(f"{outname}.bmp")

l = os.listdir("/home/gamer/.steam/debian-installation/steamapps/common/Half-Life/valve/gfx/env")

to_bg("input.png")

#l = list(filter(lambda x: x.endswith(".tga"), l))
#l = [i.split(".")[0] for i in l]

#for i in l:
#    to_skybox("input.png", f"/home/gamer/.steam/debian-installation/steamapps/common/Half-Life/valve/gfx/env/{i}")
