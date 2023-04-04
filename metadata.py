import json
from datetime import date
import hashlib


config = json.load(open('config.json'))
template = json.load(open('template.json'))

project_name = config['projectName']
description = config['description']
layer_order = config['layerOrder']
date_var = date.today()

def genrate_metadata(attributes, edition):
    template['name'] = project_name + " : " + str(edition)
    template['description'] = description
    template['edition'] = edition
    template['date'] = str(date_var)
    template['sha1'] = genrate_hash(''.join(attributes))
    attributes_values = []

    for i in range(len(layer_order)):
        attributes_values.append({
            "trait_types": layer_order[i],
            "value": attributes[i]
        })
    template['attributes'] = attributes_values

    with open("./build/metadata/NFT_" + str(edition) +"_metadata.json", "w") as outfile:
        json.dump(template, outfile)

def genrate_hash(attributes):
    hash_object = hashlib.sha1(attributes.encode('ascii'))
    return hash_object.hexdigest()