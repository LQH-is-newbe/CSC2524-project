import json
import base64
from prompts import initGenPrompt, adjustGenPrompt, selfRevisionPrompt, modifyGenPrompt
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

def initialGeneration(id, description):
    with open(f'data/{id}/meta.json', 'r') as metaF:
        origImgName = json.load(metaF)['originalImage']
    with open(f'data/{id}/{origImgName}', "rb") as origImgF:
        origImg = base64.b64encode(origImgF.read()).decode("utf-8")
    with open(f'data/{id}/original_description.txt', 'w') as descF:
        descF.write(description)
    html = initGenPrompt(origImg, description)
    with open(f'data/{id}/0.html', 'w') as html_f:
        html_f.write(html)
    takeScreenshot(f'data/{id}/0.html')
    return 0

def annotate(id, annotations):
    with open(f'data/{id}/meta.json', 'r') as metaF:
        lastVersion = json.load(metaF)['lastVersion']
    annotateImage(f'data/{id}/{lastVersion}.png', annotations)

def adjustOrModifyGeneration(id, annotations, description):
    with open(f'data/{id}/meta.json', 'r') as metaF:
        meta = json.load(metaF)
        origImgName = meta['originalImage']
        lastVersion = meta['lastVersion']
        isAdjust = meta['isAdjust']
    genImagePath = f'data/{id}/{lastVersion}_annotated.png' if len(annotations) > 0 else f'data/{id}/{lastVersion}.png'
    with open(genImagePath, "rb") as genImageF:
        genImg = base64.b64encode(genImageF.read()).decode("utf-8")
    with open(f'data/{id}/{lastVersion}.html', "r") as genHtmlF:
        genHtml = genHtmlF.read()
    with open(f'data/{id}/{lastVersion}_description.txt', 'w') as descF:
        descF.write(description)
    annotationDescriptions = []
    if len(annotations) > 0:
        for i, annotation in enumerate(annotations):
            annotationDescriptions.append((chr(ord('A')+i), annotation['label']))
        with open(f'data/{id}/{lastVersion}_annotations.txt', 'w') as annotationsF:
            for annotationDescription in annotationDescriptions:
                annotationsF.write(f'{annotationDescription[0]}: {annotationDescription[1]}\n')
    if isAdjust:
        with open(f'data/{id}/{origImgName}', "rb") as origImgF:
            origImg = base64.b64encode(origImgF.read()).decode("utf-8")
        if len(description) > 0 or len(annotationDescriptions) > 0:
            html = adjustGenPrompt(origImg, genImg, genHtml, annotationDescriptions, description)
        else:
            html = selfRevisionPrompt(origImg, genImg, genHtml)
    else:
        html = modifyGenPrompt(genImg, genHtml, annotationDescriptions, description)
    with open(f'data/{id}/{lastVersion+1}.html', 'w') as html_f:
        html_f.write(html)
    takeScreenshot(f'data/{id}/{lastVersion+1}.html')