names = ["eyeBetween", "eyeFront", "eyeBack", "eyeLength", "eyeAbove", "eyeBelow", "eyeDegree", "browBetween", "browFront", "browBack", "browDegree", "browThickness", "browShape", "browArchPosition", "noseLength", "noseBridgeThickness", "noseHeadThickness", "noseAlar", "philtrum", "lipLength", "upperLipThickness", "lowerLipThickness", "foreheadLength", "midfaceLength", "chinLength", "chinWidth", "jawWide", "jawPosition", ]
values = [-0.5822599149364703, -0.3251401730389502, -0.6354675978042565, -0.6577861076105616, 0.07462516465112781, -0.5752791241317683, -0.17028655515463145, -1.057097636787573, -0.4502935399883409, 0.2637779569192916, -0.061219574799682874, 0.013908432329603404, -0.2749170918100383, -0.9658306980661262, 0.13030057917262305, -0.6798831365804722, -0.15450074267698888, 0.050600071537507986, -0.15742229444700134, -0.1650853983515229, 0.16984419303638604, -0.004924041611259767, 0.39933375486810035, 0.3696944387847551, 0.351343668172112, 0.13161794407130933, 0.3486789514896077, -0.05032380415497438, ]
skinColor = [0.5490196078431373, 0.2901960784313726, 0.19607843137254902, ]
lipColor = [0.448573975044563, 0.18627450980392155, 0.1254901960784313, ]


import bpy

# Iterate over all selected objects
for obj in bpy.context.selected_objects:
    if obj.type == 'MESH':
        # Check if the mesh has shape keys
        if obj.data.shape_keys:
            # Get the shape keys
            shape_keys = obj.data.shape_keys.key_blocks

            for name, value in zip(names, values):
                MaxName = name + "_Max"
                minName = name + "_min"

                # Determine the values to apply based on the sign of value
                if value >= 0:
                    MaxValue = value
                    minValue = 0
                else:
                    MaxValue = 0
                    minValue = -value

                # Apply values to the corresponding shape keys
                if MaxName in shape_keys:
                    shape_key = shape_keys[MaxName]
                    shape_key.value = MaxValue
                else:
                    print(f"Shape key '{MaxName}' not found.")

                if minName in shape_keys:
                    shape_key = shape_keys[minName]
                    shape_key.value = minValue
                else:
                    print(f"Shape key '{minName}' not found.")
        else:
            print(f"Selected mesh {obj.name} does not have any shape keys.")

        # Change the color of the material named 'lipColor'
        for material in obj.data.materials:
            if material.name == 'lipColor':
                # Assuming the material uses a Principled BSDF node
                if material.node_tree:
                    nodes = material.node_tree.nodes
                    principled_node = nodes.get("Principled BSDF")
                    if principled_node:
                        principled_node.inputs['Base Color'].default_value = lipColor + [1]  # Adding alpha value 1 for RGBA
                    else:
                        print(f"No Principled BSDF node found in material '{material.name}'.")
                else:
                    print(f"No node tree found in material '{material.name}'.")
            else:
                print(f"Material 'lipColor' not found in mesh '{obj.name}'.")
        
        for material in obj.data.materials:
            if material.name == 'skinColor':
                # Assuming the material uses a Principled BSDF node
                if material.node_tree:
                    nodes = material.node_tree.nodes
                    principled_node = nodes.get("Principled BSDF")
                    if principled_node:
                        principled_node.inputs['Base Color'].default_value = skinColor + [1]  # Adding alpha value 1 for RGBA
                    else:
                        print(f"No Principled BSDF node found in material '{material.name}'.")
                else:
                    print(f"No node tree found in material '{material.name}'.")
            else:
                print(f"Material 'lipColor' not found in mesh '{obj.name}'.")
        

    else:
        print(f"Selected object {obj.name} is not a mesh.")
