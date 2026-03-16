# QGIS Color Ramp Generator Plugin

This plugin has been revamped into a fuller palette workstation for QGIS. It now lets you build multiple ramps in one session, preview transparent colors, import palettes from CSV, export merged QGIS XML, and save individual ramps as GPL palettes.

## What's New

- Multi-ramp editor with up to 100 ramp cards
- Live color swatches for `#RGB`, `#RGBA`, `#RRGGBB`, and `#RRGGBBAA`
- CSV import with `Palette`/`Name`, `Tags`, and color columns
- Downloadable CSV template
- Export all ramps into one QGIS preset-ramp XML file
- Export any single ramp as a GPL palette
- Better validation and clearer save dialogs

## Expected CSV Format

The importer reads a header row and looks for:

- `Palette` or `Name` for the ramp name
- `Tags` for QGIS ramp tags
- Any remaining non-empty columns as colors

Example:

```csv
Palette,Tags,Color1,Color2,Color3
stormfront,dresden,#F3CB66,#cb9060,#D5B09A
```

## Usage

1. Open the plugin from the QGIS Plugins menu or toolbar.
2. Add ramps manually or import a CSV file.
3. Enter colors as comma-separated hex values.
4. Export one ramp as GPL or export all ramps to a merged QGIS XML file.

## Notes

- XML output uses QGIS `preset` color ramps.
- GPL export uses the closest named RGB color for each swatch label.
- Alpha values are previewed in the UI and preserved in XML export.
