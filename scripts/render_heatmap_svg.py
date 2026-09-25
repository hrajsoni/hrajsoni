#!/usr/bin/env python3
"""
render_heatmap_svg.py
Reads data/contributions.json and renders a sleek, animated terminal-styled
contribution heatmap SVG (contrib-heatmap.svg) sized at 860px wide.
"""

import os
import json
from datetime import datetime

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

WIDTH = 860
HEIGHT = 205

BOX_SIZE = 10.5
GAP = 3.2
START_X = 64
START_Y = 56


def render_svg(data: dict) -> str:
    total_contribs = data.get("total_contributions", 0)
    longest_streak = data.get("longest_streak", 0)
    current_streak = data.get("current_streak", 0)
    weeks = data.get("weeks", [])
    month_labels = data.get("month_labels", [])
    
    # Keep only the last 53 weeks if more
    if len(weeks) > 53:
        weeks = weeks[-53:]
        
    svg_parts = []
    svg_parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" width="{WIDTH}" height="{HEIGHT}">'
    )
    
    # Styles and animations
    svg_parts.append("""  <style>
    @keyframes cellFade {
      0% { opacity: 0; transform: translateY(-4px) scale(0.7); }
      100% { opacity: 1; transform: translateY(0) scale(1); }
    }
    .grid-cell {
      animation: cellFade 0.3s cubic-bezier(0.16, 1, 0.3, 1) backwards;
      transform-box: fill-box;
      transform-origin: center;
    }
    .mono {
      font-family: 'SF Mono', 'Cascadia Code', 'Fira Code', Menlo, Consolas, monospace;
    }
    .label {
      font-size: 9px;
      fill: #7d8590;
    }
    .title {
      font-size: 11px;
      fill: #8b949e;
    }
    .footer-stat {
      font-size: 11px;
      fill: #8b949e;
    }
    .accent {
      fill: #39d353;
      font-weight: 600;
    }
  </style>""")
    
    # Background card
    svg_parts.append(
        f'  <rect width="{WIDTH}" height="{HEIGHT}" rx="8" fill="#0d1117" stroke="#30363d" stroke-width="1"/>'
    )
    
    # Terminal header bar
    svg_parts.append("""  <!-- Window Header -->
  <circle cx="20" cy="18" r="5" fill="#ff5f56"/>
  <circle cx="36" cy="18" r="5" fill="#ffbd2e"/>
  <circle cx="52" cy="18" r="5" fill="#27c93f"/>
  <text class="mono title" x="430" y="22" text-anchor="middle">harshit@github: ~ (contributions)</text>
  <line x1="0" y1="34" x2="860" y2="34" stroke="#21262d" stroke-width="1"/>""")

    # Month Labels
    svg_parts.append('  <!-- Month Labels -->')
    for m in month_labels:
        col = m.get("col", 0)
        # Check if column is within visible 53 weeks
        if 0 <= col < len(weeks):
            mx = START_X + col * (BOX_SIZE + GAP)
            svg_parts.append(f'  <text class="mono label" x="{mx:.1f}" y="48">{m["name"]}</text>')
            
    # Day Labels (Mon, Wed, Fri)
    day_indices = [(1, "Mon"), (3, "Wed"), (5, "Fri")]
    svg_parts.append('  <!-- Day Labels -->')
    for day_idx, label in day_indices:
        dy = START_Y + day_idx * (BOX_SIZE + GAP) + 8.5
        svg_parts.append(f'  <text class="mono label" x="{START_X - 28}" y="{dy:.1f}">{label}</text>')
        
    # Grid Cells
    svg_parts.append('  <!-- Heatmap Cells -->')
    for col_idx, week in enumerate(weeks):
        for row_idx, day in enumerate(week):
            if day is None:
                continue
            x = START_X + col_idx * (BOX_SIZE + GAP)
            y = START_Y + row_idx * (BOX_SIZE + GAP)
            
            level = day.get("level", 0)
            count = day.get("count", 0)
            
            # Highlight max days with top palette color if count is very high
            if count >= 15:
                color = PALETTE[5]
            else:
                color = PALETTE[min(level, len(PALETTE) - 1)]
                
            delay = 0.05 + (col_idx * 0.012) + (row_idx * 0.02)
            desc = day.get("description", f"{count} contributions on {day.get('date', '')}")
            
            svg_parts.append(
                f'  <rect class="grid-cell" x="{x:.1f}" y="{y:.1f}" width="{BOX_SIZE:.1f}" height="{BOX_SIZE:.1f}" '
                f'rx="2.2" fill="{color}" style="animation-delay: {delay:.3f}s;">'
                f'<title>{desc}</title></rect>'
            )
            
    # Footer: Stats on left, Legend on right
    svg_parts.append('  <!-- Footer Stats & Legend -->')
    svg_parts.append(
        f'  <text class="mono footer-stat" x="{START_X}" y="180">'
        f'<tspan class="accent">{total_contribs:,}</tspan> contributions in the last year &nbsp;·&nbsp; '
        f'Current streak: <tspan class="accent">{current_streak}d</tspan> &nbsp;·&nbsp; '
        f'Longest streak: <tspan class="accent">{longest_streak}d</tspan>'
        f'</text>'
    )
    
    # Legend
    legend_start_x = 716
    legend_y = 173
    svg_parts.append(f'  <text class="mono label" x="{legend_start_x - 26}" y="180">Less</text>')
    for i, col in enumerate(PALETTE[:5]):
        lx = legend_start_x + i * 13
        svg_parts.append(
            f'  <rect x="{lx}" y="{legend_y}" width="9.5" height="9.5" rx="2" fill="{col}"/>'
        )
    svg_parts.append(f'  <text class="mono label" x="{legend_start_x + 68}" y="180">More</text>')
    
    svg_parts.append('</svg>')
    return "\n".join(svg_parts)


def main():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_path = os.path.join(base_dir, "data", "contributions.json")
    out_path = os.path.join(base_dir, "contrib-heatmap.svg")
    
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found. Please run fetch_contributions.py first.")
        return
        
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    svg_content = render_svg(data)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
        
    print(f"Successfully generated {out_path}!")


if __name__ == "__main__":
    main()
