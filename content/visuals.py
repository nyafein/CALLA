"""
Visual elements for Calla — characters with expressions and page backgrounds.

Style: minimalistic. Single-color silhouettes for backgrounds, simple
shapes + small accent colors for characters. Restrained palette of
white / cream / red (#c8302b — the iconic Belarusian embroidery red) /
muted earth tones / soft sky blue.

Returns SVG strings ready to drop into st.markdown(unsafe_allow_html=True).
The viewBox attribute makes everything scale to whatever container width
Streamlit gives us.
"""

# =====================================================================
# Color palette — kept central so visual identity stays consistent.
# =====================================================================
RED        = "#c8302b"   # embroidery red, the cultural anchor color
DARK       = "#2a2a2a"   # outline / detail
SKIN       = "#fce4d6"   # face fill
HAIR_BLOND = "#dba35a"   # girl's hair
HAIR_RED   = "#c8631e"   # boy's hair
BOOT_BROWN = "#5a2818"   # leather
BERRY      = "#f4c430"   # flower centers / accent
SKY_TOP    = "#cfe6f0"   # high sky
SKY_BOT    = "#f6e8d8"   # warmer near-horizon
SUN        = "#f4c430"   # sun
BRICK      = "#a64b3c"   # Mir Castle red brick
FOREST     = "#3a5a40"   # Białowieża pine
FOREST_LT  = "#588157"   # lighter forest accent
STONE      = "#8a8a8a"   # urban silhouette


# =====================================================================
# CHARACTERS
# =====================================================================
# Each character is built from a static body SVG plus a swappable face
# group keyed by expression. Three expressions: neutral, happy, confused.
# =====================================================================

def _face(expression: str, cx: int = 100, cy: int = 85) -> str:
    """
    Return SVG markup for one of three facial expressions.
    Drawn relative to a head centered at (cx, cy).
    """
    if expression == "happy":
        # Closed-curve smiling eyes (^_^), wide upturned smile.
        return f'''
            <path d="M {cx-18} {cy-3} q 6 -8 12 0" stroke="{DARK}" stroke-width="2.5" fill="none" stroke-linecap="round"/>
            <path d="M {cx+6} {cy-3} q 6 -8 12 0" stroke="{DARK}" stroke-width="2.5" fill="none" stroke-linecap="round"/>
            <path d="M {cx-12} {cy+15} q 12 10 24 0" stroke="{DARK}" stroke-width="2.5" fill="none" stroke-linecap="round"/>
            <circle cx="{cx-22}" cy="{cy+10}" r="4" fill="{RED}" opacity="0.35"/>
            <circle cx="{cx+22}" cy="{cy+10}" r="4" fill="{RED}" opacity="0.35"/>
        '''
    elif expression == "confused":
        # Asymmetric eyes (one wide, one squinted), wavy mouth, tilted brow.
        return f'''
            <circle cx="{cx-12}" cy="{cy}" r="3.5" fill="{DARK}"/>
            <path d="M {cx+6} {cy-1} q 6 4 12 -1" stroke="{DARK}" stroke-width="2" fill="none" stroke-linecap="round"/>
            <path d="M {cx-18} {cy-12} q 6 -3 12 1" stroke="{DARK}" stroke-width="1.5" fill="none" stroke-linecap="round"/>
            <path d="M {cx-10} {cy+15} q 5 -4 10 0 q 5 4 10 0" stroke="{DARK}" stroke-width="2" fill="none" stroke-linecap="round"/>
        '''
    else:  # neutral
        return f'''
            <circle cx="{cx-12}" cy="{cy}" r="3" fill="{DARK}"/>
            <circle cx="{cx+12}" cy="{cy}" r="3" fill="{DARK}"/>
            <path d="M {cx-8} {cy+15} q 8 4 16 0" stroke="{DARK}" stroke-width="2" fill="none" stroke-linecap="round"/>
        '''


