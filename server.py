from fastapi import FastAPI, APIRouter, HTTPException
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, ConfigDict
from typing import List
import uuid
from datetime import datetime, timezone
import logging
from pathlib import Path
from dotenv import load_dotenv
import os

# === Configuration ===
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / ".env")

app = FastAPI(title="Dashboard Backend", version="1.0.0")

# === Middleware CORS (pour autoriser React en local) ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # autorise toutes les origines en dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Logger ===
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# === Modèles de données ===
class StatusCheck(BaseModel):
    model_config = ConfigDict(extra="ignore")  # Ignore MongoDB _id
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class StatusCheckCreate(BaseModel):
    client_name: str

# === Routes API ===
api_router = APIRouter(prefix="/api")

@api_router.get("/")
async def root():
    return {"message": "Hello from backend 👋"}

# Exemple d’endpoint de test
@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    # Simule des données sans base de données
    dummy_data = [
        StatusCheck(client_name="Frontend", timestamp=datetime.now(timezone.utc)),
        StatusCheck(client_name="Monitoring", timestamp=datetime.now(timezone.utc))
    ]
    return dummy_data

# === Endpoint de connexion ===
class LoginRequest(BaseModel):
    username: str
    password: str

@api_router.post("/login")
async def login(request: LoginRequest):
    """
    Simple endpoint d’authentification.
    Pour le test : 
    identifiant = admin
    mot de passe = motdepasse123
    """
    logger.info(f"Tentative de connexion pour l'utilisateur {request.username}")

    if request.username == "admin" and request.password == "motdepasse123":
        return {"token": "fake-jwt-token-12345"}
    else:
        raise HTTPException(status_code=401, detail="Identifiants incorrects")

# === Intégration du routeur ===
app.include_router(api_router)

# === Point d'entrée principal ===
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
