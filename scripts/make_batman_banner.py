#!/usr/bin/env python3
"""
make_batman_banner.py
Renders a cinematic "The Batman" (2022) styled hero banner SVG (batman-banner.svg)
sized at 860px wide x 230px high, featuring the razor-sharp chest bat-insignia,
intense crimson smoke glow, and Batcomputer HUD status typography.
"""

import os
import sys

WIDTH = 860
HEIGHT = 230

# The Batman 2022 Chest Emblem (precise geometric bat silhouette)
BAT_PATH = (
    "M 430,72 "
    "L 434,56 L 441,74 L 476,78 L 532,68 L 610,50 L 670,36 L 634,92 L 570,102 L 505,142 L 460,178 L 436,202 "
    "L 430,188 "
    "L 424,202 L 400,178 L 355,142 L 290,102 L 226,92 L 190,36 L 250,50 L 328,68 L 384,78 L 419,74 L 426,56 Z"
)


def generate_banner() -> str:
    svg = []
    svg.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" width="{WIDTH}" height="{HEIGHT}">'
    )
    
    # Styles & Animations
    svg.append("""  <style>
    @keyframes pulseGlow {
      0%, 100% { opacity: 0.35; filter: drop-shadow(0 0 15px rgba(255, 26, 43, 0.4)); }
      50% { opacity: 0.75; filter: drop-shadow(0 0 35px rgba(255, 26, 43, 0.85)); }
    }
    @keyframes scanline {
      0% { transform: translateY(-100%); }
      100% { transform: translateY(1000%); }
    }
    @keyframes glitchFade {
      0% { opacity: 0; transform: translateY(-5px); }
      100% { opacity: 1; transform: translateY(0); }
    }
    .bat-emblem {
      animation: pulseGlow 4s ease-in-out infinite;
      transform-origin: center;
    }
    .mono {
      font-family: 'SF Mono', 'Cascadia Code', 'Fira Code', Menlo, Consolas, monospace;
    }
    .headline {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
      font-weight: 900;
      letter-spacing: 5px;
      text-transform: uppercase;
    }
    .subhead {
      font-family: 'SF Mono', 'Cascadia Code', Consolas, monospace;
      font-size: 11px;
      letter-spacing: 3.5px;
      text-transform: uppercase;
      fill: #ff1a2b;
      font-weight: 600;
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
    .border-glow {
      stroke: #380a0e;
      stroke-width: 1;
    }
  </style>""")

    # Defs: Gradients and filters
    svg.append("""  <defs>
    <!-- Background crimson atmospheric gradient -->
    <radialGradient id="bgGlow" cx="50%" cy="50%" r="65%">
      <stop offset="0%" stop-color="#2a0508" stop-opacity="0.9"/>
      <stop offset="50%" stop-color="#140204" stop-opacity="0.95"/>
      <stop offset="100%" stop-color="#060709" stop-opacity="1"/>
    </radialGradient>

    <!-- Linear accent line gradient -->
    <linearGradient id="redLine" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#ff1a2b" stop-opacity="0"/>
      <stop offset="30%" stop-color="#ff1a2b" stop-opacity="0.8"/>
      <stop offset="70%" stop-color="#ff1a2b" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#ff1a2b" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="batFill" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ff2e3e" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="#7a0912" stop-opacity="0.08"/>
    </linearGradient>
  </defs>""")

    # Background card
    svg.append(f'  <rect width="{WIDTH}" height="{HEIGHT}" rx="8" fill="url(#bgGlow)"/>')
    svg.append(f'  <rect width="{WIDTH}" height="{HEIGHT}" rx="8" fill="none" class="border-glow"/>')

    # Subtle Batcomputer grid lines
    svg.append("""  <!-- HUD Grid lines -->
  <g opacity="0.12" stroke="#ff1a2b" stroke-width="0.5">
    <line x1="40" y1="0" x2="40" y2="230"/>
    <line x1="820" y1="0" x2="820" y2="230"/>
    <line x1="0" y1="36" x2="860" y2="36"/>
    <line x1="0" y1="194" x2="860" y2="194"/>
  </g>""")

    # Bat Emblem in Background (Center-aligned)
    svg.append(f"""  <!-- The Batman 2022 Insignia -->
  <path class="bat-emblem" d="{BAT_PATH}" fill="url(#batFill)" stroke="#ff1a2b" stroke-width="1.2"/>""")

    # Top Terminal Readout Bar
    svg.append("""  <!-- Top Status Bar -->
  <circle cx="20" cy="18" r="4.5" fill="#ff1a2b"/>
  <circle cx="34" cy="18" r="4.5" fill="#7f1d1d"/>
  <circle cx="48" cy="18" r="4.5" fill="#262626"/>
  <text class="mono tag" x="65" y="22">WAYNE ENTERPRISES // BATCOMPUTER OS v4.2</text>
  <text class="mono tag" x="840" y="22" text-anchor="end">SYS.STATUS: <tspan class="tag-val">ACTIVE IN SHADOWS</tspan></text>
  <line x1="20" y1="36" x2="840" y2="36" stroke="url(#redLine)" stroke-width="1"/>""")

    # Main Headline & Titles (Center)
    svg.append("""  <!-- Central Identity -->
  <text class="headline" x="430" y="98" text-anchor="middle" font-size="34" fill="#ffffff" filter="drop-shadow(0 0 12px rgba(255,26,43,0.5))">
    HARSHIT RAJ
  </text>
  
  <text class="subhead" x="430" y="124" text-anchor="middle">
    FULL-STACK DEVELOPER // ECOMMERCE ARCHITECT
  </text>

  <!-- Quote & Directive -->
  <text class="mono" x="430" y="152" text-anchor="middle" font-size="11.5" fill="#c9d1d9" letter-spacing="1.2">
    &ldquo;It&apos;s not just a signal. It&apos;s a warning.&rdquo;
  </text>""")

    # Bottom Metadata Strip
    svg.append("""  <!-- Bottom HUD Metadata -->
  <line x1="20" y1="194" x2="840" y2="194" stroke="url(#redLine)" stroke-width="1"/>
  <text class="mono tag" x="35" y="212">SECTOR: <tspan class="tag-val">GOTHAM CITY // IN</tspan></text>
  <text class="mono tag" x="430" y="212" text-anchor="middle">ARSENAL: <tspan fill="#d1d5db">TYPESCRIPT · NEXT.JS · LIQUID · PYTHON · NODE</tspan></text>
  <text class="mono tag" x="825" y="212" text-anchor="end">PROTOCOL: <tspan class="tag-val">VENGEANCE</tspan></text>""")

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
