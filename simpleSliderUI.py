import maya.cmds as cmds
import maya.OpenMayaUI as omui

try:
    from PySide2 import QtCore, QtWidgets
    from PySide2.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSlider, QLineEdit
    from shiboken2 import wrapInstance
except ImportError:
    from PySide6 import QtCore, QtWidgets
    from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSlider, QLineEdit
    from shiboken6 import wrapInstance


def mayaMainWindow():
    """
    Returns Maya's main window as a Python object.
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class SliderUI(QtWidgets.QDialog):

    def __init__(self, parent=mayaMainWindow()):
        super(SliderUI, self).__init__(parent)
        self.setWindowTitle("Slider UI")

        # Define slider values
        self.minVal = 2
        self.maxVal = 8
        self.defaultVal = 2

        # Main layout
        mainLayout = QVBoxLayout(self)

        # Title
        self.titleLabel = QLabel("Adjust the Value")
        self.titleLabel.setFixedHeight(100)
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        
        mainLayout.addWidget(self.titleLabel)

        # Slider layout
        sliderALayout = QHBoxLayout()
        self.sliderA = QSlider(QtCore.Qt.Horizontal)
        self.sliderA.setMinimum(self.minVal)
        self.sliderA.setMaximum(self.maxVal)
        self.sliderA.setValue(self.defaultVal)

        sliderALayout.addWidget(self.sliderA)
        mainLayout.addLayout(sliderALayout)

        # Slider value layout
        sliderNameLayout = QHBoxLayout()
        self.sliderANameLabel = QLabel("Value:")
        self.valueField = QLineEdit()
        self.valueField.setFixedWidth(50)
        self.valueField.setText(str(self.sliderA.value()))
        sliderNameLayout.addWidget(self.sliderANameLabel)
        
        sliderNameLayout.addWidget(self.valueField)
        mainLayout.addLayout(sliderNameLayout)

        # Run button layout
        runButtonLayout = QHBoxLayout()
        self.runButton = QPushButton("Print the Value")
        self.runButton.setFixedSize(200, 100)
        
        runButtonLayout.addWidget(self.runButton)
        mainLayout.addLayout(runButtonLayout)

        # Connect
        self.sliderA.valueChanged.connect(self.updateValueFieldFromSlider)
        self.valueField.editingFinished.connect(self.updateSliderFromValueField)
        self.runButton.clicked.connect(self.onRunButton)

    def updateValueFieldFromSlider(self):
        """
        Updates the value field based on the slider's value.
        """
        self.valueField.setText(str(self.sliderA.value()))

    def updateSliderFromValueField(self):
        """
        Updates the slider's value based on the value field input.
        """
        try:
            value = int(self.valueField.text())
            if self.minVal <= value <= self.maxVal:
                self.sliderA.setValue(value)
            else:
                self.valueField.setText(str(self.sliderA.value()))
        except ValueError:
            self.valueField.setText(str(self.sliderA.value()))

    def onRunButton(self):
        """
        Prints the current slider value when the Run button is clicked.
        """
        value = self.sliderA.value()
        print(f"Selected Value: {value}")

if __name__ == "__main__":
    try:
        sliderUI.close()
        sliderUI.deleteLater()
    except:
        pass

    sliderUI = SliderUI()
    sliderUI.show()
