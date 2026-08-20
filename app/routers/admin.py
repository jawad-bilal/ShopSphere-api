from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..auth import get_current_admin
from ..database import get_db
from ..models import User
from ..schemas import UserOut

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/me", response_model=UserOut)
def admin_me(
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    return UserOut.model_validate(current_admin)
