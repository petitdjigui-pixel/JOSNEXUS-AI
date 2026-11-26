
import os
from pathlib import Path
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from google import genai


# ==================================================
# JOSNEXUS AI - CONFIGURATION GENERALE
# ==================================================

BASE_DIR = Path(__file__).resolve().parents[2]
FRONTEND_DIR = BASE_DIR / "frontend"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.5-flash-lite"
)

app = FastAPI(
    title="JOSNEXUS AI",
    description="Intelligence artificielle multisectorielle",
    version="1.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================================================
# NEXUS MODULES
# ==================================================

MODULES = [
    {
        "id": "finance",
        "name": "NEXUS FINANCE",
        "description": "Analyse financière et marchés."
    },
    {
        "id": "sport",
        "name": "NEXUS SPORT",
        "description": "Analyse des compétitions sportives."
    },
    {
        "id": "economy",
        "name": "NEXUS ECONOMY",
        "description": "Analyse de l'économie mondiale."
    },
    {
        "id": "commerce",
        "name": "NEXUS COMMERCE",
        "description": "Analyse commerciale et opportunités."
    },
    {
        "id": "news",
        "name": "NEXUS NEWS",
        "description": "Compréhension des actualités."
    },
    {
        "id": "discovery",
        "name": "NEXUS DISCOVERY",
        "description": "Détection de tendances."
    },
    {
        "id": "brain",
        "name": "NEXUS BRAIN",
        "description": "Moteur central d'intelligence."
    }
]


# ==================================================
# MODELE DE REQUETE
# ==================================================

class DiscoveryRequest(BaseModel):
    question: str = Field(min_length=3, max_length=1000)
    domain: str = Field(default="general", max_length=50)


# ==================================================
# NEXUS BRAIN - INSTRUCTIONS IA
# ==================================================

SYSTEM_INSTRUCTIONS = """
Tu es NEXUS BRAIN, le moteur central de JOSNEXUS AI.

Tu es un assistant intelligent multisectoriel.

TES DOMAINES :
- Finance et marchés financiers.
- Sport et statistiques.
- Économie mondiale.
- Commerce et entreprises.
- Actualités et événements.
- Recherche et découverte de tendances.

TES REGLES :

1. Réponds toujours en français clair.
2. Comprends la question avant de répondre.
3. Organise tes réponses avec des titres si nécessaire.
4. Explique les causes, les conséquences et les possibilités.
5. Distingue les faits connus, les hypothèses et les estimations.
6. N'invente jamais des statistiques ou des sources.
7. Si une information récente nécessite une source en direct,
   précise que tu ne disposes pas encore de cette source.
8. En finance, explique toujours les risques.
9. En sport, ne garantis jamais un résultat.
10. Ne promets jamais de bénéfices financiers.
11. Si tu ne connais pas une réponse, dis-le honnêtement.

IDENTITE :

Tu représentes JOSNEXUS AI, une plateforme conçue par
Jospin Djigui.

Ton objectif est de transformer les questions en analyses
compréhensibles, structurées et utiles.
"""


# ==================================================
# CONNEXION GEMINI
# ==================================================

def get_gemini_client():

    if not GEMINI_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="La clé API Gemini n'est pas configurée."
        )

    return genai.Client(api_key=GEMINI_API_KEY)


# ==================================================
# PAGE D'ACCUEIL
# ==================================================

@app.get("/")
def home():

    index_file = FRONTEND_DIR / "index.html"

    if index_file.exists():
        return FileResponse(index_file)

    return {
        "project": "JOSNEXUS AI",
        "status": "online"
    }


# ==================================================
# ETAT DU SERVEUR
# ==================================================

@app.get("/api/health")
def health():

    return {
        "success": True,
        "project": "JOSNEXUS AI",
        "status": "online",
        "ai_configured": bool(GEMINI_API_KEY),
        "model": GEMINI_MODEL,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


# ==================================================
# LISTE DES MODULES
# ==================================================

@app.get("/api/modules")
def get_modules():

    return {
        "success": True,
        "total": len(MODULES),
        "modules": MODULES
    }


# ==================================================
# VUE GENERALE
# ==================================================

@app.get("/api/overview")
def overview():

    return {
        "success": True,
        "project": "JOSNEXUS AI",
        "version": "1.1.0",
        "modules": len(MODULES),
        "ai_status": (
            "configured"
            if GEMINI_API_KEY
            else "not_configured"
        ),
        "model": GEMINI_MODEL
    }


# ==================================================
# NEXUS BRAIN - ANALYSE INTELLIGENTE
# ==================================================

@app.post("/api/discovery")
def discovery(request: DiscoveryRequest):

    try:

        client = get_gemini_client()

        prompt = f"""
{SYSTEM_INSTRUCTIONS}

DOMAINE SELECTIONNE :
{request.domain}

QUESTION DE L'UTILISATEUR :
{request.question}

Produis une réponse claire, structurée et utile.
Indique les limites éventuelles de ton analyse.
"""

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )

        answer = response.text

        if not answer:
            raise HTTPException(
                status_code=502,
                detail="Gemini n'a pas produit de réponse."
            )

        return {
            "success": True,
            "project": "JOSNEXUS AI",
            "engine": "NEXUS BRAIN",
            "domain": request.domain,
            "question": request.question,
            "status": "ai",
            "model": GEMINI_MODEL,
            "analysis": answer,
            "sources": [],
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=502,
            detail=(
                "Le moteur Gemini n'a pas pu répondre. "
                "Vérifiez la clé API, le modèle et les limites "
                "de votre compte Google AI Studio."
            )
        )


# ==================================================
# FICHIERS DE L'INTERFACE
# ==================================================

if FRONTEND_DIR.exists():

    app.mount(
        "/static",
        StaticFiles(directory=str(FRONTEND_DIR)),
        name="static"
)
    
