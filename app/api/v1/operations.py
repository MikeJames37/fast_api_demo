from fastapi import APIRouter, HTTPException, Depends

from app.shemas import OperationsRequest
from app.service import operations as operations_service
from sqlalchemy.orm import Session

from app.dependency import get_db

router = APIRouter()

@router.post("/operations/income")
def add_income(operation: OperationsRequest, db: Session = Depends(get_db)):
    return operations_service.add_income(db, operation)


@router.post("/operations/expense")
def add_expense(operation: OperationsRequest, db: Session = Depends(get_db)):
    return operations_service.add_expense(db, operation)
