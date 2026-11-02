# Overlay Generator

Generate a transparent PNG overlay with horizontal reference lines from a JSON configuration. The included configuration uses Kwikset cut heights.

## Requirements

- Python with Pillow installed.

Install Pillow if needed:

```bash
python -m pip install --upgrade Pillow
```

## Quick start

1. Place `generate_overlay.py` and `kwikset.json` in the same folder.
2. Open `kwikset.json` in a text editor.
3. Set `overlay_name` to the name you want for your output PNG.
4. Enter your cut heights in `heights_from_back_inches`. Each label identifies a level, and its value is the height measured from the back reference, in inches.
5. Save the JSON and run:

```bash
python generate_overlay.py
```

The PNG is saved next to the JSON file. Once you have entered the name and cut heights and checked the scale, everything should be ready to go!

## Main settings

The JSON contains two groups:

- `functional_settings`: output name, scale, line length, and cut heights.
- `appearance_settings`: colors, transparency, margins, line width, font, and labels.

Each group includes a `_help` section explaining the expected data types and units. These help entries do not affect the drawing.

Example of the main settings (inside `functional_settings`):

```json
"overlay_name": "My_overlay",
"pixels_per_inch": 1000,
"line_length_inches": 1.3,
"heights_from_back_inches": {
  "1": 0.329,
  "2": 0.306,
  "3": 0.283
}
```

This example produces `My_overlay.png` with three horizontal levels. Replace the labels and values with those for your reference.

## Input notes

- Heights and line length are in inches.
- Use a decimal point: `0.329`, not a decimal comma.
- Put labels and names in double quotes, but leave numeric values unquoted.
- Keep the JSON syntax valid: no comments or trailing commas.
- `pixels_per_inch` sets the drawing scale. When using the PNG over another image, match their scales; resizing changes the displayed scale.
- Lines do not depend on shoulder positions. Adjust `line_length_inches` to make them long enough.
- Increase the margins if labels are clipped.
- Use both English-version files together: the script expects the English JSON keys.


## Usage notice

For educational use only.
