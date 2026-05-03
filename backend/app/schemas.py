from pydantic import BaseModel
class DemandBase(BaseModel):
 title: str
 category: str
 description: str
 status: str
 owner: str
 created_at: str
class DemandCreate(DemandBase):
 pass
class DemandUpdate(DemandBase):
 pass
