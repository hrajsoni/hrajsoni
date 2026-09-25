#!/usr/bin/env python3
"""
make_batcomputer_dossier.py
Generates a wide (860px x 430px) Batcomputer Tactical Dossier SVG
(batcomputer-dossier.svg and info-card.svg) styled with The Batman (2022)
crimson noir HUD interface, tactical diagnostics, and Wayne Tech styling.
"""

import os
import sys

WIDTH = 860
HEIGHT = 430

# The Batman 2022 Insignia (scaled for left panel badge)
# Center around (175, 115)
MINI_BAT = (
    "M 175,78 "
    "L 177,68 L 182,79 L 206,82 L 244,75 L 285,62 L 315,52 L 297,90 L 255,97 L 212,124 L 182,148 L 176,164 "
    "L 175,155 "
    "L 174,164 L 168,148 L 138,124 L 95,97 L 53,90 L 35,52 L 65,62 L 106,75 L 144,82 L 168,79 L 173,68 Z"
)


def generate_dossier(static: bool = False) -> str:
    svg = []
    svg.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" width="{WIDTH}" height="{HEIGHT}">'
    )

    # Styles
    svg.append("""  <style>
    @keyframes pulseGlow {
      0%, 100% { opacity: 0.4; filter: drop-shadow(0 0 8px rgba(255, 26, 43, 0.4)); }
      50% { opacity: 0.9; filter: drop-shadow(0 0 20px rgba(255, 26, 43, 0.8)); }
    }
    @keyframes hudFade {
      0% { opacity: 0; transform: translateY(-4px); }
      100% { opacity: 1; transform: translateY(0); }
    }
    @keyframes radarSweep {
      0% { stroke-dashoffset: 0; }
      100% { stroke-dashoffset: 360; }
    }
    .bat-badge {
      animation: pulseGlow 4s ease-in-out infinite;
    }
    .hud-line {
      animation: hudFade 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
      opacity: 0;
    }
    .static-mode {
      opacity: 1 !important;
      animation: none !important;
    }
    .mono {
      font-family: 'SF Mono', 'Cascadia Code', 'Fira Code', Menlo, Consolas, monospace;
    }
    .hud-title {
      font-size: 11px;
      fill: #8b949e;
      letter-spacing: 1px;
    }
    .section-tag {
      font-size: 10.5px;
      fill: #ff1a2b;
      font-weight: 700;
      letter-spacing: 2px;
    }
    .field-key {
      font-size: 11px;
      fill: #8b949e;
      font-weight: 600;
    }
    .field-val {
      font-size: 11px;
      fill: #e6edf3;
      font-weight: 500;
    }
    .field-accent {
      font-size: 11px;
      fill: #ff3b4b;
      font-weight: 700;
    }
    .body-txt {
      font-size: 11px;
      fill: #c9d1d9;
      line-height: 1.5;
    }
    .subtext {
      font-size: 9.5px;
      fill: #7d8590;
      letter-spacing: 0.8px;
    }
    .crosshair {
      stroke: #7f1d1d;
      stroke-width: 1;
    }
  </style>""")

    # Defs
    svg.append("""  <defs>
    <radialGradient id="dossierBg" cx="30%" cy="40%" r="75%">
      <stop offset="0%" stop-color="#140204" stop-opacity="0.9"/>
      <stop offset="60%" stop-color="#090a0d" stop-opacity="0.95"/>
      <stop offset="100%" stop-color="#050608" stop-opacity="1"/>
    </radialGradient>
    <linearGradient id="dividerGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ff1a2b" stop-opacity="0"/>
      <stop offset="20%" stop-color="#ff1a2b" stop-opacity="0.6"/>
      <stop offset="80%" stop-color="#ff1a2b" stop-opacity="0.6"/>
      <stop offset="100%" stop-color="#ff1a2b" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="batMiniFill" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ff2e3e" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="#54080e" stop-opacity="0.05"/>
    </linearGradient>
  </defs>""")

    # Background card
    svg.append(f'  <rect width="{WIDTH}" height="{HEIGHT}" rx="8" fill="url(#dossierBg)"/>')
    svg.append(
        f'  <rect width="{WIDTH}" height="{HEIGHT}" rx="8" fill="none" stroke="#380a0e" stroke-width="1"/>'
    )

    # Window Header
    svg.append("""  <!-- Window Header -->
  <circle cx="20" cy="18" r="4.5" fill="#ff1a2b"/>
  <circle cx="34" cy="18" r="4.5" fill="#7f1d1d"/>
  <circle cx="48" cy="18" r="4.5" fill="#262626"/>
  <text class="mono hud-title" x="65" y="22">batcomputer://classified/personnel/harshit-raj.dossier</text>
  <text class="mono subtext" x="840" y="22" text-anchor="end">WAYNE-TECH SECURE // 4096-BIT ENCRYPTED</text>
  <line x1="0" y1="34" x2="860" y2="34" stroke="#2a080c" stroke-width="1"/>""")

    # Central Divider (Left & Right Panels)
    svg.append("""  <!-- Center Divider & Crosshairs -->
  <line x1="330" y1="46" x2="330" y2="415" stroke="url(#dividerGrad)" stroke-width="1"/>
  <!-- Crosshairs -->
  <g class="crosshair" opacity="0.6">
    <line x1="324" y1="80" x2="336" y2="80"/>
    <line x1="330" y1="74" x2="330" y2="86"/>
    <line x1="324" y1="220" x2="336" y2="220"/>
    <line x1="330" y1="214" x2="330" y2="226"/>
    <line x1="324" y1="360" x2="336" y2="360"/>
    <line x1="330" y1="354" x2="330" y2="366"/>
  </g>""")

    anim_cls = "static-mode" if static else "hud-line"

    # ================= LEFT PANEL: Tactical Surveillance =================
    svg.append("""  <!-- Left Panel: Tactical Identity -->""")
    # Mini Bat Emblem
    svg.append(
        f'  <path class="bat-badge" d="{MINI_BAT}" fill="url(#batMiniFill)" stroke="#ff1a2b" stroke-width="1.1"/>'
    )

    left_fields = [
        ("OPERATIVE", "Harshit Raj", "field-val"),
        ("ALIAS", "The Architect", "field-accent"),
        ("AFFILIATION", "Wayne Tech // Batcave", "field-val"),
        ("SECTOR", "Gotham City // India 🇮🇳", "field-val"),
        ("CLEARANCE", "LEVEL 0 (CLASSIFIED)", "field-accent"),
        ("SPECIALTY", "High-Velocity Systems", "field-val"),
        ("THREAT LEVEL", "Fatal to Slow Stores", "field-accent"),
    ]

    ly = 185
    for i, (k, v, v_cls) in enumerate(left_fields):
        d_val = 0.05 + (i * 0.05)
        d_style = "" if static else f' style="animation-delay: {d_val:.3f}s;"'
        svg.append(
            f'  <g class="{anim_cls}"{d_style}>\n'
            f'    <text class="mono field-key" x="24" y="{ly}">{k}:</text>\n'
            f'    <text class="mono {v_cls}" x="125" y="{ly}">{v}</text>\n'
            f'  </g>'
        )
        ly += 21

    # Heartrate / Frequency waveform
    svg.append(f"""  <!-- Waveform Audio/Vitals Monitor -->
  <g class="{anim_cls}" style="animation-delay: 0.45s;">
    <text class="mono subtext" x="24" y="348">NEURAL METRICS // VITALS</text>
    <polyline points="24,372 70,372 80,362 90,382 100,358 112,388 122,372 170,372 180,364 190,380 200,372 310,372" 
              fill="none" stroke="#ff1a2b" stroke-width="1.2" opacity="0.85"/>
  </g>""")

    # Batman Diagnostic Color Palette
    bat_palette = [
        "#050608", "#1c0407", "#380a0e", "#5c0e14",
        "#8c141d", "#bd1d27", "#ff1a2b", "#ffffff"
    ]
    svg.append(f"""  <!-- Diagnostic Palette -->
  <g class="{anim_cls}" style="animation-delay: 0.5s;">""")
    for pi, color in enumerate(bat_palette):
        px = 24 + (pi * 35)
        svg.append(
            f'    <rect x="{px}" y="394" width="28" height="8" rx="2" fill="{color}" stroke="#1f0507" stroke-width="0.5"/>'
        )
    svg.append("  </g>")

    # ================= RIGHT PANEL: Tactical Operations & Arsenal =================
    svg.append("""  <!-- Right Panel: Operations & Arsenal -->""")

    rx = 352
    ry = 62

    # Section 1: Core Directive
    svg.append(f"""  <g class="{anim_cls}" style="animation-delay: 0.15s;">
    <text class="mono section-tag" x="{rx}" y="{ry}">// 01. CORE DIRECTIVE</text>
    <text class="mono body-txt" x="{rx}" y="{ry + 20}">
      Architecting high-velocity web engines, bespoke Shopify themes,
    </text>
    <text class="mono body-txt" x="{rx}" y="{ry + 38}">
      and bulletproof full-stack platforms with obsessive precision.
    </text>
  </g>""")

    # Section 2: Tactical Arsenal
    ry += 76
    svg.append(f"""  <g class="{anim_cls}" style="animation-delay: 0.25s;">
    <text class="mono section-tag" x="{rx}" y="{ry}">// 02. TACTICAL ARSENAL</text>
    
    <text class="mono field-key" x="{rx}" y="{ry + 22}">LANGUAGES :</text>
    <text class="mono field-val" x="{rx + 95}" y="{ry + 22}">TypeScript, JavaScript, Python, Liquid, Kotlin, SQL</text>

    <text class="mono field-key" x="{rx}" y="{ry + 42}">FRAMEWORKS:</text>
    <text class="mono field-val" x="{rx + 95}" y="{ry + 42}">Next.js, React, Node.js, Express, TailwindCSS</text>

    <text class="mono field-key" x="{rx}" y="{ry + 62}">PLATFORMS :</text>
    <text class="mono field-val" x="{rx + 95}" y="{ry + 62}">Shopify (Headless &amp; Liquid), GitHub Actions, Vercel</text>
  </g>""")

    # Section 3: Tactical Deployments
    ry += 96
    svg.append(f"""  <g class="{anim_cls}" style="animation-delay: 0.35s;">
    <text class="mono section-tag" x="{rx}" y="{ry}">// 03. ACTIVE DEPLOYMENTS</text>

    <text class="mono field-accent" x="{rx}" y="{ry + 22}">▶ OLD LOOM</text>
    <text class="mono subtext" x="{rx + 110}" y="{ry + 22}">Luxury eCommerce brand experience &amp; fluid motion</text>

    <text class="mono field-accent" x="{rx}" y="{ry + 42}">▶ CARECONNECT</text>
    <text class="mono subtext" x="{rx + 110}" y="{ry + 42}">Mission-critical health-tech management engine</text>

    <text class="mono field-accent" x="{rx}" y="{ry + 62}">▶ MOTIONPORTFOLIO</text>
    <text class="mono subtext" x="{rx + 110}" y="{ry + 62}">3D canvas interaction &amp; high-fidelity creative dev</text>

    <text class="mono field-accent" x="{rx}" y="{ry + 82}">▶ SMART JEWELLER</text>
    <text class="mono subtext" x="{rx + 110}" y="{ry + 82}">Native Android real-time billing &amp; inventory system</text>
  </g>""")

    # Section 4: Secure Comms
    ry += 114
    svg.append(f"""  <g class="{anim_cls}" style="animation-delay: 0.45s;">
    <text class="mono section-tag" x="{rx}" y="{ry}">// 04. ENCRYPTED COMMS FREQUENCY</text>
    <text class="mono subtext" x="{rx}" y="{ry + 20}">DISPATCH: <tspan class="field-val">hraj491@gmail.com</tspan> &nbsp;·&nbsp; NETWORK: <tspan class="field-val">github.com/hrajsoni</tspan></text>
  </g>""")

    svg.append("</svg>")
    return "\n".join(svg)


def main():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    dossier_path = os.path.join(base_dir, "batcomputer-dossier.svg")
    info_card_path = os.path.join(base_dir, "info-card.svg")
    
    static_mode = os.environ.get("STATIC", "0") == "1"
    svg_data = generate_dossier(static=static_mode)
    
    with open(dossier_path, "w", encoding="utf-8") as f:
        f.write(svg_data)
    with open(info_card_path, "w", encoding="utf-8") as f:
        f.write(svg_data)
        
    print(f"Successfully generated {dossier_path} and {info_card_path} ({WIDTH}x{HEIGHT})!")


if __name__ == "__main__":
    main()
