import logging

from fastapi import Depends, Path
from sqlalchemy import and_, not_, select
from sqlalchemy.orm import Session
from starlette import status

from src.dependencies import get_current_librarian, get_db
from src.endpoints.user.exceptions import db_not_available, user_not_exist
from src.endpoints.user.router_init import router
from src.models.user import User
from src.responses import custom_response


@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=None)
async def get_user_by_id(
    librarian: dict = Depends(get_current_librarian),
    db: Session = Depends(get_db),
    user_id: int = Path(gt=0),
) -> dict:
    """
    Returns a single user.\n
    Param
    -----
    user_id: int\n
    JWT token of a librarian.
    Throws an exception if JWT is not of librarian\n
    Returns
    ------
    dict : A dict with status code, details and data
    """
    try:
        user = (
            db.execute(
                select(User).where(and_(User.id == user_id, not_(User.is_deleted)))
            )
            .scalars()
            .first()
        )
    except Exception:
        logging.exception(f"Exception occured -- {__name__}.get_user_by_id")
        raise db_not_available()
    if user:
        logging.info(f"Returning a single user. -- {__name__}.get_user_by_id")
        return custom_response(
            status_code=status.HTTP_200_OK, details="User found", data=user
        )
    else:
        logging.error(f"User not found -- {__name__}.get_user_by_id")
        raise user_not_exist()
