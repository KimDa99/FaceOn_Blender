import os
import numpy as np
import pickle

eyeBetween = []
eyeFront = []
eyeBack = []
eyeAbove = []
eyeBelow = []
eyeDegree = []

browBetween = []
browFront = []
browBack = []
browDegree = []
browThickness = []
browShape = []

noseLength = []
noseBridgeThickness = []
noseAlar = []
philtrum = []

lipLength = []
upperLipThickness = []
lowerLipThickness = []

foreheadLength = []
chinLength = []

jaw = []
jawPosition = []

skinColor = []
lipColor = []


# load dictionary from path
def load_dict(path):
    pickle_in = open(path, "rb")
    return pickle.load(pickle_in)

def LoadValues(path):
    dicts = load_dict(path)
    eyeBetween.append(dicts['eyeBetween'])
    eyeFront.append(dicts['eyeFront'])
    eyeBack.append(dicts['eyeBack'])
    eyeAbove.append(dicts['eyeAbove'])
    eyeBelow.append(dicts['eyeBelow'])
    eyeDegree.append(dicts['eyeDegree'])

    browBetween.append(dicts['browBetween'])
    browFront.append(dicts['browFront'])
    browBack.append(dicts['browBack'])
    browDegree.append(dicts['browDegree'])
    browThickness.append(dicts['browThickness'])
    browShape.append(dicts['browShape'])

    noseLength.append(dicts['noseLength'])
    noseBridgeThickness.append(dicts['noseBridgeThickness'])
    noseAlar.append(dicts['noseAlar'])
    philtrum.append(dicts['philtrum'])

    lipLength.append(dicts['lipLength'])
    upperLipThickness.append(dicts['upperLipThickness'])
    lowerLipThickness.append(dicts['lowerLipThickness'])

    foreheadLength.append(dicts['foreheadLength'])
    chinLength.append(dicts['chinLength'])

    jaw.append(dicts['jaw'])
    jawPosition.append(dicts['jawPosition'])

    skinColor.append(dicts['skinColor'])
    lipColor.append(dicts['lipColor'])

def LoadBatch(path):
    for file in os.listdir(path):
        if file.endswith('.pickle'):
            print(file)
            load_dict(f'{path}/{file}')
            LoadValues(f'{path}/{file}')
            

def SaveValues():
    values = {
        'eyeBetween': eyeBetween,
        'eyeFront': eyeFront,
        'eyeBack': eyeBack,
        'eyeAbove': eyeAbove,
        'eyeBelow': eyeBelow,
        'eyeDegree': eyeDegree,

        'browBetween': browBetween,
        'browFront': browFront,
        'browBack': browBack,
        'browDegree': browDegree,
        'browThickness': browThickness,
        'browShape': browShape,

        'noseLength': noseLength,
        'noseBridgeThickness': noseBridgeThickness,
        'noseAlar': noseAlar,
        'philtrum': philtrum,

        'lipLength': lipLength,
        'upperLipThickness': upperLipThickness,
        'lowerLipThickness': lowerLipThickness,

        'foreheadLength': foreheadLength,
        'chinLength': chinLength,

        'jaw': jaw,
        'jawPosition': jawPosition,

        'skinColor': skinColor,
        'lipColor': lipColor
    }

    with open('FaceOn/data/numbers/All.pickle', 'wb') as handle:
        pickle.dump(values, handle, protocol=pickle.HIGHEST_PROTOCOL)

    print('FaceOn/data/numbers/All.pickle saved')

LoadBatch(path ='FaceOn/data/numbers/part1')
LoadBatch(path ='FaceOn/data/numbers/part2')
LoadBatch(path ='FaceOn/data/numbers/part3')

SaveValues()