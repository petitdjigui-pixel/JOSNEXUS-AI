from pathlib import Path
from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field


# Configuration générale
BASE_DIR = Path(__file__).resolve().parents[2]
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI(
    title="JOSNEXUS AI",
    description="Plateforme intelligente multisectorielle",
    version="1.0.0"
)

# Configuration temporaire pour le développement
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Modules de la plateforme
MODULES = [
    {
        "id": "finance",
        "name": "NEXUS FINANCE",
        "description": "Analyse des marchés financiers et des tendances.",
        "status": "development"
    },
    {
        "id": "sport",
        "name": "NEXUS SPORT",
        "description": "Analyse des statistiques et compétitions sportives.",
        "status": "development"
    },
    {
        "id": "economy",
        "name": "NEXUS ECONOMY",
        "description": "Analyse économique et financière mondiale.",
        "status": "development"
    },
    {
        "id": "commerce",
        "name": "NEXUS COMMERCE",
        "description": "Analyse des produits, prix et opportunités commerciales.",
        "status": "development"
    },
    {
        "id": "news",
        "name": "NEXUS NEWS",
        "description": "Analyse des actualités et événements.",
        "status": "development"
    },
    {
        "id": "discovery",
        "name": "NEXUS DISCOVERY",
        "description": "Détection de tendances et relations entre domaines.",
        "status": "development"
    },
    {
        "id": "brain",
        "name": "NEXUS BRAIN",
        "description": "Moteur central de coordination et d'analyse.",
        "status": "development"
    }
]


# Modèle de demande d'analyse
class DiscoveryRequest(BaseModel):
    question: str = Field(min_length=3, max_length=1000)
    domain: str = Field(default="general", max_length=50)


# Page d'accueil
@app.get("/")
def home():
    index_file = FRONTEND_DIR / "index.html"

    if index_file.exists():
        return FileResponse(index_file)

    return {
        "name": "JOSNEXUS AI",
        "version": "1.0.0",
        "message": "Le moteur JOSNEXUS AI fonctionne."
    }


# Vérifier le fonctionnement du serveur
@app.get("/api/health")
def health():
    return {
        "success": True,
        "project": "JOSNEXUS AI",
        "status": "online",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


# Obtenir les modules
@app.get("/api/modules")
def get_modules():
    return {
        "success": True,
        "total": len(MODULES),
        "modules": MODULES
    }


# Vue générale
@app.get("/api/overview")
def overview():
    return {
        "success": True,
        "project": "JOSNEXUS AI",
        "version": "1.0.0",
        "modules": len(MODULES),
        "status": "development",
        "message": "La plateforme est en construction."
    }


# Première interface de découverte
@app.post("/api/discovery")
def discovery(request: DiscoveryRequest):
    return {
        "success": True,
        "domain": request.domain,
        "question": request.question,
        "status": "demo",
        "analysis": (
            "Le système a reçu votre demande. "
            "Les sources de données réelles et le moteur IA "
            "ne sont pas encore connectés."
        ),
        "sources": [],
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


# Servir les fichiers de l'interface web
if FRONTEND_DIR.exists():
    app.mount(
        "/static",
        StaticFiles(directory=str(FRONTEND_DIR)),
        name="static"
  )
  
