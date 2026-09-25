#!/usr/bin/env python3
"""
make_batman_banner.py
Renders a cinematic "The Batman" (2022) hero banner SVG (batman-banner.svg)
sized at 860px wide x 250px high.

Features:
- A wider, imposing bat silhouette with deep chest cavity.
- "HARSHIT RAJ" curved gracefully INSIDE the bat using SVG textPath.
- Attractive, bold cinematic typography (Cinzel / Impact / Arial Black).
- Breathing crimson atmospheric glow & Batcomputer telemetry.
"""

import os
import sys

WIDTH = 860
HEIGHT = 250

# Expanded, imposing Batman Chest Emblem (spans width ~730px, height ~180px)
# Center at (430, 130)
BAT_PATH = (
    "M 430,60 "
    "C 426,60 423,50 421,44 C 419,50 416,58 412,60 "
    "C 345,68 265,56 165,46 C 115,42 75,40 60,40 "
    "C 76,85 102,110 125,122 "
    "C 155,108 200,105 235,116 "
    "C 265,132 295,154 335,174 "
    "C 375,194 410,216 430,230 "
    "C 450,216 485,194 525,174 "
    "C 565,154 595,132 625,116 "
    "C 660,105 705,108 735,122 "
    "C 758,110 784,85 800,40 "
    "C 785,40 745,42 695,46 "
    "C 595,56 515,68 448,60 "
    "C 444,58 441,50 439,44 C 437,50 434,60 430,60 Z"
)

# Curved path inside the bat for "HARSHIT RAJ" (graceful gentle arch)
TEXT_CURVE_D = "M 180,128 Q 430,94 680,128"


