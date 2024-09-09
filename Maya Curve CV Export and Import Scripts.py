# This script contains two functions:
# 1. Export CV positions of selected curves to JSON files.
# 2. Import CV positions from JSON files and update the selected curves.
# 3. Make sure to set the correct folder paths,
# 4. select curves, and ensure JSON files are named appropriately before running each part.

"""Export CV """
# Select the curves you want to save,
# then run this script to export their CV positions to JSON files.
# Make sure the folder where the files will be saved exists or will be created automatically.

import maya.cmds as cmds
import json
import os

exportToPath = ''  # Set your export path here
folderPath = os.path.join(exportToPath, '_exportFolder')

# Create the folder if it doesn't exist
if not os.path.exists(folderPath):
    os.makedirs(folderPath)

selection = cmds.ls(selection=True)
for sel in selection:
    curveName = cmds.listRelatives(sel, s=True)[0]
    cvs = cmds.ls(f"{curveName}.cv[*]", fl=True)
    pointList = []
    for cv in cvs:
        pos = cmds.pointPosition(cv)
        pointList.append(pos)
    curveData = {
        "pointList": pointList
    }
    fileName = f"{curveName}.json"
    filePath = os.path.join(folderPath, fileName)
    # Save CV data to JSON file
    with open(filePath, 'w') as jsonFile:
        json.dump(curveData, jsonFile, indent=4)


"""Import CV """
# Select the curves you want to update,
# then run this script to load their CV positions from JSON files.
# Ensure the JSON files are in the correct folder before running the script.

import maya.cmds as cmds
import json
import os

importFromPath = ''  # Set your import path here
folderPath = os.path.join(importFromPath, '_exportFolder')

selection = cmds.ls(selection=True)
for sel in selection:
    curveName = cmds.listRelatives(sel, s=True)[0]
    fileName = f"{curveName}.json"
    filePath = os.path.join(folderPath, fileName)
    try:
        # Load CV data from JSON file
        if not os.path.exists(filePath):
            print(f"File {filePath} not found.")
            continue
        with open(filePath, 'r') as jsonFile:
            curveData = json.load(jsonFile)
        cvs = cmds.ls(f"{curveName}.cv[*]", fl=True)
        pointList = curveData.get("pointList", [])
        if len(pointList) != len(cvs):
            print("Mismatch between number of CVs in curve and points in the JSON file.")
            continue
        for i, cv in enumerate(cvs):
            cmds.move(pointList[i][0], pointList[i][1], pointList[i][2], cv)
    except Exception as e:
        print(f"An error occurred: {e}")
