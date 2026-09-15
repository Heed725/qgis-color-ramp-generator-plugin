# QGIS Color Ramp Generator

[![Security and quality checks](https://github.com/Heed725/qgis-color-ramp-generator-plugin/actions/workflows/security-scan.yml/badge.svg)](https://github.com/Heed725/qgis-color-ramp-generator-plugin/actions/workflows/security-scan.yml)
[![Release](https://img.shields.io/github/v/release/Heed725/qgis-color-ramp-generator-plugin)](https://github.com/Heed725/qgis-color-ramp-generator-plugin/releases/latest)
[![QGIS](https://img.shields.io/badge/QGIS-3.x%20%7C%204.x-589632?logo=qgis&logoColor=white)](https://qgis.org/)
[![Qt](https://img.shields.io/badge/Qt-5%20%7C%206-41CD52?logo=qt&logoColor=white)](https://www.qt.io/)
[![Downloads](https://img.shields.io/github/downloads/Heed725/qgis-color-ramp-generator-plugin/total)](https://github.com/Heed725/qgis-color-ramp-generator-plugin/releases)
[![License](https://img.shields.io/github/license/Heed725/qgis-color-ramp-generator-plugin)](LICENSE)

QGIS Color Ramp Generator is a compact palette workstation for creating,
previewing and exporting reusable QGIS color ramps. Build as many as 100 ramps
in one session, import palettes from CSV, preview RGB or RGBA colors, and export
either a combined QGIS style XML file or individual GIMP GPL palettes.

Version 0.3 supports QGIS 3.x and QGIS 4.x through compatible Qt 5 and Qt 6
imports and enum handling. It has no third-party Python dependencies.

## Features

- Create, edit and delete multiple color ramps in one window.
- Preview `#RGB`, `#RGBA`, `#RRGGBB` and `#RRGGBBAA` colors instantly.
- Import multiple named palettes and tags from one CSV file.
- Download a ready-to-edit CSV template from the plugin.
- Export all ramps into one QGIS preset-ramp XML style file.
- Export an individual ramp as a GPL palette.
- Open the same editor from the toolbar, Plugins menu or Processing Toolbox.
- Validate malformed colors before export and preserve alpha in QGIS XML.

## Installation

### Install the release ZIP

1. Download [`color_ramp-0.3.zip`](https://github.com/Heed725/qgis-color-ramp-generator-plugin/releases/download/0.3/color_ramp-0.3.zip).
2. In QGIS, open **Plugins → Manage and Install Plugins**.
3. Select **Install from ZIP**, choose the downloaded file and install it.
4. Enable **QGIS Color Ramp Generator** if QGIS does not enable it
   automatically.

Do not extract or rename the ZIP before installation. It already contains the
required, PEP 8-compliant `color_ramp/` top-level directory.

### Install from source

Copy the repository files into a directory named `color_ramp` inside the active
QGIS profile's `python/plugins` directory, then restart QGIS or reload plugins.

## Usage

1. Press the palette icon on the QGIS toolbar, choose the plugin from the
   **Plugins** menu, or run **Open Color Ramp Generator** from the Processing
   Toolbox. All three entry points open the same editor.
2. Select **Add New Ramp Manually** or **Import CSV**.
3. Enter a ramp name, optional tags and comma-separated hexadecimal colors.
4. Use **Generate GPL** on one ramp or **Generate All to QGIS XML**.
5. Import the XML through the QGIS Style Manager when you want to reuse the
   ramps in other projects.

## CSV format

The first row must contain `Palette` or `Name`, an optional `Tags` column, and
one or more color columns. Other non-empty columns are treated as colors.

```csv
Palette,Tags,Color1,Color2,Color3
stormfront,dresden,#F3CB66,#CB9060,#D5B09A
ocean,blue;cool,#D9F0FF,#72B7D2,#155E75
```

Use the plugin's **Download CSV Template** button for a larger working example.

## Output formats

- **QGIS XML:** one style document containing every valid ramp as a `preset`
  color ramp. RGBA alpha values are preserved.
- **GPL:** a single palette compatible with GIMP and other applications that
  support the GPL palette format. GPL does not store alpha values.

## Compatibility and package checks

- QGIS minimum version: 3.0
- QGIS maximum version declared: 4.99
- Qt compatibility: Qt 5 and Qt 6
- Automated checks: Python compilation, Bandit, detect-secrets and Flake8
- Release package root: `color_ramp/`

The repository intentionally excludes generated PyQt5-only UI modules,
compiled resources, cached files and old ZIP archives. The release workflow
packages only the files needed by QGIS.

## Support

Report bugs or request improvements in
[GitHub Issues](https://github.com/Heed725/qgis-color-ramp-generator-plugin/issues).
Please include your QGIS, Qt, Python and operating-system versions, together
with the steps needed to reproduce the problem.

## Author and license

Created and maintained by **Hemed Lungo** (`hemedlungo@gmail.com`). See
[`LICENSE`](LICENSE) for the license terms.
