import json
from os import listdir
from os.path import isfile, join
import itertools
from PIL import Image
import asyncio
from concurrent.futures import ThreadPoolExecutor
import imageio
import metadata
import sys

config = json.load(open("config.json"))

MAX_WORKER = config['maxWorker']

height, width = config['size']['height'], config['size']['width']


def layerSetup(layerOrder: list[str]) -> list[list[str]]:
    layers = []
    for layer in layerOrder:
        path = "./layers/" + layer
        layers.append([join(path, f)
                      for f in listdir(path) if isfile(join(path, f))])

    return getUniqueCombinations(layers)


def getUniqueCombinations(layers: list[str]) -> list[list[str]]:
    return list(itertools.product(*layers))


def generateToken(layerSet, i):
    print("Minting token ", i)
    token = Image.new("RGBA", (height, width), (0, 0, 0, 0))

    for layer in layerSet:
        img = Image.open(layer).convert("RGBA").resize((height, width))
        token.paste(img, (0, 0), img)
    metadata.genrate_metadata(i, layerSet)
    token.save("./build/tokens/NFT_" + str(i) + ".png")


def generateGIFToken(layerSet, i):
    print("Minting token ", i)
    images = []

    for layer in layerSet:
        img = Image.open(layer).convert("RGBA").resize((height, width))
        images.append(img)

    imageio.mimsave("./build/tokens/NFT_" + str(i) + ".gif", images, duration=config['durationPerImage'])


async def createNFT(layerCombinations, tokenQty=None):
    with ThreadPoolExecutor(max_workers=MAX_WORKER) as executor:
        loop = asyncio.get_event_loop()
        tasks = []
        i = 1
        if(config['tokenType'] == 'img'):

            for x in layerCombinations:
                task = loop.run_in_executor(executor, generateToken, x, i)
                tasks.append(task)
                i += 1
        elif(config['tokenType'] == 'gif'):
            for x in layerCombinations:
                task = loop.run_in_executor(executor, generateGIFToken, x, i)
                tasks.append(task)
                i += 1
        else:
            print('Invalid Config')
            sys.exit()
        await asyncio.gather(*tasks)


def genrate():
    layers = layerSetup(config['layerOrder'])
    loop = asyncio.get_event_loop()
    loop.run_until_complete(createNFT(layers))


genrate()