def render_girl(expression: str = "neutral") -> str:
    """SVG for the girl character — вянок (flower wreath), вышыванка, фартух."""
    return f'''
    <svg viewBox="0 0 200 290" xmlns="http://www.w3.org/2000/svg" width="100%" style="max-width: 200px;">
      <!-- Skirt -->
      <path d="M 55 200 L 40 275 L 160 275 L 145 200 Z" fill="white" stroke="{DARK}" stroke-width="2"/>
      <!-- Skirt embroidery band -->
      <rect x="44" y="255" width="112" height="6" fill="{RED}"/>
      <circle cx="60" cy="240" r="2" fill="{RED}"/>
      <circle cx="80" cy="240" r="2" fill="{RED}"/>
      <circle cx="100" cy="240" r="2" fill="{RED}"/>
      <circle cx="120" cy="240" r="2" fill="{RED}"/>
      <circle cx="140" cy="240" r="2" fill="{RED}"/>
      <!-- Apron (фартух) -->
      <path d="M 75 200 L 70 270 L 130 270 L 125 200 Z" fill="{RED}"/>
      <line x1="76" y1="220" x2="124" y2="220" stroke="white" stroke-width="1.5"/>
      <line x1="74" y1="240" x2="126" y2="240" stroke="white" stroke-width="1.5"/>
      <!-- Vyshyvanka (top) -->
      <path d="M 60 130 L 55 205 L 145 205 L 140 130 Z" fill="white" stroke="{DARK}" stroke-width="2"/>
      <!-- Sleeves -->
      <ellipse cx="55" cy="160" rx="12" ry="25" fill="white" stroke="{DARK}" stroke-width="2"/>
      <ellipse cx="145" cy="160" rx="12" ry="25" fill="white" stroke="{DARK}" stroke-width="2"/>
      <line x1="44" y1="170" x2="66" y2="170" stroke="{RED}" stroke-width="2"/>
      <line x1="134" y1="170" x2="156" y2="170" stroke="{RED}" stroke-width="2"/>
      <!-- Embroidery on chest -->
      <line x1="75" y1="155" x2="125" y2="155" stroke="{RED}" stroke-width="2.5"/>
      <line x1="75" y1="180" x2="125" y2="180" stroke="{RED}" stroke-width="2.5"/>
      <path d="M 95 165 l 5 -5 l 5 5 l -5 5 z" fill="{RED}"/>
      <!-- Necklace (каралі) -->
      <circle cx="92" cy="135" r="2.5" fill="{RED}"/>
      <circle cx="100" cy="138" r="2.5" fill="{RED}"/>
      <circle cx="108" cy="135" r="2.5" fill="{RED}"/>
      <!-- Neck -->
      <rect x="92" y="115" width="16" height="15" fill="{SKIN}" stroke="{DARK}" stroke-width="1.5"/>
      <!-- Head -->
      <circle cx="100" cy="85" r="38" fill="{SKIN}" stroke="{DARK}" stroke-width="2"/>
      <!-- Braids (касы) -->
      <path d="M 65 90 q -10 40 -8 80 l 12 0 q 0 -38 8 -75 z" fill="{HAIR_BLOND}" stroke="{DARK}" stroke-width="1.5"/>
      <path d="M 135 90 q 10 40 8 80 l -12 0 q 0 -38 -8 -75 z" fill="{HAIR_BLOND}" stroke="{DARK}" stroke-width="1.5"/>
      <line x1="62" y1="120" x2="74" y2="120" stroke="{DARK}" stroke-width="1" opacity="0.4"/>
      <line x1="60" y1="140" x2="74" y2="140" stroke="{DARK}" stroke-width="1" opacity="0.4"/>
      <line x1="126" y1="120" x2="138" y2="120" stroke="{DARK}" stroke-width="1" opacity="0.4"/>
      <line x1="126" y1="140" x2="140" y2="140" stroke="{DARK}" stroke-width="1" opacity="0.4"/>
      <!-- Bangs -->
      <path d="M 65 60 q 35 -22 70 0 q -8 12 -22 8 q -13 -3 -26 0 q -14 -4 -22 -8 z" fill="{HAIR_BLOND}" stroke="{DARK}" stroke-width="1.5"/>
      <!-- Wreath (вянок) — daisy ring -->
      <g>
        <circle cx="62" cy="55" r="6" fill="white" stroke="{DARK}" stroke-width="1"/>
        <circle cx="76" cy="42" r="6" fill="white" stroke="{DARK}" stroke-width="1"/>
        <circle cx="92" cy="36" r="6" fill="white" stroke="{DARK}" stroke-width="1"/>
        <circle cx="108" cy="36" r="6" fill="white" stroke="{DARK}" stroke-width="1"/>
        <circle cx="124" cy="42" r="6" fill="white" stroke="{DARK}" stroke-width="1"/>
        <circle cx="138" cy="55" r="6" fill="white" stroke="{DARK}" stroke-width="1"/>
        <circle cx="62" cy="55" r="2" fill="{BERRY}"/>
        <circle cx="76" cy="42" r="2" fill="{BERRY}"/>
        <circle cx="92" cy="36" r="2" fill="{BERRY}"/>
        <circle cx="108" cy="36" r="2" fill="{BERRY}"/>
        <circle cx="124" cy="42" r="2" fill="{BERRY}"/>
        <circle cx="138" cy="55" r="2" fill="{BERRY}"/>
        <!-- small leaves -->
        <ellipse cx="68" cy="48" rx="3" ry="2" fill="{FOREST_LT}" transform="rotate(-30 68 48)"/>
        <ellipse cx="132" cy="48" rx="3" ry="2" fill="{FOREST_LT}" transform="rotate(30 132 48)"/>
      </g>
      <!-- Face (swappable) -->
      {_face(expression, 100, 85)}
    </svg>
    '''


