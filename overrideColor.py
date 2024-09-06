# Title: overrideColor.py
# DATE: 20/11/2018
# VERSION: 0.2 
# DESCRIPTION: Use this Tool to assign/override color to the selected curve

import maya.cmds as cmds


# Create the window
def xxoverrideColorxx():
    if cmds.window('OverrideColor', exists=True):
        cmds.deleteUI('OverrideColor')

    window = cmds.window('OverrideColor', s=True, title="Override Color")
    cmds.columnLayout(columnAttach=('left', 10), rowSpacing=1, columnWidth=100)

    cmds.gridLayout(numberOfColumns=15, cellWidthHeight=(18, 18))
    colors = [
        (0, 0, 0), (0.75, 0.75, 0.75), (0.5, 0.5, 0.5), (0.8, 0, 0.2),
        (0, 0, 0.4), (0, 0, 1), (0, 0.3, 0), (0.2, 0, 0.3), (0.8, 0, 0.8),
        (0.6, 0.3, 0.2), (0.25, 0.13, 0.13), (0.7, 0.2, 0), (1, 0, 0),
        (0, 1, 0), (0, 0.3, 0.6), (1, 1, 1), (1, 1, 0), (0, 1, 1),
        (1, 0.7, 0.7), (0.9, 0.7, 0.5), (1, 1, 0.4),
        (0, 0.7, 0.4), (0.6, 0.4, 0.2), (0.63, 0.63, 0.17), (0.4, 0.6, 0.2),
        (0.2, 0.63, 0.35), (0.18, 0.63, 0.63), (0.18, 0.4, 0.63),
        (0.43, 0.18, 0.63), (0.63, 0.18, 0.4)
    ]

    for i, color in enumerate(colors):
        cmds.button(l="", bgc=color, c="overrideColor({})".format(i + 1))

    cmds.setParent("..")
    cmds.columnLayout(columnAttach=('both', 10), columnWidth=280)
    cmds.button(l="Disable x Overrides", c="overrideDisabled()")
    cmds.showWindow()


# Disable overrides
def overrideDisabled():
    sel = cmds.ls(sl=True)
    for obj in sel:
        cmds.setAttr(obj + ".overrideEnabled", 0)


# Enable overrides
def overrideEnabled():
    sel = cmds.ls(sl=True)
    for obj in sel:
        cmds.setAttr(obj + ".overrideEnabled", 1)


# Apply override color
def overrideColor(colorNumber):
    sel = cmds.ls(sl=True)
    overrideEnabled()
    for obj in sel:
        cmds.setAttr(obj + ".overrideColor", colorNumber)


# Run the script
xxoverrideColorxx()
