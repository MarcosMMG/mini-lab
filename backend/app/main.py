from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.database import (
    init_db,
    list_demands,
    get_demand_by_id,
    create_demand,
    update_demand,
    delete_demand,
)
from app.schemas import DemandCreate, DemandUpdate
from app.services import build_summary, normalize_status

app = FastAPI(
    title="Painel de Demandas e Ações API",
    description="API da base comum do projeto de extensão",
    version="2.0.0",
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


@app.get("/demands")
def get_demands():
    return {"demands": list_demands()}


@app.get("/summary")
def get_summary_route():
    return build_summary()


@app.post("/demands")
def create_demand_route(demand: DemandCreate):
    new_demand = create_demand(
        title=demand.title,
        category=demand.category,
        description=demand.description,
        status=normalize_status(demand.status),
        owner=demand.owner,
        created_at=demand.created_at,
    )
    return {"message": "Demanda criada com sucesso.", "demand": new_demand}


@app.put("/demands/{demand_id}")
def update_demand_route(demand_id: int, demand: DemandUpdate):
    existing = get_demand_by_id(demand_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Demanda não encontrada.")
    updated = update_demand(
        demand_id=demand_id,
        title=demand.title,
        category=demand.category,
        description=demand.description,
        status=normalize_status(demand.status),
        owner=demand.owner,
        created_at=demand.created_at,
    )
    return {"message": "Demanda atualizada com sucesso.", "demand": updated}


@app.delete("/demands/{demand_id}")
def delete_demand_route(demand_id: int):
    existing = get_demand_by_id(demand_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Demanda não encontrada.")
    delete_demand(demand_id)
    return {"message": "Demanda removida com sucesso."}