def render_boy(expression: str = "neutral") -> str:
    """SVG for the boy character — вышыванка, пояс, штаны, боты."""
    return f'''
    <svg viewBox="0 0 200 290" xmlns="http://www.w3.org/2000/svg" width="100%" style="max-width: 200px;">
      <!-- Trousers (штаны) -->
      <path d="M 75 200 L 72 260 L 95 260 L 100 210 L 105 260 L 128 260 L 125 200 Z" fill="white" stroke="{DARK}" stroke-width="2"/>
      <!-- Boots (боты) -->
      <path d="M 70 258 L 67 275 L 96 275 L 96 258 Z" fill="{BOOT_BROWN}" stroke="{DARK}" stroke-width="1.5"/>
      <path d="M 104 258 L 104 275 L 133 275 L 130 258 Z" fill="{BOOT_BROWN}" stroke="{DARK}" stroke-width="1.5"/>
      <!-- Vyshyvanka shirt -->
      <path d="M 60 130 L 55 200 L 145 200 L 140 130 Z" fill="white" stroke="{DARK}" stroke-width="2"/>
      <!-- Sleeves -->
      <ellipse cx="55" cy="160" rx="12" ry="25" fill="white" stroke="{DARK}" stroke-width="2"/>
      <ellipse cx="145" cy="160" rx="12" ry="25" fill="white" stroke="{DARK}" stroke-width="2"/>
      <line x1="44" y1="170" x2="66" y2="170" stroke="{RED}" stroke-width="2"/>
      <line x1="134" y1="170" x2="156" y2="170" stroke="{RED}" stroke-width="2"/>
      <!-- Belt (пояс) — woven sash -->
      <rect x="55" y="195" width="90" height="8" fill="{RED}"/>
      <line x1="55" y1="199" x2="145" y2="199" stroke="{BERRY}" stroke-width="1.5" stroke-dasharray="4 3"/>
      <!-- Embroidery on chest — vertical center line + cross-stitch motif -->
      <line x1="100" y1="130" x2="100" y2="195" stroke="{RED}" stroke-width="2"/>
      <path d="M 95 145 l 5 -5 l 5 5 l -5 5 z" fill="{RED}"/>
      <path d="M 95 165 l 5 -5 l 5 5 l -5 5 z" fill="{RED}"/>
      <path d="M 95 185 l 5 -5 l 5 5 l -5 5 z" fill="{RED}"/>
      <!-- Collar embroidery -->
      <line x1="80" y1="135" x2="120" y2="135" stroke="{RED}" stroke-width="2"/>
      <!-- Neck -->
      <rect x="92" y="115" width="16" height="15" fill="{SKIN}" stroke="{DARK}" stroke-width="1.5"/>
      <!-- Head -->
      <circle cx="100" cy="85" r="38" fill="{SKIN}" stroke="{DARK}" stroke-width="2"/>
      <!-- Hair (red, short) -->
      <path d="M 62 70 q 0 -38 38 -45 q 38 7 38 45 q -10 -10 -38 -10 q -28 0 -38 10 z" fill="{HAIR_RED}" stroke="{DARK}" stroke-width="1.5"/>
      <path d="M 95 50 q -3 8 -10 12" stroke="{DARK}" stroke-width="1" fill="none" opacity="0.5"/>
      <!-- Ears -->
      <ellipse cx="62" cy="85" rx="4" ry="7" fill="{SKIN}" stroke="{DARK}" stroke-width="1.5"/>
      <ellipse cx="138" cy="85" rx="4" ry="7" fill="{SKIN}" stroke="{DARK}" stroke-width="1.5"/>
      <!-- Face (swappable) -->
      {_face(expression, 100, 85)}
    </svg>
    '''


def render_character(char_id: str, expression: str = "neutral") -> str:
    """Dispatch to the right character renderer."""
    if char_id == "girl":
        return render_girl(expression)
    elif char_id == "boy":
        return render_boy(expression)
    else:
        return ""


# =====================================================================
# BACKGROUNDS — page-level visual scenes
# =====================================================================

