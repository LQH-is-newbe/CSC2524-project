from flask import Flask, request, send_from_directory
from flask_cors import CORS
import json
from tasks import createNewProject, initialGeneration, annotate, adjustOrModifyGeneration

app = Flask(__name__)
CORS(app)

@app.post("/new-project")
def newProject():
    origImgF = request.files['file']
    description = request.form['description']
    id = createNewProject(origImgF)
    lastVersion = initialGeneration(id, description)
    return {'id': id, 'lastVersion': lastVersion, 'origImgName': origImgF.filename, 'isAdjust': True}

@app.post("/project")
def getProject():
    body = request.json
    id = body['id']
    with open(f'data/{id}/meta.json', 'r') as metaF:
        meta = json.load(metaF)
        origImgName = meta['originalImage']
        lastVersion = meta['lastVersion']
        isAdjust = meta['isAdjust']
    return {'id': id, 'lastVersion': lastVersion, 'origImgName': origImgName, 'isAdjust': isAdjust}

@app.post("/change-stage")
def changeStage():
    id = request.json['id']
    with open(f'data/{id}/meta.json', 'r+') as metaF:
        meta = json.load(metaF)
        meta['isAdjust'] = False
        metaF.seek(0)
        json.dump(meta, metaF)
    return ""

@app.post("/adjust-or-modify")
def adjust():
    body = request.json
    id = body['id']
    annotations = body['annotations']
    description = body['description']
    annotate(id, annotations)
    adjustOrModifyGeneration(id, annotations, description)
    return ""

@app.post("/accept")
def accept():
    id = request.json['id']
    with open(f'data/{id}/meta.json', 'r+') as metaF:
        meta = json.load(metaF)
        lastVersion = meta['lastVersion'] + 1
        meta['lastVersion'] = lastVersion
        metaF.seek(0)
        json.dump(meta, metaF)
    return {'lastVersion': lastVersion}

@app.route('/data/<path:path>')
def getData(path):
    return send_from_directory('data', path)
