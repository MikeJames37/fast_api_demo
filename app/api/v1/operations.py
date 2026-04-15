from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException, Depends, Query

from app.models import User
from app.shemas import OperationsRequest, OperationResponse, TransferCreateShema
from app.service import operations as operations_service
from sqlalchemy.orm import Session

from app.dependency import get_db, get_current_user

router = APIRouter()

@router.post("/operations/income", response_model=OperationResponse)
def add_income(operation: OperationsRequest, db: Session = Depends(get_db),
               current_user: User = Depends(get_current_user)):
    return operations_service.add_income(db, current_user, operation)


@router.post("/operations/expense", response_model=OperationResponse)
def add_expense(operation: OperationsRequest, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    return operations_service.add_expense(db, current_user, operation)

@router.get("/operations", response_model=list[OperationResponse])
def get_operations_list(
        wallet_id: Optional[int] = Query(None),
        date_from: Optional[datetime] = Query(None),
        date_to: Optional[datetime] = Query(None),
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    return operations_service.get_operations_list(db, user, wallet_id, date_from, date_to)

@router.post("/operations/transfer", response_model=OperationResponse)
def create_transfer(
        payload: TransferCreateShema,
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    return operations_service.transfer_between_wallets(
        db=db,
        user_id=user.id,
        from_wallet_id=payload.from_wallet_id,
        to_wallet_id=payload.to_wallet_id,
        amount=payload.amount,
    )
