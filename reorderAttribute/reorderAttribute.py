# Creates a window in Maya for reordering user-defined attributes.
# Allows users to move these attributes up or down.
# Works with attributes visible in the channel box.

import pymel.core as pm


def reorderAttrUi():
    # Check if the window exists and delete it if so
    if pm.window('_ReorderAttrWindow', query=True, exists=True):
        pm.deleteUI('_ReorderAttrWindow', window=True)

    # Create the main window for reordering attributes
    reorderAttrWin = pm.window(
        '_ReorderAttrWindow',
        title="Reorder Attribute",
        widthHeight=(200, 125),
        menuBar=False, sizeable=False,
        minimizeButton=False,
        maximizeButton=False,
        menuBarVisible=False,
        titleBar=True
    )

    # Layout for the buttons
    pm.columnLayout('reorderAttrLayout', columnAttach=("both", 50))
    pm.separator(style='none', h=7)

    # Button to move attributes up
    pm.button(label='UP UP UP', w=100, h=50, command=moveAttrUp)
    pm.separator(style='in', h=5, w=100)

    # Button to move attributes down
    pm.button(label='down down', w=100, h=50, command=moveAttrDown)

    # Show the window
    pm.showWindow(reorderAttrWin)


def moveAttrUp(*args):
    # Move the selected attribute up
    moveAttr(1)


def moveAttrDown(*args):
    # Move the selected attribute down
    moveAttr(0)


def moveAttr(mode, *args):
    pm.scriptEditorInfo(suppressInfo=False)  # Enable script editor info
    objList = pm.channelBox('mainChannelBox', query=True, mainObjectList=True)  # Get selected objects

    if objList:
        attrList = pm.channelBox('mainChannelBox', query=True, selectedMainAttributes=True)  # Get selected attributes

        if attrList:
            for obj in objList:
                userDefAttrList = pm.listAttr(obj, userDefined=True)  # List user-defined attributes

                if userDefAttrList and attrList[0] in userDefAttrList:
                    pm.scriptEditorInfo(suppressInfo=True)
                    lockAttrList = pm.listAttr(obj, userDefined=True, locked=True)  # Check for locked attributes

                    # Unlock attributes if they are locked
                    if lockAttrList:
                        for lockAttr in lockAttrList:
                            pm.setAttr(obj + "." + lockAttr, lock=False)

                    # Handle moving attributes down
                    if mode == 0:
                        sortedList = attrList[::-1] if len(attrList) > 1 else attrList
                        for i in sortedList:
                            attrLs = pm.listAttr(obj, userDefined=True)
                            attrPos = attrLs.index(i)
                            pm.deleteAttr(obj, at=attrLs[attrPos])  # Delete the selected attribute
                            pm.undo()
                            for x in range(attrPos + 2, len(attrLs), 1):
                                pm.deleteAttr(obj, at=attrLs[x])  # Delete subsequent attributes
                                pm.undo()
                    # Handle moving attributes up
                    elif mode == 1:
                        for i in attrList:
                            attrLs = pm.listAttr(obj, userDefined=True)
                            attrPos = attrLs.index(i)
                            if attrPos > 0:
                                pm.deleteAttr(obj, at=attrLs[attrPos - 1])  # Delete the previous attribute
                                pm.undo()
                                for x in range(attrPos + 1, len(attrLs), 1):
                                    pm.deleteAttr(obj, at=attrLs[x])  # Delete subsequent attributes
                                    pm.undo()

                    # Relock attributes if they were originally locked
                    if lockAttrList:
                        for lockAttr in lockAttrList:
                            pm.setAttr(obj + "." + lockAttr, lock=True)
                else:
                    pm.warning('Selected attribute cannot be moved.')
        else:
            pm.warning('Please select one or more attributes.')
    else:
        pm.warning('Please select one or more transform nodes.')

    pm.scriptEditorInfo(suppressInfo=True)


# Execute the UI function
reorderAttrUi()
