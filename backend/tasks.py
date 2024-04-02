import json
import base64
from prompts import initGenPrompt, adjustGenPrompt, modifyGenPrompt
import uuid
import os
from utils import takeScreenshot, annotateImage

def createNewProject(origImgF):
    id = str(uuid.uuid4())
    os.makedirs(f'data/{id}')
    origImgF.save(f'data/{id}/{origImgF.filename}')
    with open(f'data/{id}/meta.json', 'w') as meta:
        json.dump({'originalImage': origImgF.filename, 'lastVersion': 0, 'isAdjust': True}, meta)
    return id

def initialGeneration(id):
    with open(f'data/{id}/meta.json', 'r') as metaF:
        origImgName = json.load(metaF)['originalImage']
    with open(f'data/{id}/{origImgName}', "rb") as origImgF:
        origImg = base64.b64encode(origImgF.read()).decode("utf-8")
    html = initGenPrompt(origImg)
    with open(f'data/{id}/0.html', 'w') as html_f:
        html_f.write(html)
    takeScreenshot(f'data/{id}/0.html')
    return 0

def annotate(id, annotations):
    with open(f'data/{id}/meta.json', 'r') as metaF:
        lastVersion = json.load(metaF)['lastVersion']
    annotateImage(f'data/{id}/{lastVersion}.png', annotations)

def adjustOrModifyGeneration(id, annotations):
    with open(f'data/{id}/meta.json', 'r') as metaF:
        meta = json.load(metaF)
        origImgName = meta['originalImage']
        lastVersion = meta['lastVersion']
        isAdjust = meta['isAdjust']
    genImagePath = f'data/{id}/{lastVersion}_annotated.png' if len(annotations) > 0 else f'data/{id}/{lastVersion}.png'
    with open(genImagePath, "rb") as genImageF:
        genImg = base64.b64encode(genImageF.read()).decode("utf-8")
    if isAdjust:
        with open(f'data/{id}/{origImgName}', "rb") as origImgF:
            origImg = base64.b64encode(origImgF.read()).decode("utf-8")
        html = adjustGenPrompt(origImg, genImg, annotations)
    else:
        html = modifyGenPrompt(genImg, annotations)
    with open(f'data/{id}/{lastVersion+1}.html', 'w') as html_f:
        html_f.write(html)
    takeScreenshot(f'data/{id}/{lastVersion+1}.html')
    with open(f'data/{id}/meta.json', 'r+') as metaF:
        meta = json.load(metaF)
        meta['lastVersion'] = lastVersion+1
        metaF.seek(0)
        json.dump(meta, metaF)
    return lastVersion+1

    
    