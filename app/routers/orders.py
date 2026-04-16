from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..deps import get_db, get_current_user

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=schemas.OrderOut)
def create_order(
    order: schemas.OrderCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # normal user creates order for self; admin can create for anyone via user_id
    target_user_id = current_user.id
    if current_user.role == "admin" and order.user_id is not None:
        target_user_id = order.user_id
    return crud.create_order(db, target_user_id, order)

@router.get("/", response_model=list[schemas.OrderOut])
def list_orders(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user.role == "admin":
        return crud.get_orders(db)
    return crud.get_orders_for_user(db, current_user.id)

@router.get("/{order_id}", response_model=schemas.OrderOut)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    order = crud.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if current_user.role != "admin" and order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    return order

@router.put("/{order_id}", response_model=schemas.OrderOut)
def update_order(
    order_id: int,
    order_update: schemas.OrderUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    order = crud.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if current_user.role != "admin" and order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    updated = crud.update_order(db, order_id, order_update)
    return updated

@router.delete("/{order_id}", response_model=schemas.OrderOut)
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    order = crud.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if current_user.role != "admin" and order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    deleted = crud.delete_order(db, order_id)
    return deleted