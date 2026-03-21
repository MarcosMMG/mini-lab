from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db, list_projects

app = FastAPI(
    title="Mini AI-Native Dev Lab API",
    description="API simples para o laboratorio local full stack",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    init_db()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/projects")
def get_projects():
    return {"projects": list_projects()}
