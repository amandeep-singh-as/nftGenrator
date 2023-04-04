import json
from os import listdir
from os.path import isfile, join
from random import shuffle
from itertools import product

config = json.load(open("config.json"))
MAX_TOKENS = config['maxToken']
ORDER = config['layerOrder']

def layer_setup() -> list[list[str]]:
    layerOrder: list[str] = ORDER
    layers: list = []
    for layer in layerOrder:
        path = "./layers/" + layer
        layers.append([join(path, f) for f in listdir(path) if isfile(join(path, f))])
    unique_combinations = getUniqueCombinations(layers)

    #shuffle array to have random nft token genrations
    shuffle(unique_combinations)

    if(MAX_TOKENS != -1):
        unique_combinations = unique_combinations[:MAX_TOKENS]
    return unique_combinations

def getUniqueCombinations(layers: list[str]) -> list[list[str]]:
    return list(product(*layers))