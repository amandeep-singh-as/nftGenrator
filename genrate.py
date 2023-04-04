import json
from PIL import Image
from utils import bColors
import imageio

config = json.load(open("config.json"))

MAX_WORKER = config['maxWorker']
DURATION_PER_IMG = config['durationPerImage']

HEIGHT, WIDTH = config['size']['height'], config['size']['width']


def genrateTokens(layerSet: list[str], token_version: int) -> None:

    print(f"{bColors.bcolors.WARNING}Now Minting token #{token_version} {bColors.bcolors.ENDC}")

    token = Image.new("RGBA", (HEIGHT, WIDTH), color=(0, 0, 0, 0))

    for layer in layerSet:
        img = Image.open(layer).convert("RGBA").resize((HEIGHT, WIDTH))
        token.paste(img, (0, 0), img)
    
    token.save("./build/tokens/NFT #" + str(token_version) + ".png")

def genrateGIFTokens(layerSet: list[str], token_version: int) -> None:

    print(f"{bColors.bcolors.WARNING}Now Minting token #{token_version} {bColors.bcolors.ENDC}")

    images = []

    for layer in layerSet:
        img = Image.open(layer).convert("RGBA").resize((HEIGHT, WIDTH))
        images.append(img)

    imageio.mimsave("./build/tokens/NFT #" + str(token_version) + ".gif", images, DURATION_PER_IMG)