def render_app_landing_scene() -> str:
    """
    Bottom-of-page atmospheric scene for the app landing:
    Mir Castle silhouette + sky gradient + sun + a few clouds.
    No animation — clouds are static (per the user request).
    """
    return f'''
    <svg viewBox="0 0 1200 380" xmlns="http://www.w3.org/2000/svg" width="100%" style="max-height: 380px; display: block;">
      <!-- Sky gradient -->
      <defs>
        <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="{SKY_TOP}"/>
          <stop offset="100%" stop-color="{SKY_BOT}"/>
        </linearGradient>
        <linearGradient id="brick" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="{BRICK}"/>
          <stop offset="100%" stop-color="#7e3729"/>
        </linearGradient>
      </defs>
      <rect width="1200" height="380" fill="url(#sky)"/>

      <!-- Sun in upper-right corner -->
      <circle cx="1050" cy="90" r="42" fill="{SUN}" opacity="0.85"/>
      <circle cx="1050" cy="90" r="58" fill="{SUN}" opacity="0.18"/>

      <!-- Clouds (static) -->
      <g fill="white" opacity="0.85">
        <ellipse cx="200" cy="90" rx="55" ry="16"/>
        <ellipse cx="240" cy="80" rx="38" ry="14"/>
        <ellipse cx="170" cy="80" rx="32" ry="12"/>
      </g>
      <g fill="white" opacity="0.75">
        <ellipse cx="600" cy="120" rx="65" ry="18"/>
        <ellipse cx="640" cy="108" rx="40" ry="14"/>
      </g>
      <g fill="white" opacity="0.7">
        <ellipse cx="900" cy="70" rx="45" ry="14"/>
        <ellipse cx="930" cy="62" rx="30" ry="10"/>
      </g>

      <!-- Distant tree line -->
      <path d="M 0 280 L 0 270 L 60 260 L 120 270 L 180 258 L 240 268 L 300 262 L 360 270 L 420 260 L 480 268 L 540 262 L 600 270 L 660 260 L 720 268 L 780 262 L 840 268 L 900 260 L 960 268 L 1020 262 L 1080 270 L 1140 260 L 1200 268 L 1200 290 Z"
            fill="{FOREST}" opacity="0.5"/>

      <!-- Mir Castle — stylized silhouette anchored at bottom -->
      <g transform="translate(380, 180)">
        <!-- Main wall -->
        <rect x="0" y="80" width="440" height="120" fill="url(#brick)" stroke="{DARK}" stroke-width="1.5"/>
        <!-- Crenellations on wall top -->
        <g fill="url(#brick)" stroke="{DARK}" stroke-width="1.5">
          <rect x="20" y="70" width="14" height="14"/>
          <rect x="60" y="70" width="14" height="14"/>
          <rect x="100" y="70" width="14" height="14"/>
          <rect x="180" y="70" width="14" height="14"/>
          <rect x="220" y="70" width="14" height="14"/>
          <rect x="260" y="70" width="14" height="14"/>
          <rect x="340" y="70" width="14" height="14"/>
          <rect x="380" y="70" width="14" height="14"/>
          <rect x="420" y="70" width="14" height="14"/>
        </g>
        <!-- Left corner tower -->
        <rect x="-15" y="20" width="60" height="180" fill="url(#brick)" stroke="{DARK}" stroke-width="1.5"/>
        <polygon points="-15,20 15,-30 45,20" fill="{BRICK}" stroke="{DARK}" stroke-width="1.5"/>
        <polygon points="-15,20 15,-30 45,20" fill="#5a2818" opacity="0.6"/>
        <!-- Right corner tower -->
        <rect x="395" y="20" width="60" height="180" fill="url(#brick)" stroke="{DARK}" stroke-width="1.5"/>
        <polygon points="395,20 425,-30 455,20" fill="{BRICK}" stroke="{DARK}" stroke-width="1.5"/>
        <polygon points="395,20 425,-30 455,20" fill="#5a2818" opacity="0.6"/>
        <!-- Center tower (taller) -->
        <rect x="195" y="-10" width="50" height="210" fill="url(#brick)" stroke="{DARK}" stroke-width="1.5"/>
        <polygon points="195,-10 220,-70 245,-10" fill="{BRICK}" stroke="{DARK}" stroke-width="1.5"/>
        <polygon points="195,-10 220,-70 245,-10" fill="#5a2818" opacity="0.6"/>
        <!-- Windows -->
        <rect x="10" y="60" width="6" height="14" fill="{DARK}" opacity="0.7"/>
        <rect x="22" y="60" width="6" height="14" fill="{DARK}" opacity="0.7"/>
        <rect x="10" y="100" width="6" height="14" fill="{DARK}" opacity="0.7"/>
        <rect x="22" y="100" width="6" height="14" fill="{DARK}" opacity="0.7"/>
        <rect x="412" y="60" width="6" height="14" fill="{DARK}" opacity="0.7"/>
        <rect x="424" y="60" width="6" height="14" fill="{DARK}" opacity="0.7"/>
        <rect x="412" y="100" width="6" height="14" fill="{DARK}" opacity="0.7"/>
        <rect x="424" y="100" width="6" height="14" fill="{DARK}" opacity="0.7"/>
        <rect x="210" y="20" width="6" height="14" fill="{DARK}" opacity="0.7"/>
        <rect x="222" y="20" width="6" height="14" fill="{DARK}" opacity="0.7"/>
        <rect x="210" y="60" width="6" height="14" fill="{DARK}" opacity="0.7"/>
        <rect x="222" y="60" width="6" height="14" fill="{DARK}" opacity="0.7"/>
        <!-- Gateway -->
        <path d="M 200 200 L 200 160 q 20 -25 40 0 L 240 200 Z" fill="{DARK}" opacity="0.7"/>
      </g>

      <!-- Ground -->
      <rect x="0" y="370" width="1200" height="10" fill="{FOREST_LT}" opacity="0.4"/>
    </svg>
    '''


