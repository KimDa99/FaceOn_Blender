"""
import GetSamples
GetSamples.OpenTarGz('FaceOn/data/part1.tar.gz', 'FaceOn/data/samples')
GetSamples.OpenTarGz('FaceOn/data/part2.tar.gz', 'FaceOn/data/samples')
GetSamples.OpenTarGz('FaceOn/data/part3.tar.gz', 'FaceOn/data/samples')

GetSamples.MoveFiles('FaceOn/data/samples/part1', 'FaceOn/data/samples')
GetSamples.MoveFiles('FaceOn/data/samples/part2', 'FaceOn/data/samples')
GetSamples.MoveFiles('FaceOn/data/samples/part3', 'FaceOn/data/samples')

print('Done')

import GetLandmarks
GetLandmarks.process_images('FaceOn/data/samples', 'FaceOn/data/landmarks')

print('Done1')

import normalizePoints
normalizePoints.SaveNormalizedBatch('FaceOn/data/landmarks', 'FaceOn/data/xyzNormalized/normalized')

print('Done2')
"""

import CombineColorNormalizedPoints
CombineColorNormalizedPoints.combineNormalizedPoints('FaceOn/data/xyzNormalized/normalized', 'FaceOn/data/landmarks', 'FaceOn/data/xyzNormalized/combined_Normalized')

print('Done3')

import CalculateFeatures
CalculateFeatures.SaveBatchValues('FaceOn/data/xyzNormalized/combined_Normalized', 'FaceOn/data/xyzNormalized/numbers')

print('Done4')

import GatherFeatures
GatherFeatures.SaveBatch('FaceOn/data/xyzNormalized/numbers', 'FaceOn/data/xyzNormalized/Gathered_Features.pickle')