def generate_banner() -> str:
    svg = []
    svg.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" width="{WIDTH}" height="{HEIGHT}">'
    )

    # Styles
    svg.append("""  <style>
    @keyframes pulseGlow {
      0%, 100% { opacity: 0.55; filter: drop-shadow(0 0 12px rgba(255, 26, 43, 0.45)); }
      50% { opacity: 0.95; filter: drop-shadow(0 0 32px rgba(255, 26, 43, 0.85)); }
    }
    @keyframes textGlow {
      0%, 100% { filter: drop-shadow(0 0 8px rgba(255, 26, 43, 0.7)); }
      50% { filter: drop-shadow(0 0 18px rgba(255, 59, 75, 1)); }
    }
    .bat-emblem {
      animation: pulseGlow 4s ease-in-out infinite;
    }
    .curved-name {
      animation: textGlow 4s ease-in-out infinite;
      font-family: 'Cinzel', 'Impact', 'Haettenschweiler', 'Arial Black', sans-serif;
      font-weight: 900;
      font-size: 34px;
      letter-spacing: 7px;
    }
    .mono {
      font-family: 'SF Mono', 'Cascadia Code', 'Fira Code', Menlo, Consolas, monospace;
    }
    .subhead {
      font-family: 'SF Mono', 'Cascadia Code', Consolas, monospace;
      font-size: 11.5px;
      letter-spacing: 3.5px;
      text-transform: uppercase;
      fill: #ff2e3e;
      font-weight: 700;
    }
    .tag {
      font-size: 9.5px;
      fill: #8b949e;
      letter-spacing: 1.5px;
    }
    .tag-val {
      fill: #ff3b4b;
      font-weight: 700;
    }
    .quote {
      font-family: 'SF Mono', 'Cascadia Code', Menlo, Consolas, monospace;
      font-size: 11px;
      fill: #d1d5db;
      letter-spacing: 1px;
    }
  </style>""")

    # Defs
    svg.append(f"""  <defs>
    <!-- Background atmospheric gradient -->
    <radialGradient id="bgGlow" cx="50%" cy="50%" r="68%">
      <stop offset="0%" stop-color="#220306" stop-opacity="0.95"/>
      <stop offset="55%" stop-color="#110204" stop-opacity="0.98"/>
      <stop offset="100%" stop-color="#060709" stop-opacity="1"/>
    </radialGradient>

    <!-- Bat emblem fill gradient -->
    <linearGradient id="batFill" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#2a0509" stop-opacity="0.85"/>
      <stop offset="45%" stop-color="#170305" stop-opacity="0.92"/>
      <stop offset="100%" stop-color="#0a0102" stop-opacity="0.96"/>
    </linearGradient>

    <!-- Text gradient for HARSHIT RAJ -->
    <linearGradient id="nameGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="60%" stop-color="#fff5f5"/>
      <stop offset="100%" stop-color="#ffb3ba"/>
    </linearGradient>

    <!-- Header & footer accent line gradient -->
    <linearGradient id="redLine" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#ff1a2b" stop-opacity="0"/>
      <stop offset="25%" stop-color="#ff1a2b" stop-opacity="0.85"/>
      <stop offset="75%" stop-color="#ff1a2b" stop-opacity="0.85"/>
      <stop offset="100%" stop-color="#ff1a2b" stop-opacity="0"/>
    </linearGradient>

    <!-- Guide path for curved text inside the bat -->
    <path id="batTextCurve" d="{TEXT_CURVE_D}" fill="none"/>
  </defs>""")

    # Background card
    svg.append(f'  <rect width="{WIDTH}" height="{HEIGHT}" rx="8" fill="url(#bgGlow)"/>')
    svg.append(
        f'  <rect width="{WIDTH}" height="{HEIGHT}" rx="8" fill="none" stroke="#380a0e" stroke-width="1"/>'
    )

    # Subtle HUD Grid lines
    svg.append("""  <!-- HUD Grid lines -->
  <g opacity="0.10" stroke="#ff1a2b" stroke-width="0.5">
    <line x1="40" y1="0" x2="40" y2="250"/>
    <line x1="820" y1="0" x2="820" y2="250"/>
    <line x1="0" y1="36" x2="860" y2="36"/>
    <line x1="0" y1="214" x2="860" y2="214"/>
  </g>""")

    # Bat Emblem in Background (Center-aligned, spanning wings)
    svg.append(f"""  <!-- The Batman Emblem (Container for Identity) -->
  <path class="bat-emblem" d="{BAT_PATH}" fill="url(#batFill)" stroke="#ff1a2b" stroke-width="1.4"/>""")

    # Top Terminal Readout Bar
    svg.append("""  <!-- Top Status Bar -->
  <circle cx="20" cy="18" r="4.5" fill="#ff1a2b"/>
  <circle cx="34" cy="18" r="4.5" fill="#7f1d1d"/>
  <circle cx="48" cy="18" r="4.5" fill="#262626"/>
  <text class="mono tag" x="65" y="22">WAYNE ENTERPRISES // BATCOMPUTER OS v4.2</text>
  <text class="mono tag" x="840" y="22" text-anchor="end">SYS.STATUS: <tspan class="tag-val">ACTIVE IN SHADOWS</tspan></text>
  <line x1="20" y1="36" x2="840" y2="36" stroke="url(#redLine)" stroke-width="1"/>""")

    # Curved Name: "HARSHIT RAJ" INSIDE THE BAT
    svg.append("""  <!-- Curved Name INSIDE the Bat Emblem -->
  <text class="curved-name" fill="url(#nameGrad)">
    <textPath href="#batTextCurve" startOffset="50%" text-anchor="middle">
      HARSHIT RAJ
    </textPath>
  </text>""")

    # Subtitles & Quote INSIDE / under the chest cavity
    svg.append("""  <!-- Core Title & Directives -->
  <text class="subhead" x="430" y="160" text-anchor="middle">
    FULL-STACK DEVELOPER // ECOMMERCE ARCHITECT
  </text>

  <text class="quote" x="430" y="184" text-anchor="middle">
    &quot;It&apos;s not just a signal. It&apos;s a warning.&quot;
  </text>""")

    # Bottom Metadata Strip
    svg.append("""  <!-- Bottom HUD Metadata -->
  <line x1="20" y1="214" x2="840" y2="214" stroke="url(#redLine)" stroke-width="1"/>
  <text class="mono tag" x="35" y="232">SECTOR: <tspan class="tag-val">GOTHAM CITY // IN</tspan></text>
  <text class="mono tag" x="430" y="232" text-anchor="middle">ARSENAL: <tspan fill="#d1d5db">TYPESCRIPT · NEXT.JS · LIQUID · PYTHON · NODE</tspan></text>
  <text class="mono tag" x="825" y="232" text-anchor="end">PROTOCOL: <tspan class="tag-val">VENGEANCE</tspan></text>""")

    svg.append("</svg>")
    return "\n".join(svg)


def main():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    out_path = os.path.join(base_dir, "batman-banner.svg")

    if len(sys.argv) > 1:
        out_path = sys.argv[1]

    svg_data = generate_banner()
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg_data)

    print(f"Successfully generated {out_path} ({WIDTH}x{HEIGHT})!")


if __name__ == "__main__":
    main()