def render_minsk_skyline() -> str:
    """
    Header banner for Unit 0 — Minsk skyline silhouette featuring the
    National Library (rhombicuboctahedron) as the iconic anchor.
    """
    return f'''
    <svg viewBox="0 0 1200 220" xmlns="http://www.w3.org/2000/svg" width="100%" style="max-height: 220px; display: block;">
      <defs>
        <linearGradient id="msk-sky" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="{SKY_TOP}"/>
          <stop offset="100%" stop-color="#e8d8c0"/>
        </linearGradient>
      </defs>
      <rect width="1200" height="220" fill="url(#msk-sky)"/>

      <!-- Distant buildings (back layer, lighter) -->
      <g fill="{STONE}" opacity="0.45">
        <rect x="0" y="160" width="80" height="60"/>
        <rect x="80" y="140" width="60" height="80"/>
        <rect x="140" y="155" width="50" height="65"/>
        <rect x="900" y="150" width="70" height="70"/>
        <rect x="970" y="135" width="55" height="85"/>
        <rect x="1100" y="155" width="100" height="65"/>
      </g>

      <!-- Mid-range Soviet-era apartment blocks -->
      <g fill="{STONE}" opacity="0.7" stroke="{DARK}" stroke-width="1">
        <rect x="180" y="120" width="90" height="100"/>
        <rect x="280" y="135" width="70" height="85"/>
        <rect x="360" y="115" width="100" height="105"/>
        <rect x="800" y="125" width="80" height="95"/>
        <rect x="890" y="140" width="70" height="80"/>
        <rect x="990" y="120" width="100" height="100"/>
      </g>

      <!-- Window grids on apartment blocks -->
      <g fill="{SUN}" opacity="0.6">
        <!-- block 1 -->
        <rect x="190" y="135" width="6" height="8"/>
        <rect x="206" y="135" width="6" height="8"/>
        <rect x="222" y="135" width="6" height="8"/>
        <rect x="238" y="135" width="6" height="8"/>
        <rect x="254" y="135" width="6" height="8"/>
        <rect x="190" y="155" width="6" height="8"/>
        <rect x="222" y="155" width="6" height="8"/>
        <rect x="254" y="155" width="6" height="8"/>
        <rect x="190" y="175" width="6" height="8"/>
        <rect x="206" y="175" width="6" height="8"/>
        <rect x="238" y="175" width="6" height="8"/>
        <!-- block 2 -->
        <rect x="370" y="130" width="7" height="9"/>
        <rect x="390" y="130" width="7" height="9"/>
        <rect x="410" y="130" width="7" height="9"/>
        <rect x="430" y="130" width="7" height="9"/>
        <rect x="370" y="155" width="7" height="9"/>
        <rect x="410" y="155" width="7" height="9"/>
        <rect x="430" y="155" width="7" height="9"/>
        <rect x="390" y="180" width="7" height="9"/>
        <rect x="430" y="180" width="7" height="9"/>
        <!-- block 3 -->
        <rect x="1000" y="135" width="7" height="9"/>
        <rect x="1020" y="135" width="7" height="9"/>
        <rect x="1040" y="135" width="7" height="9"/>
        <rect x="1060" y="135" width="7" height="9"/>
        <rect x="1000" y="160" width="7" height="9"/>
        <rect x="1040" y="160" width="7" height="9"/>
        <rect x="1060" y="160" width="7" height="9"/>
      </g>

      <!-- National Library — rhombicuboctahedron (iconic Minsk) -->
      <g transform="translate(540, 80)">
        <!-- top -->
        <polygon points="60,0 100,20 60,40 20,20" fill="{STONE}" stroke="{DARK}" stroke-width="1.5"/>
        <!-- middle band -->
        <polygon points="0,40 40,60 80,40 120,60 80,80 40,60 0,80 -20,60" fill="{STONE}" opacity="0.85" stroke="{DARK}" stroke-width="1.5"/>
        <!-- main body (square front + sides) -->
        <polygon points="20,60 100,60 100,140 20,140" fill="{STONE}" stroke="{DARK}" stroke-width="1.5"/>
        <polygon points="100,60 120,80 120,130 100,140" fill="{STONE}" opacity="0.7" stroke="{DARK}" stroke-width="1.5"/>
        <polygon points="20,60 0,80 0,130 20,140" fill="{STONE}" opacity="0.85" stroke="{DARK}" stroke-width="1.5"/>
        <!-- diamond cuts (visual texture) -->
        <line x1="60" y1="60" x2="60" y2="140" stroke="{DARK}" stroke-width="0.8" opacity="0.4"/>
        <line x1="40" y1="80" x2="80" y2="80" stroke="{DARK}" stroke-width="0.8" opacity="0.4"/>
        <line x1="40" y1="100" x2="80" y2="100" stroke="{DARK}" stroke-width="0.8" opacity="0.4"/>
        <line x1="40" y1="120" x2="80" y2="120" stroke="{DARK}" stroke-width="0.8" opacity="0.4"/>
        <!-- lit windows -->
        <rect x="44" y="84" width="6" height="8" fill="{SUN}" opacity="0.7"/>
        <rect x="68" y="84" width="6" height="8" fill="{SUN}" opacity="0.7"/>
        <rect x="44" y="104" width="6" height="8" fill="{SUN}" opacity="0.7"/>
        <rect x="68" y="124" width="6" height="8" fill="{SUN}" opacity="0.7"/>
        <!-- base -->
        <rect x="-20" y="140" width="160" height="10" fill="{STONE}" stroke="{DARK}" stroke-width="1.5"/>
      </g>

      <!-- Ground -->
      <rect x="0" y="218" width="1200" height="2" fill="{DARK}" opacity="0.3"/>
    </svg>
    '''


