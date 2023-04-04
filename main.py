import json
import asyncio
from concurrent.futures import ThreadPoolExecutor
from metadata import genrate_metadata
from genrate import genrateGIFTokens, genrateTokens
from utils import bColors
from sys import exit
from setup import layer_setup

config = json.load(open("config.json"))

MAX_WORKER = int(config["maxWorker"])
TOKEN = config["tokenType"]

async def createNFT(combinations: list[list[str]], tokenQty: int | None = None):
    with ThreadPoolExecutor(max_workers=MAX_WORKER) as executor:
        loop = asyncio.get_event_loop()
        tasks, metadata_tasks, token_version = [], [], 1
        
        for layers in combinations:
            if(TOKEN == 'img'):
                task = loop.run_in_executor(executor, genrateTokens, layers, token_version)
            elif(TOKEN == 'gif'):
                task = loop.run_in_executor(executor, genrateGIFTokens, layers, token_version)
            else:
                print(f"{bColors.bcolors.FAIL}Invalid Config {bColors.bcolors.ENDC}")
                exit()
            metadata_task = loop.run_in_executor(executor, genrate_metadata, layers, token_version)

            tasks.append(task)
            metadata_tasks.append(metadata_task)
            token_version += 1
        await asyncio.gather(*tasks)
        await asyncio.gather(*metadata_tasks)

def genrate():
    layers = layer_setup()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(createNFT(layers))

genrate()
