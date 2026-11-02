import argparse
import json
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def number(value, name, minimum=0, integer=False, strict=False):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{name}: expected a finite number.")
    if value < minimum or (strict and value == minimum):
        raise ValueError(f"{name}: expected a value {'>' if strict else '>='} {minimum}.")
    if integer and not isinstance(value, int):
        raise ValueError(f"{name}: expected an integer.")
    return value


def boolean(value, name):
    if not isinstance(value, bool):
        raise ValueError(f"{name}: expected true or false.")
    return value


def color(value, name):
    if not isinstance(value, list) or len(value) != 4:
        raise ValueError(f"{name}: expected a list of 4 RGBA integers.")
    for component in value:
        number(component, name, integer=True)
        if component > 255:
            raise ValueError(f"{name}: components must be between 0 and 255.")
    return tuple(value)


def create_overlay(config, folder):
    settings = config["functional_settings"]
    appearance = config["appearance_settings"]
    name = settings["overlay_name"]
    if not isinstance(name, str) or not name.strip() or name in (".", "..") or any(c in name for c in '<>:"/\\|?*'):
        raise ValueError("overlay_name: expected a nonempty file name without reserved characters.")
    scale = number(settings["pixels_per_inch"], "pixels_per_inch", strict=True)
    length = number(settings["line_length_inches"], "line_length_inches", strict=True)
    levels = settings["heights_from_back_inches"]
    if not isinstance(levels, dict) or not levels:
        raise ValueError("heights_from_back_inches: expected a nonempty object.")
    for height in levels.values():
        number(height, "height")
    for key in ("left_margin_px", "right_margin_px", "top_margin_px", "bottom_margin_px"):
        number(appearance[key], key, integer=True)
    for key in ("back_label_dx_px", "back_label_dy_px", "label_dx_px", "label_dy_px"):
        number(appearance[key], key, minimum=-math.inf, integer=True)
    width = number(appearance["line_width_px"], "line_width_px", minimum=1, integer=True)
    show_back = boolean(appearance["show_back_reference"], "show_back_reference")
    show_values = boolean(appearance["show_values"], "show_values")
    for key in ("back_label", "label_format"):
        if not isinstance(appearance[key], str):
            raise ValueError(f"{key}: expected text.")
    line_color = color(appearance["line_color_rgba"], "line_color_rgba")
    background = color(appearance["background_rgba"], "background_rgba")
    font_size = number(appearance["font"]["size_px"], "font.size_px", minimum=1, integer=True)
    font_file = appearance["font"]["file"]
    font = ImageFont.load_default(size=font_size) if font_file is None else ImageFont.truetype(str(folder / font_file), font_size)
    x_start = appearance["left_margin_px"]
    x_end = x_start + round(length * scale)
    y_back = appearance["top_margin_px"] + round(max(levels.values()) * scale)
    image_width = x_end + appearance["right_margin_px"] + 1
    image_height = y_back + appearance["bottom_margin_px"] + 1
    image = Image.new("RGBA", (image_width, image_height), background)
    draw = ImageDraw.Draw(image)
    if show_back:
        draw.line((x_start, y_back, x_end, y_back), fill=line_color, width=width)
        draw.text((x_start + appearance["back_label_dx_px"], y_back + appearance["back_label_dy_px"]), appearance["back_label"], fill=line_color, font=font)
    for label, height in levels.items():
        y = y_back - round(height * scale)
        draw.line((x_start, y, x_end, y), fill=line_color, width=width)
        text = appearance["label_format"].format(name=label, height=height) if show_values else label
        draw.text((x_end + appearance["label_dx_px"], y + appearance["label_dy_px"]), text, fill=line_color, font=font)
    destination = folder / (name if name.lower().endswith(".png") else name + ".png")
    image.save(destination, format="PNG")
    return destination, image.size


def main():
    parser = argparse.ArgumentParser(description="Generate a horizontal-level overlay using a JSON configuration.")
    parser.add_argument("configuration", nargs="?", type=Path, default=Path(__file__).resolve().with_name("kwikset.json"))
    args = parser.parse_args()
    try:
        path = args.configuration.resolve()
        with path.open(encoding="utf-8") as file:
            config = json.load(file)
        destination, size = create_overlay(config, path.parent)
    except (OSError, ValueError, KeyError, TypeError, IndexError, AttributeError) as error:
        parser.exit(1, f"Error: {error}\n")
    print(f"Overlay created: {destination} ({size[0]} x {size[1]} px)")


if __name__ == "__main__":
    main()
