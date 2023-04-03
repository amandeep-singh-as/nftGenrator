import json
from os import listdir
from os.path import isfile, join
import itertools
from PIL import Image
import asyncio
from concurrent.futures import ThreadPoolExecutor

config = open("config.json")

data = json.load(config)
height, width = data['size']['height'], data['size']['width']


def layerSetup(layerOrder: list[str]) -> list[list[str]]:
    layers = []
    for layer in layerOrder:
        path = "./layers/" + layer
        layers.append([join(path, f)
                      for f in listdir(path) if isfile(join(path, f))])

    return getUniqueCombinations(layers)


def getUniqueCombinations(layers: list[str]) -> list[list[str]]:
    return list(itertools.product(*layers))


def genrateToken(layerSet, i):
    print("Minting token ", i)
    token = Image.new("RGBA", (height, width), (0, 0, 0, 0))

    for layer in layerSet:
        img = Image.open(layer).convert("RGBA").resize((height, width))
        token.paste(img, (0, 0), img)
    token.save("./build/NFT" + str(i) + ".png")


async def createNFT(layerCombinations, tokenQty=None):
    with ThreadPoolExecutor(max_workers=10) as executor:
        loop = asyncio.get_event_loop()
        tasks = []
        i = 1
        for x in layerCombinations:
            task = loop.run_in_executor(executor, genrateToken, x, i)
            tasks.append(task)
            i += 1
        await asyncio.gather(*tasks)


def genrate():
    layers = layerSetup(data['layerOrder'])
    loop = asyncio.get_event_loop()
    loop.run_until_complete(createNFT(layers))


genrate()