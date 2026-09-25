#!/usr/bin/env python3
"""
make_ascii_svg.py
Converts source-prepped.png into a self-typing animated monochrome ASCII art SVG
(harshit-ascii.svg) sized at 370px wide x 440px high.
"""

import sys
import os
import cv2
import numpy as np

WIDTH = 370
HEIGHT = 440

RAMP = " .:-=+*cs#%@"

COLS = 62
FONT_ASPECT = 0.54  # Character width / height aspect ratio


def generate_ascii(img_path: str):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Could not load image: {img_path}")
        
    h, w = img.shape
    rows = int(COLS * (h / w) * FONT_ASPECT)
    resized = cv2.resize(img, (COLS, rows), interpolation=cv2.INTER_AREA)
    
    ascii_lines = []
    ramp_len = len(RAMP)
    
    for row in resized:
        line_chars = []
        for pixel in row:
            # 255 is pure white (spaces), 0 is darkest
            val = 255 - int(pixel)
            idx = int(val / 256.0 * ramp_len)
            idx = min(idx, ramp_len - 1)
            line_chars.append(RAMP[idx])
        ascii_lines.append("".join(line_chars))
        
    return ascii_lines


def build_svg(lines: list, static: bool = False) -> str:
    num_rows = len(lines)
    y_start = 50
    avail_h = HEIGHT - y_start - 12
    line_h = avail_h / max(num_rows, 1)
    
    font_size = 7.6
    x_start = 14
    text_width = 342
    
    stagger = 0.032
    row_dur = 0.08
    
    svg = []
    svg.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" width="{WIDTH}" height="{HEIGHT}">'
    )
    
    # Styles
    svg.append("""  <style>
    .mono {
      font-family: 'SF Mono', 'Cascadia Code', 'Fira Code', Menlo, Consolas, monospace;
      font-size: 7.6px;
      fill: #c9d1d9;
      letter-spacing: 0.9px;
      white-space: pre;
    }
    .title {
      font-family: 'SF Mono', 'Cascadia Code', Menlo, Consolas, monospace;
      font-size: 11px;
      fill: #8b949e;
    }
  </style>""")
    
    # Definitions (Clip paths for self-typing animation)
    svg.append("  <defs>")
    if not static:
        for i in range(num_rows):
            start_t = 0.1 + (i * stagger)
            y_pos = y_start + (i * line_h)
            svg.append(f'    <clipPath id="wipe-{i}">')
            svg.append(
                f'      <rect x="0" y="{y_pos - font_size + 1:.1f}" width="0" height="{line_h + 1:.1f}">'
            )
            svg.append(
                f'        <animate attributeName="width" from="0" to="{WIDTH}" begin="{start_t:.3f}s" dur="{row_dur:.3f}s" fill="freeze"/>'
            )
            svg.append("      </rect>")
            svg.append("    </clipPath>")
    svg.append("  </defs>")
    
    # Card Background & Terminal Bar
    svg.append(
        f'  <rect width="{WIDTH}" height="{HEIGHT}" rx="8" fill="#0d1117" stroke="#30363d" stroke-width="1"/>'
    )
    svg.append("""  <!-- Window Header -->
  <circle cx="18" cy="18" r="4.5" fill="#ff5f56"/>
  <circle cx="32" cy="18" r="4.5" fill="#ffbd2e"/>
  <circle cx="46" cy="18" r="4.5" fill="#27c93f"/>
  <text class="title" x="185" y="22" text-anchor="middle">harshit@ascii: ~</text>
  <line x1="0" y1="34" x2="370" y2="34" stroke="#21262d" stroke-width="1"/>""")

    # Rows
    svg.append("  <!-- ASCII Portrait Content -->")
    for i, line in enumerate(lines):
        y_pos = y_start + (i * line_h) + (font_size * 0.8)
        
        # Escape XML characters
        safe_line = (
            line.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
        )
        
        clip_attr = "" if static else f' clip-path="url(#wipe-{i})"'
        svg.append(
            f'  <text class="mono" x="{x_start}" y="{y_pos:.1f}"{clip_attr} xml:space="preserve">{safe_line}</text>'
        )
        
        if not static:
            start_t = 0.1 + (i * stagger)
            # Typing cursor riding the wipe edge
            svg.append(
                f'  <rect x="{x_start}" y="{y_pos - font_size + 1:.1f}" width="5" height="{line_h:.1f}" fill="#58a6ff" opacity="0">'
            )
            svg.append(
                f'    <animate attributeName="x" from="{x_start}" to="{x_start + text_width}" begin="{start_t:.3f}s" dur="{row_dur:.3f}s" fill="freeze"/>'
            )
            svg.append(
                f'    <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.05;0.95;1" begin="{start_t:.3f}s" dur="{row_dur:.3f}s" fill="freeze"/>'
            )
            svg.append("  </rect>")
            
    svg.append("</svg>")
    return "\n".join(svg)


def main():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    img_path = os.path.join(base_dir, "source-prepped.png")
    out_path = os.path.join(base_dir, "harshit-ascii.svg")
    
    if len(sys.argv) > 1:
        img_path = sys.argv[1]
    if len(sys.argv) > 2:
        out_path = sys.argv[2]
        
    static_mode = os.environ.get("STATIC", "0") == "1"
    
    if not os.path.exists(img_path):
        print(f"Error: {img_path} not found. Please run prep_photo.py first.")
        return
        
    print(f"Generating ASCII art from {img_path}...")
    lines = generate_ascii(img_path)
    print(f"Generated {len(lines)} lines of ASCII art.")
    
    svg_data = build_svg(lines, static=static_mode)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg_data)
        
    print(f"Successfully wrote {out_path} ({WIDTH}x{HEIGHT})!")


if __name__ == "__main__":
    main()