def render_bialowieza_scene() -> str:
    """
    Header banner for Basic Phrases — Białowieża forest with a zubr
    in the foreground and a busel (white stork) flying overhead.
    """
    return f'''
    <svg viewBox="0 0 1200 240" xmlns="http://www.w3.org/2000/svg" width="100%" style="max-height: 240px; display: block;">
      <defs>
        <linearGradient id="forest-sky" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#dfe9d8"/>
          <stop offset="100%" stop-color="#f4ead8"/>
        </linearGradient>
      </defs>
      <rect width="1200" height="240" fill="url(#forest-sky)"/>

      <!-- Distant pines (back layer) -->
      <g fill="{FOREST}" opacity="0.4">
        <polygon points="50,200 70,120 90,200"/>
        <polygon points="100,200 125,100 150,200"/>
        <polygon points="160,200 180,130 200,200"/>
        <polygon points="220,200 245,110 270,200"/>
        <polygon points="290,200 310,125 330,200"/>
        <polygon points="900,200 920,135 940,200"/>
        <polygon points="950,200 975,115 1000,200"/>
        <polygon points="1020,200 1040,130 1060,200"/>
        <polygon points="1080,200 1105,105 1130,200"/>
        <polygon points="1150,200 1170,130 1190,200"/>
      </g>

      <!-- Mid-layer pines (more saturated) -->
      <g fill="{FOREST}" opacity="0.85">
        <polygon points="0,210 30,90 60,210"/>
        <polygon points="80,210 115,70 150,210"/>
        <polygon points="180,210 215,80 250,210"/>
        <polygon points="280,210 315,75 350,210"/>
        <polygon points="850,210 885,80 920,210"/>
        <polygon points="940,210 975,70 1010,210"/>
        <polygon points="1040,210 1075,90 1110,210"/>
        <polygon points="1140,210 1175,80 1210,210"/>
      </g>

      <!-- Deciduous tree clumps -->
      <g fill="{FOREST_LT}" opacity="0.85">
        <ellipse cx="380" cy="170" rx="50" ry="40"/>
        <ellipse cx="430" cy="180" rx="40" ry="30"/>
        <ellipse cx="780" cy="175" rx="48" ry="38"/>
        <ellipse cx="820" cy="182" rx="35" ry="28"/>
      </g>
      <g fill="{DARK}" opacity="0.6">
        <rect x="395" y="190" width="8" height="25"/>
        <rect x="425" y="195" width="6" height="20"/>
        <rect x="790" y="195" width="8" height="25"/>
      </g>

      <!-- Busel (white stork) — flying silhouette -->
      <g transform="translate(720, 60)">
        <!-- body -->
        <ellipse cx="0" cy="0" rx="22" ry="6" fill="white" stroke="{DARK}" stroke-width="1.5"/>
        <!-- wings (V shape, in flight) -->
        <path d="M -10 -3 q -25 -18 -45 -10 q 18 4 35 7" fill="white" stroke="{DARK}" stroke-width="1.5"/>
        <path d="M 10 -3 q 25 -18 45 -10 q -18 4 -35 7" fill="white" stroke="{DARK}" stroke-width="1.5"/>
        <!-- wing tips (black) -->
        <path d="M -55 -13 q 8 0 15 4" fill="{DARK}" stroke="{DARK}" stroke-width="2"/>
        <path d="M 55 -13 q -8 0 -15 4" fill="{DARK}" stroke="{DARK}" stroke-width="2"/>
        <!-- neck and head -->
        <path d="M 22 -2 q 12 -2 18 -8 q 6 -2 12 0" fill="white" stroke="{DARK}" stroke-width="1.5"/>
        <!-- beak (long, red) -->
        <path d="M 52 -10 l 14 -2" stroke="{RED}" stroke-width="3" stroke-linecap="round"/>
        <!-- eye -->
        <circle cx="48" cy="-8" r="1" fill="{DARK}"/>
        <!-- legs trailing -->
        <line x1="-5" y1="5" x2="-15" y2="20" stroke="{RED}" stroke-width="1.5"/>
        <line x1="0" y1="5" x2="-10" y2="22" stroke="{RED}" stroke-width="1.5"/>
      </g>

      <!-- ZUBR (European bison) — foreground hero, side profile -->
      <g transform="translate(480, 130)">
        <!-- body, with prominent forequarters and hump -->
        <path d="M 30 30
                 q 0 -10 8 -16
                 q 8 -8 25 -10
                 q 30 -3 50 5
                 q 25 8 32 25
                 q 5 12 0 22
                 l -10 10
                 l 5 28
                 l -8 0
                 l -5 -25
                 l -50 0
                 l -5 25
                 l -8 0
                 l 5 -25
                 l -25 0
                 z"
              fill="{DARK}" stroke="{DARK}" stroke-width="1"/>
        <!-- shaggy mane texture on chest/head -->
        <path d="M 28 18 q 5 -5 10 -2 q -3 5 -8 6" fill="{DARK}"/>
        <path d="M 32 25 q 5 -5 12 -2 q -4 6 -10 7" fill="#1a1a1a"/>
        <!-- head/horn -->
        <path d="M 25 32 q -5 -8 0 -14 q 8 -4 14 0" fill="{DARK}"/>
        <!-- horn (curved) -->
        <path d="M 28 18 q -2 -6 4 -8 q 4 0 4 4" stroke="{SKIN}" stroke-width="1.5" fill="none" stroke-linecap="round"/>
        <!-- eye -->
        <circle cx="32" cy="28" r="1.2" fill="white"/>
        <!-- nose / muzzle -->
        <ellipse cx="22" cy="36" rx="3" ry="2" fill="#1a1a1a"/>
        <!-- beard (under chin) -->
        <path d="M 25 40 q -2 6 2 10 q 4 -3 5 -8" fill="{DARK}"/>
        <!-- tail -->
        <line x1="148" y1="35" x2="158" y2="42" stroke="{DARK}" stroke-width="3" stroke-linecap="round"/>
        <circle cx="158" cy="42" r="3" fill="{DARK}"/>
      </g>

      <!-- Foreground grass tufts -->
      <g fill="{FOREST_LT}" opacity="0.8">
        <path d="M 100 220 l 4 -10 l 3 8 l 3 -10 l 4 12 z"/>
        <path d="M 400 225 l 4 -8 l 3 6 l 3 -8 l 4 10 z"/>
        <path d="M 880 222 l 4 -10 l 3 8 l 3 -10 l 4 12 z"/>
        <path d="M 1100 225 l 4 -8 l 3 6 l 3 -8 l 4 10 z"/>
      </g>

      <!-- Ground line -->
      <line x1="0" y1="225" x2="1200" y2="225" stroke="{DARK}" stroke-width="1" opacity="0.4"/>
    </svg>
    '''


