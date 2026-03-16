import csv
import io
import os
import re
from xml.sax.saxutils import escape

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QColor, QIcon, QPainter
from qgis.PyQt.QtWidgets import (
    QAction,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)
from qgis.core import (
    QgsApplication,
    QgsProcessingAlgorithm,
    QgsProcessingContext,
    QgsProcessingFeedback,
    QgsProcessingProvider,
)

from .resources import *


NAMED_COLORS_WITH_RGB = [
    ("AliceBlue", 240, 248, 255), ("AntiqueWhite", 250, 235, 215),
    ("Aqua", 0, 255, 255), ("Aquamarine", 127, 255, 212),
    ("Azure", 240, 255, 255), ("Beige", 245, 245, 220),
    ("Bisque", 255, 228, 196), ("Black", 0, 0, 0),
    ("BlanchedAlmond", 255, 235, 205), ("Blue", 0, 0, 255),
    ("BlueViolet", 138, 43, 226), ("Brown", 165, 42, 42),
    ("BurlyWood", 222, 184, 135), ("CadetBlue", 95, 158, 160),
    ("Chartreuse", 127, 255, 0), ("Chocolate", 210, 105, 30),
    ("Coral", 255, 127, 80), ("CornflowerBlue", 100, 149, 237),
    ("Cornsilk", 255, 248, 220), ("Crimson", 220, 20, 60),
    ("Cyan", 0, 255, 255), ("DarkBlue", 0, 0, 139),
    ("DarkCyan", 0, 139, 139), ("DarkGoldenRod", 184, 134, 11),
    ("DarkGray", 169, 169, 169), ("DarkGreen", 0, 100, 0),
    ("DarkKhaki", 189, 183, 107), ("DarkMagenta", 139, 0, 139),
    ("DarkOliveGreen", 85, 107, 47), ("DarkOrange", 255, 140, 0),
    ("DarkOrchid", 153, 50, 204), ("DarkRed", 139, 0, 0),
    ("DarkSalmon", 233, 150, 122), ("DarkSeaGreen", 143, 188, 143),
    ("DarkSlateBlue", 72, 61, 139), ("DarkSlateGray", 47, 79, 79),
    ("DarkTurquoise", 0, 206, 209), ("DarkViolet", 148, 0, 211),
    ("DeepPink", 255, 20, 147), ("DeepSkyBlue", 0, 191, 255),
    ("DimGray", 105, 105, 105), ("DodgerBlue", 30, 144, 255),
    ("FireBrick", 178, 34, 34), ("FloralWhite", 255, 250, 240),
    ("ForestGreen", 34, 139, 34), ("Fuchsia", 255, 0, 255),
    ("Gainsboro", 220, 220, 220), ("GhostWhite", 248, 248, 255),
    ("Gold", 255, 215, 0), ("GoldenRod", 218, 165, 32),
    ("Gray", 128, 128, 128), ("Green", 0, 128, 0),
    ("GreenYellow", 173, 255, 47), ("HoneyDew", 240, 255, 240),
    ("HotPink", 255, 105, 180), ("IndianRed", 205, 92, 92),
    ("Indigo", 75, 0, 130), ("Ivory", 255, 255, 240),
    ("Khaki", 240, 230, 140), ("Lavender", 230, 230, 250),
    ("LavenderBlush", 255, 240, 245), ("LawnGreen", 124, 252, 0),
    ("LemonChiffon", 255, 250, 205), ("LightBlue", 173, 216, 230),
    ("LightCoral", 240, 128, 128), ("LightCyan", 224, 255, 255),
    ("LightGoldenRodYellow", 250, 250, 210), ("LightGray", 211, 211, 211),
    ("LightGreen", 144, 238, 144), ("LightPink", 255, 182, 193),
    ("LightSalmon", 255, 160, 122), ("LightSeaGreen", 32, 178, 170),
    ("LightSkyBlue", 135, 206, 250), ("LightSlateGray", 119, 136, 153),
    ("LightSteelBlue", 176, 196, 222), ("LightYellow", 255, 255, 224),
    ("Lime", 0, 255, 0), ("LimeGreen", 50, 205, 50),
    ("Linen", 250, 240, 230), ("Magenta", 255, 0, 255),
    ("Maroon", 128, 0, 0), ("MediumAquaMarine", 102, 205, 170),
    ("MediumBlue", 0, 0, 205), ("MediumOrchid", 186, 85, 211),
    ("MediumPurple", 147, 112, 219), ("MediumSeaGreen", 60, 179, 113),
    ("MediumSlateBlue", 123, 104, 238), ("MediumSpringGreen", 0, 250, 154),
    ("MediumTurquoise", 72, 209, 204), ("MediumVioletRed", 199, 21, 133),
    ("MidnightBlue", 25, 25, 112), ("MintCream", 245, 255, 250),
    ("MistyRose", 255, 228, 225), ("Moccasin", 255, 228, 181),
    ("NavajoWhite", 255, 222, 173), ("Navy", 0, 0, 128),
    ("OldLace", 253, 245, 230), ("Olive", 128, 128, 0),
    ("OliveDrab", 107, 142, 35), ("Orange", 255, 165, 0),
    ("OrangeRed", 255, 69, 0), ("Orchid", 218, 112, 214),
    ("PaleGoldenRod", 238, 232, 170), ("PaleGreen", 152, 251, 152),
    ("PaleTurquoise", 175, 238, 238), ("PaleVioletRed", 219, 112, 147),
    ("PapayaWhip", 255, 239, 213), ("PeachPuff", 255, 218, 185),
    ("Peru", 205, 133, 63), ("Pink", 255, 192, 203),
    ("Plum", 221, 160, 221), ("PowderBlue", 176, 224, 230),
    ("Purple", 128, 0, 128), ("Red", 255, 0, 0),
    ("RosyBrown", 188, 143, 143), ("RoyalBlue", 65, 105, 225),
    ("SaddleBrown", 139, 69, 19), ("Salmon", 250, 128, 114),
    ("SandyBrown", 244, 164, 96), ("SeaGreen", 46, 139, 87),
    ("SeaShell", 255, 245, 238), ("Sienna", 160, 82, 45),
    ("Silver", 192, 192, 192), ("SkyBlue", 135, 206, 235),
    ("SlateBlue", 106, 90, 205), ("SlateGray", 112, 128, 144),
    ("Snow", 255, 250, 250), ("SpringGreen", 0, 255, 127),
    ("SteelBlue", 70, 130, 180), ("Tan", 210, 180, 140),
    ("Teal", 0, 128, 128), ("Thistle", 216, 191, 216),
    ("Tomato", 255, 99, 71), ("Turquoise", 64, 224, 208),
    ("Violet", 238, 130, 238), ("Wheat", 245, 222, 179),
    ("White", 255, 255, 255), ("WhiteSmoke", 245, 245, 245),
    ("Yellow", 255, 255, 0), ("YellowGreen", 154, 205, 50),
]

