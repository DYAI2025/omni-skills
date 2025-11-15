"""
server.py – FastAPI Server für Marker Annotation

Stellt /annotate-Endpoint bereit, der Texte + SIT nimmt, 
marker-engine-rl aufruft und Annotation-Response zurückgibt.
"""

import os
import sys
import json
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Marker-Engine importieren
ENGINE_DIR = Path(__file__).parent.parent.parent.parent / "marker-engine-rl"
sys.path.insert(0, str(ENGINE_DIR / "scripts" / "python"))

try:
    from engine import MarkerEngine
    from adapter import events_to_annotation_response
except ImportError as e:
    print(f"❌ Fehler beim Import: {e}")
    print(f"   Prüfe, ob marker-engine-rl/scripts/python/ existiert")
    sys.exit(1)

app = FastAPI(title="Marker Annotator API", version="1.0.0")

# CORS aktivieren (für Chrome Extension)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnnotateRequest(BaseModel):
    """Request-Body für /annotate Endpoint."""
    texts: list[str] = Field(..., min_items=1, description="Liste von Texten")
    sit: float = Field(0.5, ge=0.0, le=1.0, description="SIT-Wert (0.0–1.0)")


class AnnotateResponse(BaseModel):
    """Response-Body für /annotate Endpoint."""
    sit: float
    annotations: list[dict[str, Any]]
    clusters: list[dict[str, Any]]
    rf_context: dict[str, Any]
    post_analysis: dict[str, Any]
    telemetry: dict[str, Any]


@app.post("/annotate", response_model=AnnotateResponse)
def annotate(request: AnnotateRequest):
    """
    Annotiert Texte mit Markern.
    
    Args:
        request: AnnotateRequest mit texts und sit
    
    Returns:
        AnnotateResponse mit spans, clusters, telemetry
    
    Raises:
        HTTPException: Bei Engine-Fehlern
    """
    try:
        # Marker-Engine initialisieren
        engine = MarkerEngine()
        
        # Events sammeln
        all_events = []
        for msg_idx, text in enumerate(request.texts):
            events = engine.detect_markers(
                text, 
                msg_index=msg_idx, 
                sit=request.sit
            )
            all_events.extend(events)
        
        # Zu Annotation-Response konvertieren
        response = events_to_annotation_response(
            all_events, 
            request.texts, 
            request.sit
        )
        
        return response
    
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Engine-Fehler: {str(e)}"
        )


@app.get("/health")
def health():
    """Health-Check Endpoint."""
    return {"status": "ok", "service": "marker-annotator"}


@app.get("/")
def root():
    """Root Endpoint mit API-Info."""
    return {
        "service": "Marker Annotator API",
        "version": "1.0.0",
        "endpoints": {
            "POST /annotate": "Annotiert Texte mit Markern",
            "GET /health": "Health-Check",
            "GET /docs": "API-Dokumentation (Swagger UI)"
        }
    }


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", "8642"))
    host = os.getenv("HOST", "127.0.0.1")
    
    print(f"🚀 Starting Marker Annotator Server on {host}:{port}")
    print(f"   Swagger UI: http://{host}:{port}/docs")
    print(f"   Health: http://{host}:{port}/health")
    
    uvicorn.run(app, host=host, port=port)
