#!/usr/bin/env python3
import datetime
import cairosvg
import math
import os
import argparse
from PIL import Image

# --- Main Configuration ---
# Set your birthday here
BIRTH_DATE = datetime.date(2006, 2, 9)

# --- New Feature: Reminders ---
# Add the number of any week you want to highlight (1-based index).
# Example: Week 52 is the last week of the first year. Week 53 is the first of the second year.
REMINDER_WEEKS = [1014,1017,1035] # e.g. End of year 2.5, 5, 10, 20, 30, 40

# --- New Feature: Scale & Position ---
# Adjust the overall size of the calendar
SCALE = 1.5 
# Adjust the position of the calendar on the 16:9 canvas
X_OFFSET = 0 
Y_OFFSET = 0

# --- Color Palette ---
# --- Modified: Added colors for the reminder feature ---
COLOR_PALETTE = {
    "background": "#0A0A0A",
    "text": "#B0B0B0",
    "lines": "#333333",
    "filled_box": "#3D3D3D",      # Darkened from #4F4F4F
    "empty_box": "#1E1E1E",
    "reminder_border": "#FFFFFF", # Keeping original white border
        "reminder_fill": "#4D3800"   # Darkened from #E5C100 (a darker gold)
}

# --- Visual Layout Settings ---
TOTAL_YEARS = 40
WEEKS_IN_YEAR = 52
BOX_SIZE = 11 * SCALE
BOX_SPACING = 3 * SCALE
PADDING = 40 * SCALE
GROUP_SPACING = (11 / 2) * SCALE 
WEEKS_IN_GROUP = 4
WEEK_GROUP_SPACING = (11 / 2) * SCALE 
FONT_FAMILY = "Arial, sans-serif"
CANVAS_16x9_WIDTH = 1920
CANVAS_16x9_HEIGHT = 1080