TEMPLATE_CSV = """Palette,Tags,Color1,Color2,Color3,Color4,Color5,Color6,Color7,Color8,Color9,Color10,Color11,Color12
stormfront,dresden,#F3CB66,#cb9060,#D5B09A,#a59587,#544142,#030504
foolmoon,dresden,#532026,#BA141E,#E2E3E7,#61829C,#354C6A,#050505
graveperil,dresden,#C7341E,#EC9C3E,#DDD2B5,#B9AA7F,#936E4C,#40382E
summerknight,dresden,#AC5A42,#865C1E,#BCAF49,#746D28,#3E3C19,#191C0C
deathmasks,dresden,#926159,#87876E,#C7D2D8,#62B7C8,#43535C,#23313C
bloodrites,dresden,#875E3B,#E37F3E,#B3C6AD,#5E6748,#384630,#0D120B
deadbeat,dresden,#818470,#D1BED8,#B9C9D8,#5E7EAC,#876B4D,#131A24
provenguilty,dresden,#AD3D27,#D1E5C6,#BCD384,#4F9D4E,#255025,#0E130F
whitenight,dresden,#847675,#BA857C,#F9F9F9,#CBCCD1,#5D758A,#2E2E30
smallfavor,dresden,#A94120,#E6B12B,#FED89F,#8E6036,#532612,#060405
turncoat,dresden,#651F10,#A86249,#B19D6F,#888D60,#6A412A,#2F1E0F
changes,dresden,#560B06,#D54A1E,#C38636,#F6E090,#503F23,#1B1202
ghoststory,dresden,#33645F,#9D1B1F,#CEA0B5,#F6F5F1,#7B7987,#1D2731
colddays,dresden,#8A8CA4,#D3EEF9,#A0FFFE,#70B7E1,#5074A5,#BFBBA1
skingame,dresden,#3E321A,#643613,#D35127,#EB974E,#FAEAAD,#AFBBDF
sidejobs,dresden,#DBD8C3,#C1714D,#F1B161,#A9823B,#4B4118,#2F2111
briefcases,dresden,#C2697F,#FDDFA4,#B4B9E0,#513965,#201B43,#2C3778
paired,dresden,#9e4058,#C2697F,#d0641e,#e68e54,#f9ab0e,#fbc559,#589e40,#7fc269,#2C3778,#4151b0,#513965,#785596
"""


