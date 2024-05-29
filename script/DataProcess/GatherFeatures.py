import os
import numpy as np
import pickle

fileNames = []

symmetry = []

eyeBetween = []
eyeFront = []
eyeBack = []
eyeLength = []
eyeAbove = []
eyeBelow = []
eyeDegree = []

browBetween = []
browFront = []
browBack = []
browDegree = []
browThickness = []
browShape = []
browArchPosition = []

noseLength = []
noseBridgeThickness = []
noseHeadThickness = []
noseAlar = []
philtrum = []

lipLength = []
upperLipThickness = []
lowerLipThickness = []

foreheadLength = []
midfaceLength = []

chinLength = []
chinWidth = []

jawWide = []
jawPosition = []

skinColor = []
lipColor = []


# load dictionary from path
def load_dict(path):
    pickle_in = open(path, "rb")
    return pickle.load(pickle_in)

def LoadValues(path):
    dicts = load_dict(path)

    symmetry.append(dicts['symmetry'])
    eyeBetween.append(dicts['eyeBetween'])
    eyeFront.append(dicts['eyeFront'])
    eyeBack.append(dicts['eyeBack'])
    eyeLength.append(dicts['eyeLength'])
    eyeAbove.append(dicts['eyeAbove'])
    eyeBelow.append(dicts['eyeBelow'])
    eyeDegree.append(dicts['eyeDegree'])

    browBetween.append(dicts['browBetween'])
    browFront.append(dicts['browFront'])
    browBack.append(dicts['browBack'])
    browDegree.append(dicts['browDegree'])
    browThickness.append(dicts['browThickness'])
    browShape.append(dicts['browShape'])
    browArchPosition.append(dicts['browArchPosition'])

    noseLength.append(dicts['noseLength'])
    noseBridgeThickness.append(dicts['noseBridgeThickness'])
    noseHeadThickness.append(dicts['noseHeadThickness'])
    noseAlar.append(dicts['noseAlar'])
    philtrum.append(dicts['philtrum'])

    lipLength.append(dicts['lipLength'])
    upperLipThickness.append(dicts['upperLipThickness'])
    lowerLipThickness.append(dicts['lowerLipThickness'])

    foreheadLength.append(dicts['foreheadLength'])
    midfaceLength.append(dicts['midfaceLength'])
    chinLength.append(dicts['chinLength'])
    chinWidth.append(dicts['chinWidth'])

    jawWide.append(dicts['jawWide'])
    jawPosition.append(dicts['jawPosition'])

    skinColor.append(dicts['skinColor'])
    lipColor.append(dicts['lipColor'])

def LoadBatch(path):
    for file in os.listdir(path):
        if file.endswith('.pickle'):
            fileNames.append(file)
            LoadValues(f'{path}/{file}')
            

def SaveValues(pathName = 'FaceOn/data/numbers/All.pickle'):
    values = {
        'fileNames': fileNames,
        'symmetry': symmetry,
        'eyeBetween': eyeBetween,
        'eyeFront': eyeFront,
        'eyeBack': eyeBack,
        'eyeLength': eyeLength,
        'eyeAbove': eyeAbove,
        'eyeBelow': eyeBelow,
        'eyeDegree': eyeDegree,

        'browBetween': browBetween,
        'browFront': browFront,
        'browBack': browBack,
        'browDegree': browDegree,
        'browThickness': browThickness,
        'browShape': browShape,
        'browArchPosition': browArchPosition,

        'noseLength': noseLength,
        'noseBridgeThickness': noseBridgeThickness,
        'noseHeadThickness': noseHeadThickness,
        'noseAlar': noseAlar,
        'philtrum': philtrum,

        'lipLength': lipLength,
        'upperLipThickness': upperLipThickness,
        'lowerLipThickness': lowerLipThickness,

        'foreheadLength': foreheadLength,
        'midfaceLength': midfaceLength,

        'chinLength': chinLength,
        'chinWidth': chinWidth,

        'jawWide': jawWide,
        'jawPosition': jawPosition,

        'skinColor': skinColor,
        'lipColor': lipColor
    }

    with open(pathName, 'wb') as handle:
        pickle.dump(values, handle, protocol=pickle.HIGHEST_PROTOCOL)

    print( pathName + ' saved')

def SaveBatch(path, extract_path = 'FaceOn/data/numbers/All.pickle'):
    LoadBatch(path)
    SaveValues(extract_path)
