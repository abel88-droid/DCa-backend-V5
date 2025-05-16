# app/routes/warnings.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models import Warning
from pydantic import BaseModel

router = APIRouter(prefix="/warnings", tags=["warnings"])

# Pydantic schemas to validate input/output
class WarningCreate(BaseModel):
    user_id: str
    guild_id: str
    reason: str | None = None

class WarningOut(BaseModel):
    id: int
    user_id: str
    guild_id: str
    reason: str | None = None

    class Config:
        orm_mode = True

@router.get("/", response_model=list[WarningOut])
async def get_warnings(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Warning))
    warnings = result.scalars().all()
    return warnings

@router.post("/", response_model=WarningOut)
async def create_warning(warning: WarningCreate, db: AsyncSession = Depends(get_db)):
    new_warning = Warning(**warning.dict())
    db.add(new_warning)
    await db.commit()
    await db.refresh(new_warning)
    return new_warning

@router.delete("/{warning_id}")
async def delete_warning(warning_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Warning).filter_by(id=warning_id))
    warning = result.scalars().first()
    if not warning:
        raise HTTPException(status_code=404, detail="Warning not found")
    await db.delete(warning)
    await db.commit()
    return {"detail": "Warning deleted"}
