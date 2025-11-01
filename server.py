from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, ConfigDict
from typing import List
from datetime import datetime, timezone
import uuid
import os
import logging
from pathlib import Path

# Chargement éventuel des variables d’environnement (.env)
from dotenv import load_dotenv
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / ".env")

# ---------------------------------------------------------------------------
# ⚙️ Application principale
# ---------------------------------------------------------------------------
app = FastAPI(title="Dashboard Backend")

# Router principal avec préfixe /api
api_router = APIRouter(prefix="/api")

# ---------------------------------------------------------------------------
# 🔒 CORS (autorisations pour le frontend)
# ---------------------------------------------------------------------------
origins = os.environ.get("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# 🧱 Modèles Pydantic
# ---------------------------------------------------------------------------
class StatusCheck(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class StatusCheckCreate(BaseModel):
    client_name: str

# ---------------------------------------------------------------------------
# 🧠 Routes principales
# ---------------------------------------------------------------------------
@api_router.get("/")
async def root():
    return {"message": "Hello from backend 👋"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    """Fake endpoint pour tests (aucune base MongoDB ici)."""
    status_obj = StatusCheck(**input.dict())
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    """Retourne un exemple statique pour le test."""
    return [
        StatusCheck(client_name="Matthis"),
        StatusCheck(client_name="TestClient"),
    ]

# ---------------------------------------------------------------------------
# 🔐 Authentification simple
# ---------------------------------------------------------------------------
class LoginRequest(BaseModel):
    username: str
    password: str

@api_router.post("/login")
async def login(request: LoginRequest):
    """Vérifie les identifiants fournis par le frontend."""
    VALID_USERNAME = "admin"
    VALID_PASSWORD = "motdepasse123"

    if request.username == VALID_USERNAME and request.password == VALID_PASSWORD:
        return {
            "token": "fake-jwt-token",
            "user": request.username,
            "message": "Connexion réussie ✅"
        }
    else:
        raise HTTPException(status_code=401, detail="Identifiants incorrects")

# ---------------------------------------------------------------------------
# 🪵 Logging basique
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# 🚀 Lien du router principal
# ---------------------------------------------------------------------------
app.include_router(api_router)

# ---------------------------------------------------------------------------
# (Facultatif) Exécution locale : uvicorn server:app --reload
# ---------------------------------------------------------------------------
