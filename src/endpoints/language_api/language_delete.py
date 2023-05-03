import logging

from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.endpoints.auth import get_current_librarian
from src.models import all_models
from src.models.database import get_db

from .router_init import router


@router.delete("/{language_id}", response_model=None, status_code=status.HTTP_200_OK)
async def delete_language_by_id(
    language_id: int,
    user: dict = Depends(get_current_librarian),
    db: Session = Depends(get_db),
) -> all_models.Language:
    """
    This function will be used to delete a language by id.
    Parameters:
        language_id: The id of the language.
        user: The user data. (current librarian)
        db: The database session.
    Returns:
        language: The deleted language.
    """
    logging.info("Deleting language in database with id: " + str(language_id))
    found_language = db.scalars(
        select(all_models.Language).where(all_models.Language.id == language_id)
    ).first()
    if not found_language:
        logging.warning("Language not found in database")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Language not found"
        )
    try:
        db.delete(found_language)
        db.commit()
        logging.info("Deleted language in database with id: " + str(language_id))
        return found_language
    except Exception as e:
        logging.exception("Error deleting language from database. Details = " + str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))