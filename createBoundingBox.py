# Create bounding boxes around selected objects.
# You can select multiple objects and click 'Create Bounding Box' to generate bounding boxes.
# Bounding boxes are named based on the original object name with '_BBox' suffix.
import maya.cmds as cmds

def command(*args):
    selectedGeo = cmds.ls(sl=True)

    if selectedGeo:
        for geo in selectedGeo:
            name = geo + "_BBox"
            split = geo.rsplit(":")
            if len(split) >= 2:
                name = split[0] + "_BBox"
            else:
                print(geo)
                name = geo.rsplit("_")[0] + "_BBox"
            dup = cmds.duplicate(geo, n=name)[0]
            box = cmds.geomToBBox(dup, n=dup, single=True)[0]

def UI():
    if cmds.window("bBoxWin", exists=True):
        cmds.deleteUI("bBoxWin")
    cmds.window("bBoxWin", t="Bounding Box Window")
    cmds.columnLayout(adjustableColumn=True)
    cmds.text(l="You can select multiple objects")
    cmds.button(l="Create Bounding Box", c=command, h=60, w=300, bgc=[0.1, 0.1, 0.1])
    cmds.showWindow("bBoxWin")


if __name__ == "__main__":
    UI()