class ColorSwatch(QFrame):
    def __init__(self, rgba=None, tooltip="", parent=None):
        super().__init__(parent)
        self._rgba = rgba
        self.setFixedSize(26, 26)
        self.setToolTip(tooltip)

    def set_rgba(self, rgba, tooltip):
        self._rgba = rgba
        self.setToolTip(tooltip)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.rect().adjusted(1, 1, -1, -1)

        square = 6
        for row in range(0, rect.height(), square):
            for col in range(0, rect.width(), square):
                dark = ((row // square) + (col // square)) % 2 == 0
                painter.fillRect(
                    rect.x() + col,
                    rect.y() + row,
                    square,
                    square,
                    QColor("#d8d8d8" if dark else "#f2f2f2"),
                )

        if self._rgba:
            painter.fillRect(rect, QColor(*self._rgba))
        else:
            painter.fillRect(rect, QColor("#ffffff"))
            painter.setPen(QColor("#d9534f"))
            painter.drawLine(rect.topLeft(), rect.bottomRight())
            painter.drawLine(rect.topRight(), rect.bottomLeft())

        painter.setPen(QColor("#b8c0c7"))
        painter.drawRect(rect)


class RampCard(QFrame):
    def __init__(self, plugin, index, name="", colors="", tags=""):
        super().__init__()
        self.plugin = plugin
        self.index = index
        self.setObjectName("RampCard")
        self.setFrameShape(QFrame.StyledPanel)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)

        default_colors = colors or "#1f77b4,#ff7f0e80,#2ca02c,#d62728"
        default_name = name or "MyColorRamp{0}".format(index)
        default_tags = tags or "custom,ramp{0}".format(index)

        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        title = QLabel("Ramp {0}".format(index))
        title.setObjectName("RampTitle")
        layout.addWidget(title)

        layout.addWidget(QLabel("Enter Hex Color Codes (comma-separated, #RGB, #RGBA, #RRGGBB, #RRGGBBAA):"))
        self.color_input = QLineEdit(default_colors)
        self.color_input.textChanged.connect(self.update_preview)
        layout.addWidget(self.color_input)

        self.swatch_row = QHBoxLayout()
        self.swatch_row.setSpacing(6)
        self.swatch_row.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(self.swatch_row)

        self.error_label = QLabel("")
        self.error_label.setObjectName("ErrorLabel")
        self.error_label.setWordWrap(True)
        layout.addWidget(self.error_label)

        layout.addWidget(QLabel("Ramp / Palette Name:"))
        self.name_input = QLineEdit(default_name)
        layout.addWidget(self.name_input)

        layout.addWidget(QLabel("QGIS Ramp Tags (comma-separated):"))
        self.tags_input = QLineEdit(default_tags)
        layout.addWidget(self.tags_input)

        button_row = QHBoxLayout()
        button_row.setSpacing(8)
        self.gpl_button = QPushButton("Generate GPL")
        self.gpl_button.setObjectName("GplButton")
        self.gpl_button.clicked.connect(lambda: self.plugin.generate_gpl_for_card(self))
        button_row.addWidget(self.gpl_button)

        self.delete_button = QPushButton("Delete Ramp")
        self.delete_button.setObjectName("DeleteButton")
        self.delete_button.clicked.connect(lambda: self.plugin.delete_ramp(self))
        button_row.addWidget(self.delete_button)
        button_row.addStretch(1)
        layout.addLayout(button_row)

        self.update_preview()

    def set_index(self, index):
        self.index = index
        title = self.findChild(QLabel, "RampTitle")
        if title:
            title.setText("Ramp {0}".format(index))

    def clear_swatch_row(self):
        while self.swatch_row.count():
            item = self.swatch_row.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def update_preview(self):
        self.clear_swatch_row()
        invalid = []
        tokens = [token.strip() for token in self.color_input.text().split(",") if token.strip()]

        if not tokens:
            helper = QLabel("Add one or more colors to preview this ramp.")
            helper.setObjectName("MutedLabel")
            self.swatch_row.addWidget(helper)
            self.error_label.setText("")
            return

        for token in tokens:
            rgba = self.plugin.hex_to_rgba(token)
            swatch = ColorSwatch(rgba=rgba, tooltip=token)
            self.swatch_row.addWidget(swatch)
            if rgba is None:
                invalid.append(token)

        self.swatch_row.addStretch(1)
        self.error_label.setText(
            "Invalid hex code(s): {0}".format(", ".join(invalid)) if invalid else ""
        )

    def get_ramp_data(self):
        raw_colors = [token.strip() for token in self.color_input.text().split(",") if token.strip()]
        valid_colors = []
        invalid_colors = []

        for token in raw_colors:
            rgba = self.plugin.hex_to_rgba(token)
            if rgba is None:
                invalid_colors.append(token)
            else:
                valid_colors.append({"hex": token, "rgba": rgba})

        if invalid_colors:
            self.error_label.setText(
                "Invalid hex code(s): {0}. Please fix them.".format(", ".join(invalid_colors))
            )
            return None

        if not valid_colors:
            self.error_label.setText("No valid colors entered for this ramp.")
            return None

        self.error_label.setText("")
        return {
            "valid_colors": valid_colors,
            "ramp_name": self.name_input.text().strip() or "UnnamedRamp{0}".format(self.index),
            "ramp_tags": self.tags_input.text().strip(),
        }


class OpenPaletteGeneratorAlgorithm(QgsProcessingAlgorithm):
    def __init__(self, plugin):
        super().__init__()
        self.plugin = plugin

    def name(self):
        return "open_palette_generator"

    def displayName(self):
        return "Open Color Ramp Generator"

    def group(self):
        return "Palette Tools"

    def groupId(self):
        return "palette_tools"

    def shortHelpString(self):
        return "Opens the QGIS Color Ramp Generator window."

    def icon(self):
        return self.plugin.app_icon()

    def createInstance(self):
        return OpenPaletteGeneratorAlgorithm(self.plugin)

    def initAlgorithm(self, config=None):
        return None

    def flags(self):
        return super().flags() | QgsProcessingAlgorithm.FlagNoThreading

    def processAlgorithm(self, parameters, context: QgsProcessingContext, feedback: QgsProcessingFeedback):
        self.plugin.run()
        return {}


class ColorRampGeneratorProvider(QgsProcessingProvider):
    def __init__(self, plugin):
        super().__init__()
        self.plugin = plugin

    def loadAlgorithms(self):
        self.addAlgorithm(OpenPaletteGeneratorAlgorithm(self.plugin))

    def id(self):
        return "qgis_color_ramp_generator"

    def name(self):
        return "QGIS Color Ramp Generator"

    def longName(self):
        return self.name()

    def icon(self):
        return self.plugin.app_icon()


class QGISColorRampGenerator(QMainWindow):
    def __init__(self, iface):
        super().__init__()
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.icon_path = os.path.join(self.plugin_dir, "icon.png")
        self.actions = []
        self.menu = self.tr("&QGIS Color Ramp Generator")
        self.toolbar = self.iface.addToolBar("QGISColorRampGenerator")
        self.toolbar.setObjectName("QGISColorRampGenerator")
        self.provider = None
        self.ramp_counter = 0
        self.ramp_cards = []
        self._build_ui()

    def tr(self, message):
        return message

    def initGui(self):
        self.add_action(
            self.icon_path,
            text=self.tr("QGIS Color Ramp Generator"),
            callback=self.run,
            parent=self.iface.mainWindow(),
        )
        if self.provider is None:
            self.provider = ColorRampGeneratorProvider(self)
            QgsApplication.processingRegistry().addProvider(self.provider)

    def unload(self):
        for action in self.actions:
            self.iface.removePluginMenu(self.menu, action)
            self.iface.removeToolBarIcon(action)
        if self.provider is not None:
            QgsApplication.processingRegistry().removeProvider(self.provider)
            self.provider = None
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
        parent=None,
    ):
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

    def _build_ui(self):
        self.setWindowTitle("QGIS XML & GPL Color Palette Generator")
        self.resize(980, 760)
        self.setWindowIcon(self.app_icon())

        central = QWidget()
        root = QVBoxLayout(central)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(14)

        header = QLabel("QGIS XML & GPL Color Palette Generator")
        header.setObjectName("WindowTitle")
        root.addWidget(header)

        subtitle = QLabel(
            "Create multiple QGIS preset ramps, preview RGBA colors, import CSV palettes, and export either merged XML or per-ramp GPL files."
        )
        subtitle.setWordWrap(True)
        subtitle.setObjectName("Subtitle")
        root.addWidget(subtitle)

        file_section = self._build_section()
        file_layout = file_section.layout()
        file_layout.addWidget(QLabel("General File Name Prefix (Optional):"))
        self.file_prefix_input = QLineEdit()
        self.file_prefix_input.setPlaceholderText("e.g., MyProject_Palettes")
        file_layout.addWidget(self.file_prefix_input)
        root.addWidget(file_section)

        controls = self._build_section()
        controls_layout = controls.layout()
        controls_label = QLabel("Import / Export")
        controls_label.setObjectName("SectionLabel")
        controls_layout.addWidget(controls_label)

        button_row = QHBoxLayout()
        button_row.setSpacing(10)
        self.import_button = QPushButton("Import CSV")
        self.import_button.setObjectName("ImportButton")
        self.import_button.clicked.connect(self.import_csv)
        button_row.addWidget(self.import_button)

        self.template_button = QPushButton("Download CSV Template")
        self.template_button.setObjectName("TemplateButton")
        self.template_button.clicked.connect(self.download_template_csv)
        button_row.addWidget(self.template_button)

        self.add_button = QPushButton("Add New Ramp Manually")
        self.add_button.setObjectName("AddButton")
        self.add_button.clicked.connect(self.add_ramp)
        button_row.addWidget(self.add_button)

        self.generate_xml_button = QPushButton("Generate All to QGIS XML")
        self.generate_xml_button.setObjectName("GenerateXmlButton")
        self.generate_xml_button.clicked.connect(self.generate_xml)
        button_row.addWidget(self.generate_xml_button)
        button_row.addStretch(1)
        controls_layout.addLayout(button_row)
        root.addWidget(controls)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)

        self.scroll_content = QWidget()
        self.ramp_layout = QVBoxLayout(self.scroll_content)
        self.ramp_layout.setContentsMargins(0, 0, 0, 0)
        self.ramp_layout.setSpacing(12)
        self.ramp_layout.addStretch(1)
        self.scroll_area.setWidget(self.scroll_content)
        root.addWidget(self.scroll_area, 1)

        self.empty_state = QLabel(
            'Click "Add New Ramp Manually" or "Import CSV" to begin creating your color palettes.'
        )
        self.empty_state.setAlignment(Qt.AlignCenter)
        self.empty_state.setWordWrap(True)
        self.empty_state.setObjectName("EmptyState")
        self.ramp_layout.insertWidget(0, self.empty_state)

        self.setCentralWidget(central)
        self.setStyleSheet(self._stylesheet())

    def app_icon(self):
        return QIcon(self.icon_path)

    def _build_section(self):
        frame = QFrame()
        frame.setObjectName("SectionCard")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)
        return frame

    def _stylesheet(self):
        return """
        QMainWindow {
            background: #eef2f5;
        }
        QLabel#WindowTitle {
            font-size: 24px;
            font-weight: 700;
            color: #213547;
        }
        QLabel#Subtitle {
            color: #51606d;
            font-size: 13px;
        }
        QFrame#SectionCard, QFrame#RampCard {
            background: #ffffff;
            border: 1px solid #d8e0e6;
            border-radius: 10px;
        }
        QLabel#SectionLabel, QLabel#RampTitle {
            font-weight: 700;
            color: #243746;
        }
        QLabel#ErrorLabel {
            color: #c0392b;
            min-height: 18px;
        }
        QLabel#MutedLabel {
            color: #75828f;
            font-style: italic;
        }
        QLabel#EmptyState {
            color: #768492;
            font-style: italic;
            padding: 36px;
            border: 2px dashed #d4dde5;
            border-radius: 10px;
            background: #f9fbfc;
        }
        QLineEdit {
            padding: 9px 10px;
            border: 1px solid #cfd8df;
            border-radius: 6px;
            background: #ffffff;
        }
        QLineEdit:focus {
            border: 1px solid #4a90a4;
        }
        QPushButton {
            color: white;
            border: none;
            border-radius: 6px;
            padding: 9px 14px;
            font-weight: 600;
        }
        QPushButton#AddButton { background: #5d6d7e; }
        QPushButton#AddButton:hover { background: #4a5766; }
        QPushButton#GenerateXmlButton { background: #4caf50; }
        QPushButton#GenerateXmlButton:hover { background: #419744; }
        QPushButton#GplButton { background: #3498db; }
        QPushButton#GplButton:hover { background: #2b82ba; }
        QPushButton#DeleteButton { background: #e74c3c; }
        QPushButton#DeleteButton:hover { background: #cc3d2f; }
        QPushButton#ImportButton { background: #9b59b6; }
        QPushButton#ImportButton:hover { background: #8648a1; }
        QPushButton#TemplateButton { background: #1abc9c; }
        QPushButton#TemplateButton:hover { background: #149b81; }
        """

    def run(self):
        self.show()
        self.raise_()
        self.activateWindow()

    def add_ramp(self, name="", colors="", tags=""):
        if len(self.ramp_cards) >= 100:
            QMessageBox.warning(self, "Limit Reached", "Maximum 100 ramps allowed.")
            return

        self.ramp_counter += 1
        card = RampCard(self, self.ramp_counter, name=name, colors=colors, tags=tags)
        self.ramp_cards.append(card)
        self.ramp_layout.insertWidget(self.ramp_layout.count() - 1, card)
        self.empty_state.setVisible(False)

    def delete_ramp(self, card):
        if card not in self.ramp_cards:
            return
        self.ramp_cards.remove(card)
        self.ramp_layout.removeWidget(card)
        card.deleteLater()
        self._refresh_ramp_indices()
        self.empty_state.setVisible(not self.ramp_cards)

    def _refresh_ramp_indices(self):
        for index, card in enumerate(self.ramp_cards, start=1):
            card.set_index(index)

    def import_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Import CSV Palette File",
            "",
            "CSV Files (*.csv);;All Files (*)",
        )
        if not file_path:
            return

        try:
            with open(file_path, "r", encoding="utf-8-sig", newline="") as handle:
                rows = list(csv.reader(handle))
        except OSError as exc:
            QMessageBox.critical(self, "Import Failed", "Could not read the CSV file:\n{0}".format(exc))
            return

        if len(rows) < 2:
            QMessageBox.warning(self, "Import Failed", "CSV file is empty or contains only a header.")
            return

        header = [column.strip().lower() for column in rows[0]]
        if len(header) < 2:
            QMessageBox.warning(
                self,
                "Import Failed",
                "CSV must contain at least a name column and one color column.",
            )
            return

        name_index = 0
        for idx, value in enumerate(header):
            if value in ("palette", "name"):
                name_index = idx
                break

        tags_index = header.index("tags") if "tags" in header else -1
        imported = 0

        for row in rows[1:]:
            if not any(cell.strip() for cell in row):
                continue
            name = row[name_index].strip() if name_index < len(row) else ""
            tags = row[tags_index].strip() if tags_index != -1 and tags_index < len(row) else ""
            colors = []
            for idx, value in enumerate(row):
                if idx in (name_index, tags_index) or not value.strip():
                    continue
                colors.append(value.strip())

            if name and colors:
                self.add_ramp(name=name, colors=",".join(colors), tags=tags or name.lower())
                imported += 1

        if imported == 0:
            QMessageBox.warning(
                self,
                "Import Finished",
                "No valid palette rows were found in the CSV file.",
            )
        else:
            QMessageBox.information(
                self,
                "Import Complete",
                "Imported {0} palette(s).".format(imported),
            )

    def download_template_csv(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save CSV Template",
            "qgis_palette_template.csv",
            "CSV Files (*.csv);;All Files (*)",
        )
        if not file_path:
            return

        try:
            with open(file_path, "w", encoding="utf-8", newline="") as handle:
                handle.write(TEMPLATE_CSV)
        except OSError as exc:
            QMessageBox.critical(self, "Save Failed", "Could not save the template:\n{0}".format(exc))

    def generate_gpl_for_card(self, card):
        data = card.get_ramp_data()
        if not data:
            QMessageBox.warning(
                self,
                "Cannot Generate GPL",
                "Please fix the errors in this ramp before exporting.",
            )
            return

        content = self._build_gpl(data)
        file_name = self._build_gpl_filename(data["ramp_name"])
        self._save_text_file(
            title="Save GPL Palette",
            suggested_name=file_name,
            filter_text="GPL Palette (*.gpl);;All Files (*)",
            content=content,
        )

    def generate_xml(self):
        if not self.ramp_cards:
            QMessageBox.warning(
                self,
                "Nothing To Export",
                "Please add at least one color ramp before generating XML.",
            )
            return

        ramp_entries = []
        for card in self.ramp_cards:
            data = card.get_ramp_data()
            if not data:
                QMessageBox.warning(
                    self,
                    "Cannot Generate XML",
                    "One or more ramps have invalid colors. Please fix them and try again.",
                )
                return
            ramp_entries.append(data)

        xml_content = self._build_xml(ramp_entries)
        prefix = self.file_prefix_input.text().strip() or "QGIS_ColorRamps"
        self._save_text_file(
            title="Save QGIS XML",
            suggested_name="{0}.xml".format(prefix),
            filter_text="XML Files (*.xml);;All Files (*)",
            content=xml_content,
        )

    def _save_text_file(self, title, suggested_name, filter_text, content):
        file_path, _ = QFileDialog.getSaveFileName(self, title, suggested_name, filter_text)
        if not file_path:
            return
        try:
            with open(file_path, "w", encoding="utf-8", newline="") as handle:
                handle.write(content)
        except OSError as exc:
            QMessageBox.critical(self, "Save Failed", "Could not save the file:\n{0}".format(exc))

    def _build_xml(self, ramp_entries):
        lines = [
            "<!DOCTYPE qgis_style>",
            '<qgis_style version="2">',
            "<symbols/>",
            "<colorramps>",
        ]
        for entry in ramp_entries:
            ramp_name = escape(entry["ramp_name"], {'"': "&quot;"})
            ramp_tags = escape(entry["ramp_tags"], {'"': "&quot;"})
            lines.append(
                '<colorramp type="preset" name="{0}" tags="{1}">'.format(ramp_name, ramp_tags)
            )
            lines.append("  <Option type=\"Map\">")
            for index, color_data in enumerate(entry["valid_colors"]):
                r, g, b, a = color_data["rgba"]
                lines.append(
                    '    <Option type="QString" name="preset_color_{0}" value="{1},{2},{3},{4}"/>'.format(
                        index, r, g, b, a
                    )
                )
            lines.append('    <Option type="QString" name="rampType" value="preset"/>')
            lines.append("  </Option>")
            lines.append("</colorramp>")
        lines.extend(
            [
                "</colorramps>",
                "<textformats/>",
                "<labelsettings/>",
                "<legendpatchshapes/>",
                "<symbols3d/>",
                "</qgis_style>",
            ]
        )
        return "\n".join(lines)

    def _build_gpl(self, entry):
        output = io.StringIO()
        output.write("GIMP Palette\n")
        output.write("Name: {0}\n".format(entry["ramp_name"]))
        output.write("Columns: 8\n")
        output.write("#\n")
        for color_data in entry["valid_colors"]:
            r, g, b, _a = color_data["rgba"]
            color_name = self.get_closest_color_name(r, g, b)
            output.write(
                "{0:>3} {1:>3} {2:>3}\t{3}\n".format(r, g, b, color_name)
            )
        return output.getvalue()

    def _build_gpl_filename(self, ramp_name):
        safe_ramp = self._slugify(ramp_name) or "palette"
        prefix = self._slugify(self.file_prefix_input.text().strip())
        return "{0}_{1}.gpl".format(prefix, safe_ramp) if prefix else "{0}.gpl".format(safe_ramp)

    def _slugify(self, value):
        value = re.sub(r"[^A-Za-z0-9]+", "_", value or "").strip("_")
        return value.lower()

    def is_valid_hex(self, value):
        return bool(re.match(r"^#?([0-9a-fA-F]{3}|[0-9a-fA-F]{4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$", value or ""))

    def hex_to_rgba(self, value):
        if not self.is_valid_hex(value):
            return None

        color = value.lstrip("#")
        if len(color) in (3, 4):
            color = "".join(char * 2 for char in color)

        if len(color) == 6:
            return (
                int(color[0:2], 16),
                int(color[2:4], 16),
                int(color[4:6], 16),
                255,
            )

        return (
            int(color[0:2], 16),
            int(color[2:4], 16),
            int(color[4:6], 16),
            int(color[6:8], 16),
        )

    def get_closest_color_name(self, r, g, b):
        closest_name = "Unknown Color"
        min_distance = None
        for name, red, green, blue in NAMED_COLORS_WITH_RGB:
            distance = (r - red) ** 2 + (g - green) ** 2 + (b - blue) ** 2
            if min_distance is None or distance < min_distance:
                min_distance = distance
                closest_name = name
        return closest_name
