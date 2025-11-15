"""
colors.py – Color Mapping für Marker Annotator

Definiert die Farbpaletten für Light- und Dark-Mode gemäß 
color-palette.md und stellt Utility-Funktionen bereit.
"""

LIGHT_COLORS = {
    "ATO": "#7c3aed",
    "SEM": "#0ea5e9",
    "CLU": "#f59e0b",
    "MEMA": "#ef4444"
}

DARK_COLORS = {
    "ATO": "#a78bfa",
    "SEM": "#67e8f9",
    "CLU": "#fbbf24",
    "MEMA": "#f87171"
}

FALLBACK_COLOR_LIGHT = "#64748b"
FALLBACK_COLOR_DARK = "#94a3b8"


def color_for(level: str, dark_mode: bool = False) -> str:
    """
    Gibt die Farbe für einen Marker-Level zurück.
    
    Args:
        level: Marker-Level (ATO, SEM, CLU, MEMA)
        dark_mode: Wenn True, Dark-Mode-Farbe verwenden
    
    Returns:
        Hex-Farbe (z.B. "#7c3aed")
    """
    palette = DARK_COLORS if dark_mode else LIGHT_COLORS
    return palette.get(level, 
                      FALLBACK_COLOR_DARK if dark_mode 
                      else FALLBACK_COLOR_LIGHT)


def alpha_for(dark_mode: bool = False) -> float:
    """
    Gibt die empfohlene Alpha-Deckkraft für Highlights zurück.
    
    Args:
        dark_mode: Wenn True, Dark-Mode-Alpha verwenden
    
    Returns:
        Alpha-Wert zwischen 0.0 und 1.0
    """
    return 0.46 if dark_mode else 0.32


def rgba_for(level: str, dark_mode: bool = False) -> str:
    """
    Gibt die RGBA-Farbe (mit Alpha) für einen Marker zurück.
    
    Args:
        level: Marker-Level (ATO, SEM, CLU, MEMA)
        dark_mode: Wenn True, Dark-Mode-Farbe verwenden
    
    Returns:
        RGBA-String (z.B. "rgba(124, 58, 237, 0.32)")
    """
    hex_color = color_for(level, dark_mode)
    alpha = alpha_for(dark_mode)
    
    # Hex zu RGB konvertieren
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    
    return f"rgba({r}, {g}, {b}, {alpha})"


def all_colors(dark_mode: bool = False) -> dict[str, str]:
    """
    Gibt alle Farben für den angegebenen Modus zurück.
    
    Args:
        dark_mode: Wenn True, Dark-Mode-Farben zurückgeben
    
    Returns:
        Dictionary mit Level → Hex-Farbe
    """
    return DARK_COLORS.copy() if dark_mode else LIGHT_COLORS.copy()


def validate_level(level: str) -> bool:
    """
    Prüft, ob ein Level-String valide ist.
    
    Args:
        level: Zu prüfender Level-String
    
    Returns:
        True wenn valide (ATO, SEM, CLU, MEMA)
    """
    return level in LIGHT_COLORS
