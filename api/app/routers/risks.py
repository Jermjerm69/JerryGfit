from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.user import User
from app.models.risk import Risk
from app.schemas.risk import Risk as RiskSchema, RiskCreate, RiskUpdate
from app.core.security import get_current_user

router = APIRouter()


@router.post("/", response_model=RiskSchema, status_code=status.HTTP_201_CREATED)
def create_risk(
    risk_data: RiskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new risk."""
    db_risk = Risk(**risk_data.model_dump(), owner_id=current_user.id)
    db.add(db_risk)
    db.commit()
    db.refresh(db_risk)
    return db_risk


@router.get("/", response_model=List[RiskSchema])
def list_risks(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List all risks for the current user."""
    risks = (
        db.query(Risk)
        .filter(Risk.owner_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return risks


@router.get("/{risk_id}", response_model=RiskSchema)
def get_risk(
    risk_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a specific risk."""
    risk = db.query(Risk).filter(Risk.id == risk_id, Risk.owner_id == current_user.id).first()
    if not risk:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Risk not found"
        )
    return risk


@router.put("/{risk_id}", response_model=RiskSchema)
def update_risk(
    risk_id: int,
    risk_data: RiskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update a risk (stub - to be fully implemented)."""
    risk = db.query(Risk).filter(Risk.id == risk_id, Risk.owner_id == current_user.id).first()
    if not risk:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Risk not found"
        )

    # Update fields
    update_data = risk_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(risk, field, value)

    db.commit()
    db.refresh(risk)
    return risk


@router.delete("/{risk_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_risk(
    risk_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a risk."""
    risk = db.query(Risk).filter(Risk.id == risk_id, Risk.owner_id == current_user.id).first()
    if not risk:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Risk not found"
        )

    db.delete(risk)
    db.commit()
    return None
