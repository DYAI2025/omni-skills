"""
adapter.py – Konvertiert Engine-Events zu Annotation-Spans

Nimmt die NDJSON-Events vom marker-engine-rl und wandelt sie in 
Span-basierte Annotationen (msgIndex, start, end) für den 
Chrome-Extension-Visualizer um.
"""

import json
from typing import Any


def convert_events_to_spans(
    events: list[dict[str, Any]], 
    texts: list[str]
) -> list[dict[str, Any]]:
    """
    Konvertiert Engine-Events zu Annotation-Spans.
    
    Args:
        events: Liste von Events aus marker-engine-rl (NDJSON Format)
        texts: Original-Texte (für Längenvalidierung)
    
    Returns:
        Liste von Spans mit {msgIndex, start, end, level, id, color}
    """
    spans = []
    
    for event in events:
        level = event.get("level", "").upper()
        marker_id = event.get("marker_id", "")
        msg_index = event.get("msg_index", 0)
        
        # Range extrahieren
        range_data = event.get("range", {})
        start = range_data.get("start", 0)
        end = range_data.get("end", 0)
        
        # Validierung
        if not level or not marker_id:
            continue
        if start < 0 or end <= start:
            continue
        if msg_index < 0 or msg_index >= len(texts):
            continue
        if end > len(texts[msg_index]):
            continue
        
        # Span erstellen
        span = {
            "msgIndex": msg_index,
            "start": start,
            "end": end,
            "level": level,
            "id": marker_id,
            "color": None  # Wird client-side gesetzt
        }
        
        spans.append(span)
    
    return spans


def build_clusters(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Extrahiert Cluster-Informationen aus MEMA/CLU-Events.
    
    Args:
        events: Liste von Events aus marker-engine-rl
    
    Returns:
        Liste von Cluster-Dicts mit {level, members, ars}
    """
    clusters = []
    
    for event in events:
        level = event.get("level", "").upper()
        
        if level not in ["CLU", "MEMA"]:
            continue
        
        members = event.get("composition", {}).get("members", [])
        ars = event.get("ars", None)
        
        cluster = {
            "level": level,
            "members": members,
            "ars": ars
        }
        
        clusters.append(cluster)
    
    return clusters


def extract_rf_context(events: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Extrahiert RF-Manifestation-Kontext (STUFE × TYP × ZEIT × INT).
    
    Args:
        events: Liste von Events aus marker-engine-rl
    
    Returns:
        Dict mit {stufe, typ, zeit, intensität}
    """
    rf_context = {
        "stufe": None,
        "typ": None,
        "zeit": None,
        "intensität": None
    }
    
    # Suche nach RF-Manifestation in Events
    for event in events:
        rf = event.get("rf_manifestation", {})
        if rf:
            rf_context["stufe"] = rf.get("stufe")
            rf_context["typ"] = rf.get("typ")
            rf_context["zeit"] = rf.get("zeit")
            rf_context["intensität"] = rf.get("intensität")
            break  # Erste RF-Manifestation verwenden
    
    return rf_context


def build_telemetry(events: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Erstellt Telemetrie-Daten aus Events.
    
    Args:
        events: Liste von Events aus marker-engine-rl
    
    Returns:
        Dict mit {total_markers, by_level, novel_filtered, violations}
    """
    telemetry = {
        "total_markers": len(events),
        "by_level": {"ATO": 0, "SEM": 0, "CLU": 0, "MEMA": 0},
        "novel_filtered": 0,
        "violations": []
    }
    
    for event in events:
        level = event.get("level", "").upper()
        if level in telemetry["by_level"]:
            telemetry["by_level"][level] += 1
        
        # Novel-Marker zählen
        if event.get("is_novel", False):
            telemetry["novel_filtered"] += 1
        
        # Violations sammeln
        violations = event.get("violations", [])
        telemetry["violations"].extend(violations)
    
    return telemetry


def events_to_annotation_response(
    events: list[dict[str, Any]], 
    texts: list[str], 
    sit: float
) -> dict[str, Any]:
    """
    Komplette Konvertierung von Engine-Events zu Annotation-Response.
    
    Args:
        events: Liste von Events aus marker-engine-rl
        texts: Original-Texte
        sit: SIT-Wert (0.0–1.0)
    
    Returns:
        Vollständiges Annotation-Response-Dict gemäß annotation-schema.json
    """
    return {
        "sit": sit,
        "annotations": convert_events_to_spans(events, texts),
        "clusters": build_clusters(events),
        "rf_context": extract_rf_context(events),
        "post_analysis": {
            "novel_candidates": []
        },
        "telemetry": build_telemetry(events)
    }