def render_scenario_background(scenario_key: str) -> str:
    """
    Compact per-scenario header for the Conversation Partner active view.
    Three scenes: Hrodna market, Minsk café, Strochitsy / Kupalle.
    """
    if scenario_key == "hrodna_market":
        return f'''
        <svg viewBox="0 0 1200 140" xmlns="http://www.w3.org/2000/svg" width="100%" style="max-height: 140px; display: block;">
          <rect width="1200" height="140" fill="#f4e8d4"/>
          <!-- Old town silhouettes (Hrodna) — gabled roofs, church spire -->
          <g fill="{STONE}" opacity="0.55">
            <rect x="0" y="80" width="80" height="60"/>
            <rect x="80" y="70" width="60" height="70"/>
            <polygon points="100,70 110,55 120,70"/>
            <rect x="140" y="75" width="50" height="65"/>
            <rect x="900" y="80" width="60" height="60"/>
            <rect x="960" y="70" width="80" height="70"/>
            <rect x="1040" y="85" width="60" height="55"/>
            <rect x="1100" y="75" width="50" height="65"/>
          </g>
          <!-- Church / castle silhouette -->
          <g fill="{BRICK}" opacity="0.65" stroke="{DARK}" stroke-width="1">
            <rect x="500" y="60" width="200" height="80"/>
            <polygon points="500,60 540,30 580,60"/>
            <polygon points="600,60 640,20 680,60"/>
            <rect x="528" y="75" width="14" height="20" fill="{DARK}" opacity="0.6"/>
            <rect x="556" y="75" width="14" height="20" fill="{DARK}" opacity="0.6"/>
            <rect x="628" y="75" width="14" height="20" fill="{DARK}" opacity="0.6"/>
            <rect x="656" y="75" width="14" height="20" fill="{DARK}" opacity="0.6"/>
          </g>
          <!-- Market awnings — striped tents -->
          <g>
            <polygon points="220,100 280,100 250,75" fill="{RED}" opacity="0.75"/>
            <polygon points="290,100 350,100 320,75" fill="white" stroke="{DARK}" stroke-width="1" opacity="0.85"/>
            <polygon points="360,100 420,100 390,75" fill="{RED}" opacity="0.75"/>
            <rect x="225" y="100" width="55" height="40" fill="#a86a2c" opacity="0.7"/>
            <rect x="295" y="100" width="55" height="40" fill="#a86a2c" opacity="0.7"/>
            <rect x="365" y="100" width="55" height="40" fill="#a86a2c" opacity="0.7"/>
          </g>
          <line x1="0" y1="138" x2="1200" y2="138" stroke="{DARK}" stroke-width="1" opacity="0.4"/>
        </svg>
        '''
    elif scenario_key == "minsk_cafe":
        return f'''
        <svg viewBox="0 0 1200 140" xmlns="http://www.w3.org/2000/svg" width="100%" style="max-height: 140px; display: block;">
          <rect width="1200" height="140" fill="#ede4d3"/>
          <!-- Urban modern blocks -->
          <g fill="{STONE}" opacity="0.65" stroke="{DARK}" stroke-width="1">
            <rect x="0" y="40" width="180" height="100"/>
            <rect x="180" y="60" width="120" height="80"/>
            <rect x="900" y="50" width="160" height="90"/>
            <rect x="1060" y="65" width="140" height="75"/>
          </g>
          <!-- Window grids -->
          <g fill="{SUN}" opacity="0.6">
            <rect x="20" y="60" width="6" height="9"/><rect x="36" y="60" width="6" height="9"/>
            <rect x="52" y="60" width="6" height="9"/><rect x="68" y="60" width="6" height="9"/>
            <rect x="84" y="60" width="6" height="9"/><rect x="100" y="60" width="6" height="9"/>
            <rect x="20" y="85" width="6" height="9"/><rect x="52" y="85" width="6" height="9"/>
            <rect x="84" y="85" width="6" height="9"/><rect x="116" y="85" width="6" height="9"/>
            <rect x="20" y="110" width="6" height="9"/><rect x="36" y="110" width="6" height="9"/>
            <rect x="68" y="110" width="6" height="9"/><rect x="100" y="110" width="6" height="9"/>
            <rect x="920" y="70" width="6" height="9"/><rect x="940" y="70" width="6" height="9"/>
            <rect x="960" y="70" width="6" height="9"/><rect x="990" y="70" width="6" height="9"/>
            <rect x="920" y="100" width="6" height="9"/><rect x="960" y="100" width="6" height="9"/>
            <rect x="990" y="100" width="6" height="9"/><rect x="1020" y="100" width="6" height="9"/>
          </g>
          <!-- Café front center: striped awning + small tables -->
          <g transform="translate(450, 60)">
            <rect x="0" y="0" width="300" height="80" fill="white" stroke="{DARK}" stroke-width="1.5"/>
            <!-- Awning -->
            <rect x="-10" y="-15" width="320" height="20" fill="{RED}" stroke="{DARK}" stroke-width="1"/>
            <line x1="20" y1="-15" x2="20" y2="5" stroke="white" stroke-width="2"/>
            <line x1="60" y1="-15" x2="60" y2="5" stroke="white" stroke-width="2"/>
            <line x1="100" y1="-15" x2="100" y2="5" stroke="white" stroke-width="2"/>
            <line x1="140" y1="-15" x2="140" y2="5" stroke="white" stroke-width="2"/>
            <line x1="180" y1="-15" x2="180" y2="5" stroke="white" stroke-width="2"/>
            <line x1="220" y1="-15" x2="220" y2="5" stroke="white" stroke-width="2"/>
            <line x1="260" y1="-15" x2="260" y2="5" stroke="white" stroke-width="2"/>
            <line x1="300" y1="-15" x2="300" y2="5" stroke="white" stroke-width="2"/>
            <!-- Door -->
            <rect x="135" y="30" width="30" height="50" fill="{BOOT_BROWN}" opacity="0.8"/>
            <!-- Window -->
            <rect x="20" y="20" width="80" height="35" fill="{SKY_TOP}" stroke="{DARK}" stroke-width="1" opacity="0.7"/>
            <rect x="200" y="20" width="80" height="35" fill="{SKY_TOP}" stroke="{DARK}" stroke-width="1" opacity="0.7"/>
            <!-- Sign -->
            <text x="150" y="14" font-family="serif" font-size="9" fill="white" text-anchor="middle" font-style="italic">Кавярня</text>
            <!-- Outdoor table & chairs -->
            <circle cx="-30" cy="105" r="10" fill="{BOOT_BROWN}" stroke="{DARK}" stroke-width="1"/>
            <line x1="-30" y1="105" x2="-30" y2="135" stroke="{DARK}" stroke-width="1.5"/>
            <circle cx="335" cy="105" r="10" fill="{BOOT_BROWN}" stroke="{DARK}" stroke-width="1"/>
            <line x1="335" y1="105" x2="335" y2="135" stroke="{DARK}" stroke-width="1.5"/>
          </g>
          <line x1="0" y1="138" x2="1200" y2="138" stroke="{DARK}" stroke-width="1" opacity="0.4"/>
        </svg>
        '''
    elif scenario_key == "strochitsy_kupalle":
        return f'''
        <svg viewBox="0 0 1200 140" xmlns="http://www.w3.org/2000/svg" width="100%" style="max-height: 140px; display: block;">
          <defs>
            <linearGradient id="kup-sky" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stop-color="#3a3a5a"/>
              <stop offset="100%" stop-color="#a85a3a"/>
            </linearGradient>
          </defs>
          <rect width="1200" height="140" fill="url(#kup-sky)"/>
          <!-- Stars -->
          <g fill="white" opacity="0.7">
            <circle cx="80" cy="20" r="1"/>
            <circle cx="200" cy="35" r="1"/>
            <circle cx="320" cy="15" r="1.2"/>
            <circle cx="450" cy="30" r="1"/>
            <circle cx="900" cy="20" r="1"/>
            <circle cx="1050" cy="35" r="1.2"/>
            <circle cx="1150" cy="15" r="1"/>
          </g>
          <!-- Distant trees -->
          <g fill="{DARK}" opacity="0.7">
            <polygon points="0,140 30,80 60,140"/>
            <polygon points="60,140 90,70 120,140"/>
            <polygon points="120,140 150,75 180,140"/>
            <polygon points="1000,140 1030,80 1060,140"/>
            <polygon points="1060,140 1090,70 1120,140"/>
            <polygon points="1120,140 1150,75 1180,140"/>
          </g>
          <!-- Wooden hut (traditional хата) -->
          <g transform="translate(220, 70)">
            <rect x="0" y="20" width="120" height="50" fill="#7a4828" stroke="{DARK}" stroke-width="1"/>
            <polygon points="-10,20 60,-15 130,20" fill="#5a2818" stroke="{DARK}" stroke-width="1"/>
            <rect x="20" y="35" width="20" height="20" fill="{SUN}" opacity="0.8"/>
            <rect x="80" y="35" width="20" height="20" fill="{SUN}" opacity="0.8"/>
            <rect x="50" y="40" width="20" height="30" fill="{DARK}" opacity="0.7"/>
          </g>
          <!-- Bonfire (Kupalle is the fire-jumping festival!) -->
          <g transform="translate(620, 100)">
            <!-- Logs -->
            <line x1="-20" y1="35" x2="20" y2="35" stroke="{BOOT_BROWN}" stroke-width="6"/>
            <line x1="-15" y1="40" x2="15" y2="40" stroke="#5a2818" stroke-width="6"/>
            <!-- Flames -->
            <path d="M -15 35 q 5 -25 0 -35 q 8 5 5 25 q 8 -15 12 -28 q 4 12 -2 30 q 8 -12 14 -25 q 2 18 -4 28 q 6 -8 12 -18 q 0 14 -8 23 z"
                  fill="{SUN}" opacity="0.9"/>
            <path d="M -10 35 q 4 -20 0 -28 q 6 4 4 20 q 6 -10 8 -20 q 2 8 -1 22 z"
                  fill="{RED}" opacity="0.85"/>
          </g>
          <!-- Floating flower wreaths on water (Kupalle tradition) -->
          <g transform="translate(820, 115)">
            <ellipse cx="0" cy="0" rx="20" ry="6" fill="none" stroke="{FOREST_LT}" stroke-width="2"/>
            <circle cx="-15" cy="-2" r="3" fill="white"/>
            <circle cx="-8" cy="2" r="3" fill="{RED}" opacity="0.7"/>
            <circle cx="2" cy="-2" r="3" fill="white"/>
            <circle cx="12" cy="2" r="3" fill="{BERRY}"/>
            <circle cx="-15" cy="-2" r="1" fill="{BERRY}"/>
            <circle cx="2" cy="-2" r="1" fill="{BERRY}"/>
          </g>
          <g transform="translate(900, 125)">
            <ellipse cx="0" cy="0" rx="18" ry="5" fill="none" stroke="{FOREST_LT}" stroke-width="2"/>
            <circle cx="-12" cy="-1" r="2.5" fill="white"/>
            <circle cx="-4" cy="1" r="2.5" fill="{RED}" opacity="0.7"/>
            <circle cx="6" cy="-1" r="2.5" fill="white"/>
            <circle cx="13" cy="1" r="2.5" fill="{BERRY}"/>
          </g>
          <!-- Water suggestion -->
          <line x1="780" y1="115" x2="950" y2="115" stroke="white" stroke-width="0.5" opacity="0.4"/>
          <line x1="790" y1="125" x2="940" y2="125" stroke="white" stroke-width="0.5" opacity="0.3"/>
        </svg>
        '''
    else:
        return ""