# --- Modified: Function now accepts reminder weeks ---
def create_life_calendar_svg(birth_date, colors, reminder_weeks, center_on_canvas=None):
    """Generates the complete SVG content for the life calendar."""
    today = datetime.date.today()
    weeks_lived = (today - birth_date).days / 7

    num_year_groups = math.ceil(TOTAL_YEARS / 5)
    num_week_groups = math.ceil(WEEKS_IN_YEAR / WEEKS_IN_GROUP)

    grid_width = (WEEKS_IN_YEAR * (BOX_SIZE + BOX_SPACING) - BOX_SPACING +
                  (num_week_groups - 1) * WEEK_GROUP_SPACING)
    grid_height = (TOTAL_YEARS * (BOX_SIZE + BOX_SPACING) - BOX_SPACING +
                   (num_year_groups - 1) * GROUP_SPACING)
    
    if center_on_canvas:
        svg_width, svg_height = center_on_canvas
        canvas_x_offset = (svg_width - grid_width) / 2 + X_OFFSET
        canvas_y_offset = (svg_height - grid_height) / 2 + Y_OFFSET
    else:
        svg_width = grid_width + 2 * PADDING
        svg_height = grid_height + 2 * PADDING
        canvas_x_offset = PADDING
        canvas_y_offset = PADDING

    svg_elements = [
        f'<svg width="{svg_width}" height="{svg_height}" xmlns="http://www.w3.org/2000/svg">',
        f'<rect width="100%" height="100%" fill="{colors["background"]}" />',
        f"""<style>
            .box {{ stroke: {colors["lines"]}; stroke-width: {0.5 * SCALE}; }}
            .filled {{ fill: {colors["filled_box"]}; }}
            .filled_reminder {{
        fill: {colors["reminder_fill"]}; /* Fills the SVG element with the specified color */
        stroke: {colors["lines"]}; /* Draws a border with the lines color */
        stroke-width: {0.5 * SCALE}; /* Sets the thickness of the border */
}}
            .empty {{ fill: {colors["empty_box"]}; }}
            .label {{ font-family: {FONT_FAMILY}; font-size: {(BOX_SIZE - 1)}px; fill: {colors["text"]}; text-anchor: end; }}
            .header-label {{ font-family: {FONT_FAMILY}; font-size: {BOX_SIZE}px; fill: {colors["text"]}; text-anchor: middle; }}
        </style>""",
        f'<text x="{canvas_x_offset - 15 * SCALE}" y="{canvas_y_offset - 20 * SCALE}" class="label" style="text-anchor: start; font-weight: bold;">YEARS</text>',
        f'<text x="{canvas_x_offset + grid_width / 2}" y="{canvas_y_offset - 20 * SCALE}" class="header-label" style="font-weight: bold;">WEEKS</text>'
    ]

    total_boxes_drawn = 0
    for year in range(TOTAL_YEARS):
        group_offset = (year // 5) * GROUP_SPACING
        y_pos = canvas_y_offset + year * (BOX_SIZE + BOX_SPACING) + group_offset
        if (year + 1) == 1 or (year + 1) % 5 == 0:
            svg_elements.append(f'<text x="{canvas_x_offset - 10 * SCALE}" y="{y_pos + BOX_SIZE - (2 * SCALE)}" class="label">{year + 1}</text>')

        for week in range(WEEKS_IN_YEAR):
            week_group_offset = (week // WEEKS_IN_GROUP) * WEEK_GROUP_SPACING
            x_pos = canvas_x_offset + week * (BOX_SIZE + BOX_SPACING) + week_group_offset
            if year == 0 and (week + 1) % 4 == 0:
                svg_elements.append(f'<text x="{x_pos + BOX_SIZE / 2}" y="{canvas_y_offset - 8 * SCALE}" class="header-label">{week + 1}</text>')
            
            # --- Modified: Logic for handling reminder weeks ---
            current_week_number = total_boxes_drawn + 1
            has_passed = total_boxes_drawn < weeks_lived
            is_reminder = current_week_number in reminder_weeks

            box_class = "filled" if has_passed else "empty"
            extra_style = "" # No extra inline style by default

            if is_reminder:
                box_class = "filled_reminder"
      

            svg_elements.append(f'<rect x="{x_pos}" y="{y_pos}" width="{BOX_SIZE}" height="{BOX_SIZE}" class="box {box_class}" {extra_style}/>')
            total_boxes_drawn += 1

    svg_elements.append('</svg>')
    return "\n".join(svg_elements)


def save_svg_and_png(svg_data, svg_path, png_path):
    """Saves the SVG data and converts it to a PNG file."""
    try:
        with open(svg_path, "w", encoding="utf-8") as f:
            f.write(svg_data)
        print(f"✅ Successfully saved SVG to: {svg_path}")
    except IOError as e:
        print(f"❌ Error saving SVG file: {e}")
        return

    try:
        cairosvg.svg2png(bytestring=svg_data.encode('utf-8'), write_to=png_path)
        print(f"✅ Successfully converted SVG to PNG: {png_path}")
    except Exception as e:
        print(f"❌ Error converting SVG to PNG: {e}")
        print("   Please ensure cairosvg and its dependencies are installed correctly.")

def crop_image_for_display(input_path, output_path, birth_date):
    """Crops the full calendar image to a 16:9 aspect ratio centered on the current year."""
    print(f"✂️ Cropping image for 16:9 display...")
    try:
        today = datetime.date.today()
        weeks_lived = (today - birth_date).days / 7
        current_year = int(weeks_lived // WEEKS_IN_YEAR)

        group_offset = (current_year // 5) * GROUP_SPACING
        y_center = PADDING + current_year * (BOX_SIZE + BOX_SPACING) + group_offset + (BOX_SIZE / 2)

        with Image.open(input_path) as img:
            crop_left = PADDING - (20 * SCALE) 
            crop_right = img.width - (PADDING / 2)
            crop_width = crop_right - crop_right

            crop_height = crop_width * 9 / 16
            crop_top = y_center - (crop_height / 2)
            crop_bottom = y_center + (crop_height / 2)

            crop_top = max(0, crop_top)
            crop_bottom = min(img.height, crop_bottom)

            cropped_img = img.crop((crop_left, crop_top, crop_right, crop_bottom))
            cropped_img.save(output_path)
            print(f"✅ Successfully saved cropped image to: {output_path}")

    except Exception as e:
        print(f"❌ Error cropping image: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a Life Calendar image.")
    parser.add_argument(
        '--ratio16x9',
        action='store_true',
        help="Generate a non-cropped 16:9 version with the calendar centered."
    )
    parser.add_argument(
        '--crop',
        action='store_true',
        help="Generate an additional cropped version with a 16:9 aspect ratio."
    )
    args = parser.parse_args()

    home_dir = os.path.expanduser("~")
    
    # --- Modified: Logic now passes the REMINDER_WEEKS list to the generator function ---
    if args.ratio16x9:
        print("📅 Generating 16:9 Life Calendar...")
        svg_output_path = os.path.join(home_dir, "life_calendar_16x9.svg")
        png_output_path = os.path.join(home_dir, "life_calendar_16x9.png")
        canvas_dims = (CANVAS_16x9_WIDTH, CANVAS_16x9_HEIGHT)
        life_calendar_svg_content = create_life_calendar_svg(BIRTH_DATE, COLOR_PALETTE, REMINDER_WEEKS, center_on_canvas=canvas_dims)
        save_svg_and_png(life_calendar_svg_content, svg_output_path, png_output_path)

    else:
        print("📅 Generating Life Calendar...")
        svg_output_path = os.path.join(home_dir, "life_calendar.svg")
        full_png_path = os.path.join(home_dir, "life_calendar_full.png")
        life_calendar_svg_content = create_life_calendar_svg(BIRTH_DATE, COLOR_PALETTE, REMINDER_WEEKS)
        save_svg_and_png(life_calendar_svg_content, svg_output_path, full_png_path)

        if args.crop:
            cropped_png_path = os.path.join(home_dir, "life_calendar_cropped.png")
            crop_image_for_display(full_png_path, cropped_png_path, BIRTH_DATE)
    
    print("✨ Done.")
