# Bake Animation Tool: Simplify Maya Animation Baking
#
# This tool bakes animations onto selected objects and attributes in Maya. It offers
# flexible frame range options, adjustable sample rates, and the ability to include shape nodes.
#
# Key Features:
# 1. Frame Range: Playback, full, or custom start/end frames.
# 2. Sampling Rate: Set how often keyframes are created.
# 3. Shape Nodes: Option to bake shape node attributes.
# 4. Channel Box Support: Bake selected attributes or all by default.
#
# Author: Sandesh Chakradhar
# GitHub: https://github.com/svndes
# Contact: svndes@gmail.com

import maya.cmds as cmds
from PySide2.QtWidgets import *
from PySide2.QtCore import Qt
from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance


class BakeAnimationToolUI(QWidget):
    def __init__(self, parent=None):
        super(BakeAnimationToolUI, self).__init__(parent=parent)
        self.setWindowFlags(Qt.Window)
        self.setWindowTitle("Bake Animation Tool")
        self.setFixedSize(440, 260)

        layout = QVBoxLayout()
        self.setLayout(layout)

        frameRangeLayout = QHBoxLayout()
        layout.addLayout(frameRangeLayout)
        frameRangeLabel = QLabel("Frame Range")
        frameRangeLayout.addWidget(frameRangeLabel)
        self.rangeCombo = QComboBox()
        self.rangeCombo.addItems(["Playback Frame Range", "Full Frame Range", "Custom Frame Range"])
        self.rangeCombo.setFixedWidth(260)
        frameRangeLayout.addWidget(self.rangeCombo)

        startEndLayout = QHBoxLayout()
        layout.addLayout(startEndLayout)
        startEndLabel = QLabel("Start/End Frame")
        startEndLayout.addWidget(startEndLabel)
        self.startLineEdit = QLineEdit()
        self.startLineEdit.setFixedWidth(80)
        startEndLayout.addWidget(self.startLineEdit)
        self.endLineEdit = QLineEdit()
        self.endLineEdit.setFixedWidth(80)
        startEndLayout.addWidget(self.endLineEdit)

        sampleLayout = QHBoxLayout()
        layout.addLayout(sampleLayout)
        sampleLabel = QLabel("Sample by")
        sampleLayout.addWidget(sampleLabel)
        self.sampleLineEdit = QLineEdit("1.0")
        self.sampleLineEdit.setFixedWidth(80)
        sampleLayout.addWidget(self.sampleLineEdit)

        includeShapesLayout = QHBoxLayout()
        layout.addLayout(includeShapesLayout)
        includeShapesLabel = QLabel("Include Shape Nodes")
        includeShapesLayout.addWidget(includeShapesLabel)
        self.includeShapesCheckbox = QCheckBox()
        includeShapesLayout.addWidget(self.includeShapesCheckbox)

        bakeButtonLayout = QHBoxLayout()
        layout.addLayout(bakeButtonLayout)
        self.bakeButton = QPushButton("Bake Animation")
        bakeButtonLayout.addWidget(self.bakeButton)

        aboutButtonLayout = QHBoxLayout()
        layout.addLayout(aboutButtonLayout)
        self.aboutButton = QPushButton("About This Tool")
        aboutButtonLayout.addWidget(self.aboutButton)

        self.rangeCombo.currentIndexChanged.connect(self.onRangeChanged)
        self.rangeCombo.setCurrentIndex(0)
        self.onRangeChanged(0)

        self.bakeButton.clicked.connect(self.onBakeClicked)
        self.aboutButton.clicked.connect(self.showAboutDialog)

    def onRangeChanged(self, index):
        """Update start and end frames based on range selection."""
        selectedRange = self.rangeCombo.currentText()
        if selectedRange == "Playback Frame Range":
            startTime = cmds.playbackOptions(q=True, minTime=True)
            endTime = cmds.playbackOptions(q=True, maxTime=True)
            self.startLineEdit.setEnabled(False)
            self.endLineEdit.setEnabled(False)
        elif selectedRange == "Full Frame Range":
            startTime = cmds.playbackOptions(q=True, animationStartTime=True)
            endTime = cmds.playbackOptions(q=True, animationEndTime=True)
            self.startLineEdit.setEnabled(False)
            self.endLineEdit.setEnabled(False)
        elif selectedRange == "Custom Frame Range":
            startTime = cmds.playbackOptions(q=True, minTime=True)
            endTime = cmds.playbackOptions(q=True, maxTime=True)
            self.startLineEdit.setEnabled(True)
            self.endLineEdit.setEnabled(True)
        self.startLineEdit.setText(str(startTime))
        self.endLineEdit.setText(str(endTime))

    def onBakeClicked(self):
        """Bake animation"""
        startValue = float(self.startLineEdit.text())
        endValue = float(self.endLineEdit.text())
        sampleValue = float(self.sampleLineEdit.text())
        includeShapes = self.includeShapesCheckbox.isChecked()

        selectedObjects = cmds.ls(selection=True)
        if not selectedObjects:
            cmds.warning("Please select an object to bake animation.")
            return

        channelBox = cmds.channelBox("mainChannelBox", q=True, sma=True)
        cmds.refresh(suspend=True)

        if channelBox:
            cmds.bakeResults(
                selectedObjects,
                simulation=True,
                t=(startValue, endValue),
                sampleBy=sampleValue,
                preserveOutsideKeys=True,
                sparseAnimCurveBake=False,
                removeBakedAttributeFromLayer=False,
                bakeOnOverrideLayer=False,
                minimizeRotation=True,
                controlPoints=False,
                shape=includeShapes,
                at=channelBox
            )
        else:
            cmds.bakeResults(
                selectedObjects,
                simulation=True,
                t=(startValue, endValue),
                sampleBy=sampleValue,
                preserveOutsideKeys=True,
                sparseAnimCurveBake=False,
                removeBakedAttributeFromLayer=False,
                bakeOnOverrideLayer=False,
                minimizeRotation=True,
                controlPoints=False,
                shape=includeShapes
            )

        cmds.refresh(suspend=False)

    def showAboutDialog(self):
        """Show the 'About' dialog."""
        aboutDialog = QDialog(self)
        aboutDialog.setWindowTitle("About This Tool")
        aboutDialog.setMinimumSize(720, 720)
        layout = QVBoxLayout()
        aboutDialog.setLayout(layout)
        aboutText = QTextEdit()
        aboutText.setText(
            "Bake Animation Tool\n\n"
            "A Maya Python UI tool for baking animation onto selected objects and selected attributes.\n\n"
            "Features:\n"
            "  Frame Range Options:\n"
            "     - Playback Frame Range: The frames that are shown while you play the animation.\n"
            "     - Full Frame Range: All the frames set in the time slider.\n"
            "     - Custom Frame Range: Frames that you choose manually.\n\n"
            "  Start/End Frame:\n"
            "     - Set the range for baking make sure to select Custom Frame Range.\n\n"
            "  Sample By:\n"
            "     - Decide how often to set keyframes during baking.\n\n"
            "  Include Shape Nodes:\n"
            "     - Choose whether to bake attributes of shape nodes when you're baking everything.\n\n"
            "  Bake Animation:\n"
            "     - Start the baking process with the settings you've chosen.\n\n"
            "Author:\n"
            "   Sandesh Chakradhar\n"
            "   svndes@gmail.com\n"
            "   https://www.linkedin.com/in/sandesh-chakradhar-172552287\n\n"
            "Source Code:\n"
            "   https://github.com/svndes\n"
        )
        aboutText.setReadOnly(True)
        aboutText.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(aboutText)
        okButton = QPushButton("OK")
        okButton.clicked.connect(aboutDialog.accept)
        layout.addWidget(okButton)
        aboutDialog.exec_()


def run():
    if QApplication.instance():
        for win in QApplication.allWindows():
            if "BakeAnimationToolWindow" in win.objectName():
                win.destroy()
    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QWidget)
    BakeAnimationToolUI.window = BakeAnimationToolUI(parent=mayaMainWindow)
    BakeAnimationToolUI.window.setObjectName("BakeAnimationToolWindow")
    BakeAnimationToolUI.window.setWindowTitle('Bake Animation')
    BakeAnimationToolUI.window.show()


run()
