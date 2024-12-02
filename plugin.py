import os
from qgis.PyQt.QtCore import QCoreApplication, QVariant
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QMainWindow, QFileDialog, QMessageBox, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from qgis.core import QgsProject
from .resources import *
from .ui_mainwindow import Ui_MainWindow

class QGISColorRampGenerator(QMainWindow, Ui_MainWindow):
    def __init__(self, iface):
        super().__init__()
        self.iface = iface
        self.setupUi(self)
        self.rampCount = 0
        self.addRampButton.clicked.connect(self.addRamp)
        self.generateXMLButton.clicked.connect(self.generateXML)
        self.plugin_dir = os.path.dirname(__file__)
        self.actions = []
        self.menu = self.tr(u'&QGIS Color Ramp Generator')
        self.toolbar = self.iface.addToolBar(u'QGISColorRampGenerator')
        self.toolbar.setObjectName(u'QGISColorRampGenerator')

    def initGui(self):
        icon_path = ':/plugins/qgis_color_ramp_generator/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'QGIS Color Ramp Generator'),
            callback=self.run,
            parent=self.iface.mainWindow())

    def unload(self):
        for action in self.actions:
            self.iface.removePluginMenu(self.tr(u'&QGIS Color Ramp Generator'), action)
            self.iface.removeToolBarIcon(action)
        del self.toolbar

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)
        if status_tip is not None:
            action.setStatusTip(status_tip)
        if whats_this is not None:
            action.setWhatsThis(whats_this)
        if add_to_menu:
            self.iface.addPluginToMenu(self.menu, action)
        if add_to_toolbar:
            self.toolbar.addAction(action)
        self.actions.append(action)
        return action

    def run(self):
        self.show()

    def addRamp(self):
        if self.rampCount < 10:
            self.rampCount += 1
            newRampId = f"rampGroup{self.rampCount}"
            rampWidget = self.createRampWidget(newRampId)
            self.rampContainerLayout.addWidget(rampWidget)
        else:
            QMessageBox.warning(self, "Limit Reached", "Maximum 10 ramps allowed!")

    def createRampWidget(self, rampId):
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        widget.setObjectName(rampId)

        colorLabel = QLabel("Enter Hex Color Codes (comma-separated):")
        colorInput = QLineEdit("#000000,#FFFFFF,#FF0000")
        colorInput.setObjectName(f"colorInput{self.rampCount}")
        colorInput.textChanged.connect(lambda: self.updateColorViewers(rampId))

        rampNameLabel = QLabel("Ramp Name:")
        rampNameInput = QLineEdit(f"MyColorRamp{self.rampCount}")
        rampNameInput.setObjectName(f"rampName{self.rampCount}")

        rampTagsLabel = QLabel("Ramp Tags (comma-separated):")
        rampTagsInput = QLineEdit(f"custom,ramp{self.rampCount}")
        rampTagsInput.setObjectName(f"rampTags{self.rampCount}")

        deleteButton = QPushButton("Delete")
        deleteButton.setObjectName(f"deleteButton{self.rampCount}")
        deleteButton.clicked.connect(lambda: self.deleteRamp(rampId))

        layout.addWidget(colorLabel)
        layout.addWidget(colorInput)
        layout.addWidget(rampNameLabel)
        layout.addWidget(rampNameInput)
        layout.addWidget(rampTagsLabel)
        layout.addWidget(rampTagsInput)
        layout.addWidget(deleteButton)

        return widget

    def deleteRamp(self, rampId):
        rampWidget = self.findChild(QWidget, rampId)
        if rampWidget:
            self.rampContainerLayout.removeWidget(rampWidget)
            rampWidget.deleteLater()
            self.rampCount -= 1

    def updateColorViewers(self, rampId):
        # Implement color viewer update logic here
        pass

    def generateXML(self):
        xmlString = '<qgis_style version="2">\n<symbols/>\n<colorramps>\n'
        for i in range(1, self.rampCount + 1):
            colorInput = self.findChild(QLineEdit, f"colorInput{i}")
            rampNameInput = self.findChild(QLineEdit, f"rampName{i}")
            rampTagsInput = self.findChild(QLineEdit, f"rampTags{i}")

            hexColors = colorInput.text().split(',')
            rampName = rampNameInput.text()
            rampTags = rampTagsInput.text()

            xmlString += f'<colorramp type="preset" name="{rampName}" tags="{rampTags}">\n'
            xmlString += '<Option type="Map">\n'
            for index, hexColor in enumerate(hexColors):
                rgb = self.hexToRgb(hexColor.strip())
                if not rgb:
                    QMessageBox.warning(self, "Invalid Hex Code", f"Invalid hex code: {hexColor.strip()}")
                    return
                rgba = f"{rgb['r']},{rgb['g']},{rgb['b']},255"
                xmlString += f'<Option type="QString" name="preset_color_{index}" value="{rgba}"/>\n'
                xmlString += f'<Option type="QString" name="preset_color_name_{index}" value="{index}. Color {index}"/>\n'
            xmlString += '<Option type="QString" name="rampType" value="preset"/>\n'
            xmlString += '</Option>\n'
            xmlString += '</colorramp>\n'
        xmlString += '</colorramps>\n<textformats/>\n<labelsettings/>\n<legendpatchshapes/>\n<symbols3d/>\n</qgis_style>'
        self.downloadXML(xmlString, 'MergedColorRamps.xml')

    def hexToRgb(self, hex):
        hex = hex.lstrip('#')
        if len(hex) == 3:
            hex = ''.join([c*2 for c in hex])
        return {'r': int(hex[0:2], 16), 'g': int(hex[2:4], 16), 'b': int(hex[4:6], 16)}

    def downloadXML(self, xmlString, filename):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getSaveFileName(self, "Save XML", filename, "XML Files (*.xml);;All Files (*)", options=options)
        if filePath:
            with open(filePath, 'w') as file:
                file.write(xmlString)