# FaceOn_Blender
Character Face builder by extracting face features from a given image in Blender.

https://github.com/KimDa99/FaceOn_UE/assets/91198933/2cc563f6-8b4c-4f1b-8adb-52ae18acb794

## Features can be applied to Blender asset
### Eyes
- Eye Degree
- Eye Between
- Eye Below
- Eye Above
- Eye Length

### Eyebrows
- Between
- Shape
- Degree

### Nose
- Nose Bridge Width
- Nose Head Width
- Nose Alar Width
- Nose Length

### Lips
- UpperLip Thickness
- UnderLip Thickness
- Lip Length

### Face Line
- Philtrum Length
- Jaw size
- Chin Width
- Chin Length

# How to use
1. Calculate Features to extract values of face feature in Script/GetPicture_and_Calculate.py
![image](https://github.com/KimDa99/FaceOn_Blender/assets/91198933/e09f88c4-5a44-4846-8960-3f98566d0a31)
- write 'your_target_image_path' on image_path
- write 'your_desired_value_path' on saving_path
  
2. Copy&Paste the value text on Blender script. Select the applying meshes & click 'Run'
   ![image](https://github.com/KimDa99/FaceOn_Blender/assets/91198933/a1720f78-712a-4b17-8e2e-2e9335a9db56)
   - the Blender script 'ChangeShapeKeyColor.py' is linked inside with 'Model/BasicFace.blend'
     - if you can not find it, you can use "script\ChangeShapeKeyColor_Blender.py"
   - Before running the script, you need to select the Face objects to apply.

# How it was made
1. Get Feature data for standard
  - Get Sample images  
  - Used Mediapipe for extracting landmarks of faces.
  - Calculate face features from landmarks - and find the mean, Max, and min values of each feature to make standards.
2. Get features of the target, and evaluate how they are close to each criterion value.
3. Prepare the model with shape keys(morph targets) and map with evaluated value

# Things to improve
1. color detection:
  - skin, lip color
  - eye Color, brow color
2. face detection
  - brow, forehead
3. apply depth of face
  - nose, frontal bone, zygomatic bone, and mouth 
