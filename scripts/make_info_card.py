#!/usr/bin/env python3
"""
make_info_card.py
Renders an animated neofetch-style developer card SVG (info-card.svg)
sized at 490px wide x 440px high, perfectly aligning with harshit-ascii.svg.
"""

import sys
import os

WIDTH = 490
HEIGHT = 440


def build_card(static: bool = False) -> str:
    lines = [
        {"type": "header", "user": "harshit", "host": "github"},
        {"type": "divider"},
        {"type": "field", "key": "OS", "val": "Arch Linux (x86_64)"},
        {"type": "field", "key": "Role", "val": "Full-Stack Dev & eCommerce Operator"},
        {"type": "field", "key": "Focus", "val": "High-Performance Shopify Themes & Next.js"},
        {"type": "field", "key": "Stack", "val": "TypeScript, React, Next.js, Liquid, Python"},
        {"type": "field", "key": "Projects", "val": "Old Loom, CareConnect, MotionPortfolio"},
        {"type": "field", "key": "Uptime", "val": "Building digital products & scaling brands"},
        {"type": "field", "key": "Shell", "val": "zsh 5.9 / tmux"},
        {"type": "field", "key": "Editor", "val": "Neovim / Cursor"},
        {"type": "field", "key": "Location", "val": "India 🇮🇳"},
        {"type": "field", "key": "Contact", "val": "hraj491@gmail.com"},
        {"type": "field", "key": "GitHub", "val": "github.com/hrajsoni"},
        {"type": "palette"},
    ]

    svg = []
    svg.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" width="{WIDTH}" height="{HEIGHT}">'
    )

    # Styles
    svg.append("""  <style>
    @keyframes lineFade {
      0% { opacity: 0; transform: translateX(-8px); }
      100% { opacity: 1; transform: translateX(0); }
    }
    .line-anim {
      animation: lineFade 0.35s cubic-bezier(0.16, 1, 0.3, 1) forwards;
      opacity: 0;
    }
    .static {
      opacity: 1 !important;
      animation: none !important;
    }
    .mono {
      font-family: 'SF Mono', 'Cascadia Code', 'Fira Code', Menlo, Consolas, monospace;
    }
    .title {
      font-size: 11px;
      fill: #8b949e;
    }
    .user { fill: #39d353; font-weight: 700; font-size: 13.5px; }
    .at { fill: #8b949e; font-size: 13.5px; }
    .host { fill: #58a6ff; font-weight: 700; font-size: 13.5px; }
    .divider { fill: #30363d; font-size: 11px; }
    .key { fill: #58a6ff; font-weight: 600; font-size: 11.5px; }
    .colon { fill: #8b949e; font-size: 11.5px; }
    .val { fill: #c9d1d9; font-size: 11.5px; }
    .val-accent { fill: #e6edf3; font-weight: 500; font-size: 11.5px; }
  </style>""")

    # Background Card
    svg.append(
        f'  <rect width="{WIDTH}" height="{HEIGHT}" rx="8" fill="#0d1117" stroke="#30363d" stroke-width="1"/>'
    )

    # Window Header
    svg.append("""  <!-- Window Header -->
  <circle cx="20" cy="18" r="4.5" fill="#ff5f56"/>
  <circle cx="34" cy="18" r="4.5" fill="#ffbd2e"/>
  <circle cx="48" cy="18" r="4.5" fill="#27c93f"/>
  <text class="mono title" x="245" y="22" text-anchor="middle">harshit@neofetch: ~</text>
  <line x1="0" y1="34" x2="490" y2="34" stroke="#21262d" stroke-width="1"/>""")

    svg.append("  <!-- Neofetch Content -->")
    y = 60
    line_spacing = 23
    delay = 0.05
    stagger = 0.06

    normal_palette = [
        "#161b22", "#f85149", "#3fb950", "#d29922",
        "#58a6ff", "#bc8cff", "#39c5cf", "#b1bac4"
    ]
    bright_palette = [
        "#484f58", "#ff7b72", "#56d364", "#e3b341",
        "#79c0ff", "#d2a8ff", "#56d4dd", "#f0f6fc"
    ]

    anim_class = "static" if static else "line-anim"

    for idx, item in enumerate(lines):
        delay_style = "" if static else f' style="animation-delay: {delay:.3f}s;"'
        
        if item["type"] == "header":
            svg.append(
                f'  <g class="{anim_class}"{delay_style}>\n'
                f'    <text class="mono user" x="24" y="{y}">{item["user"]}</text>'
                f'<text class="mono at" x="80" y="{y}">@</text>'
                f'<text class="mono host" x="93" y="{y}">{item["host"]}</text>\n'
                f'  </g>'
            )
            y += 18
        elif item["type"] == "divider":
            dashes = "—" * 38
            svg.append(
                f'  <g class="{anim_class}"{delay_style}>\n'
                f'    <text class="mono divider" x="24" y="{y}">{dashes}</text>\n'
                f'  </g>'
            )
            y += 20
        elif item["type"] == "field":
            key = item["key"]
            val = item["val"]
            svg.append(
                f'  <g class="{anim_class}"{delay_style}>\n'
                f'    <text class="mono key" x="24" y="{y}">{key}</text>'
                f'<text class="mono colon" x="95" y="{y}">:</text>'
                f'<text class="mono val" x="108" y="{y}">{val}</text>\n'
                f'  </g>'
            )
            y += line_spacing
        elif item["type"] == "palette":
            y += 8
            # Palette box size
            box_w = 21
            box_h = 10
            svg.append(f'  <g class="{anim_class}"{delay_style}>')
            # Row 1
            for p_i, color in enumerate(normal_palette):
                bx = 24 + p_i * (box_w + 3)
                svg.append(
                    f'    <rect x="{bx}" y="{y}" width="{box_w}" height="{box_h}" rx="2" fill="{color}"/>'
                )
            # Row 2
            y += box_h + 3
            for p_i, color in enumerate(bright_palette):
                bx = 24 + p_i * (box_w + 3)
                svg.append(
                    f'    <rect x="{bx}" y="{y}" width="{box_w}" height="{box_h}" rx="2" fill="{color}"/>'
                )
            svg.append("  </g>")

        delay += stagger

    svg.append("</svg>")
    return "\n".join(svg)


def main():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    out_path = os.path.join(base_dir, "info-card.svg")
    
    if len(sys.argv) > 1:
        out_path = sys.argv[1]
        
    static_mode = os.environ.get("STATIC", "0") == "1"
    svg_content = build_card(static=static_mode)
    
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
        
    print(f"Successfully wrote {out_path} ({WIDTH}x{HEIGHT})!")


if __name__ == "__main__":
    main()
